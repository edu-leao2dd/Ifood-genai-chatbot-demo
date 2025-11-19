import streamlit as st
from groq import Groq

# Interface e Título
st.title("iFood GenAI Chatbot Demo")
st.write("Chatbot simples usando Llama3 via Groq API — projeto para vaga GenAI iFood.")

# Lógica de Chave: Tenta ler do secrets.toml, se não achar, pede input.
api_key = st.secrets.get("groq_api_key")

if not api_key:
    # Se a chave não estiver no secrets.toml, mostra o campo de input
    api_key = st.text_input("Digite sua GROQ_API_KEY:", type="password")

# Input do usuário
user_input = st.text_area("Digite sua pergunta:")

# Resposta
if st.button("Enviar"):
    if not api_key:
        st.error("Por favor, coloque sua GROQ_API_KEY.")
    else:
        # O cliente Groq agora usa a chave lida do secrets OU do input
        client = Groq(api_key=api_key)
        
        # Feedback visual enquanto a IA pensa
        with st.spinner("Gerando resposta..."): 
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": "Você é um assistente de IA útil."},
                    {"role": "user", "content": user_input},
                ],
            )

        st.subheader("Resposta:")
        st.write(completion.choices[0].message.content)