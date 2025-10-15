from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import BooleanOutputParser


def ask_boolean_question(user_question, system_prompt):
    
    llm = ChatOllama(
        model="llama3.2",  
        temperature=0.5
    )
    
    parser = BooleanOutputParser()
    
    # Manually provide format instructions since BooleanOutputParser doesn't implement get_format_instructions()
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
    print(f"Type: {type(response)}")
    
    return response


if __name__ == '__main__':
    SYSTEM_PROMPT = "You are a knowledgeable assistant who answers questions with enthusiasm and accuracy."
    
    ask_boolean_question("Is Python older than Java?", SYSTEM_PROMPT)
    print("\n" + "="*60 + "\n")
    
    ask_boolean_question("Should I learn React before learning Next.js?", SYSTEM_PROMPT)
    print("\n" + "="*60 + "\n")
    
    ask_boolean_question("Is the Earth larger than Mars?", SYSTEM_PROMPT)
