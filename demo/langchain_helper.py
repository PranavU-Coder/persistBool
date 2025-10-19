from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

from persist_bool import SentimentAnalyzer

def ask_boolean_question(user_question, system_prompt):
    
    llm = ChatOllama(
        model="llama3.2",  
        temperature=0.5
    )
    
    parser = SentimentAnalyzer()
    
    prompt_template = PromptTemplate(
        input_variables=['query'],
        template="{system_prompt}\n\n{query}\n\n"
    )
    
    chain = prompt_template | llm | parser
    
    response = chain.invoke({
        "system_prompt": system_prompt,
        "query": user_question
    })
    
    print(f"Question: {user_question}")
    print(f"Response: {response}")  
    
    return response