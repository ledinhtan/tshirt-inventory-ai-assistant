import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_sql_query_chain 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma 
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector 
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate 
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool 
from langchain_core.output_parsers import StrOutputParser 

from src.prompts import FEW_SHOTS, MYSQL_PROMPT, ANSWER_PROMPT
from src.database import get_db_connection

def create_sql_chain(api_key):
    # Initiate LLM & DB
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        api_key=api_key,
        temperature=0.3,  
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    db = get_db_connection()

    # VectorDB for Few-shot
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2') 
    
    to_vectorise = [" ".join(example.values()) for example in FEW_SHOTS]

    DB_VERSION = "v1" # If we update FEW_SHOTS in the file "prompts.py" in the future, we can change v1 into v2, etc. 
    persist_dir = f"./chroma_db_{DB_VERSION}"
    
    if os.path.exists(persist_dir): 
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        vectorstore = Chroma.from_texts(
            texts=to_vectorise, 
            embedding=embeddings, 
            metadatas=FEW_SHOTS, 
            persist_directory=persist_dir
        )

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

    # Build a prompt template
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=MYSQL_PROMPT,
        suffix="\nQuestion: {input}\nSQLQuery: ",
        input_variables=["input", "table_info", "top_k"]
    )

    # Create Chain components
    sql_generation_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)
    execute_query = QuerySQLDataBaseTool(db=db) # Create SQL execution tools
    answer_prompt_template = PromptTemplate.from_template(ANSWER_PROMPT)
    
    # A dictionary containing the chains so that app.py can easily call them
    return {
        "sql_gen": sql_generation_chain,
        "db_exec": execute_query,
        "answer_chain": answer_prompt_template | llm | StrOutputParser()
    }