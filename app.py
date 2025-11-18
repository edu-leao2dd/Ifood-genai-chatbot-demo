import streamlit as st
from groq import Groq

# Interface
st.title("iFood GenAI Chatbot Demo")
st.write("Chatbot simples usando Llama3 via Groq API — projeto para vaga GenAI iFood.")

# Chave da API
api_key = st.text_input("Digite sua GROQ_API_KEY:", type="password")

# Input do usuário
user_input = st.text_area("Digite sua pergunta:")

# Resposta
if st.button("Enviar"):
    if not api_key:
        st.error("Por favor, coloque sua GROQ_API_KEY.")
    else:
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Você é um assistente de IA útil."},
                {"role": "user", "content": user_input},
            ],
        )

        st.subheader("Resposta:")
        st.write(completion.choices[0].message["content"])
