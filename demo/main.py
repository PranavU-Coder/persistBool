import streamlit as st
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import BooleanOutputParser
from langchain_core.output_parsers import StrOutputParser

def ask_boolean_question(user_question, system_prompt):
    
    llm = ChatOllama(
        model="llama3.2",  
        temperature=0.5
    )
    
    bool_parser = BooleanOutputParser()
    str_parser = StrOutputParser()
    
    prompt_template = PromptTemplate(
        input_variables=['query'],
        template="{system_prompt}\n\n{query}\n\n"
    )
    
    chain = prompt_template | llm | str_parser
        
    response = chain.invoke({
        "system_prompt": system_prompt,
        "query": user_question
    })
    
    return response


# Streamlit UI
st.title(" Boolean Question Assistant")

st.markdown("Ask yes/no questions and get boolean responses from the LLM!")

with st.sidebar:
    st.header("Configuration")
    
    system_prompt = st.text_area(
        label="System Prompt",
        value="You are a knowledgeable assistant who answers questions with enthusiasm and accuracy.",
        height=100,
        help="Define the personality and behavior of the assistant"
    )
    
    st.divider()
    
    st.markdown("### Example Questions")
    st.markdown("""
    - Is Python older than Java?
    - Should I learn React before Next.js?
    """)

# Main content
with st.form(key='question_form'):
    user_question = st.text_area(
        label="Ask a Yes/No Question",
        placeholder="Enter your question here...",
        height=100,
        max_chars=500
    )
    
    submit_button = st.form_submit_button(label='Submit Question', type="primary")

if submit_button and user_question:
    with st.spinner("Thinking..."):
        try:
            response = ask_boolean_question(user_question, system_prompt)
            
            st.divider()
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.subheader("Response:")
                if response:
                    st.success("YES")
                else:
                    st.error(" NO")
            
            with col2:
                st.subheader("Details:")
                st.write(f"**Question:** {user_question}")
                st.write(f"**Boolean Value:** `{response}`")
                st.write(f"**Type:** `{type(response).__name__}`")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submit_button:
    st.warning("Please enter a question before submitting!")