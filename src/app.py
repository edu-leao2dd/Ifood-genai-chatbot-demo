import streamlit as st
from groq import Groq

# Contexto de IA para o iFood (System Prompt)
SYSTEM_PROMPT = "Você é um assistente de IA amigável focado em culinária e delivery, respondendo com dicas de receitas, sugestões de restaurantes, ou fatos curiosos sobre comida. Mantenha as respostas curtas e úteis, como um concierge de alimentos."

# Inicialização da Memória (st.session_state)
if "messages" not in st.session_state:
    # O histórico começa com o System Prompt
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Interface e Título
st.title("iFood GenAI Chatbot Demo")
st.write("Chatbot simples usando Llama3 via Groq API — projeto para vaga GenAI iFood.")

# Lógica de Chave: Tenta ler do secrets.toml, se não achar, pede input.
api_key = st.secrets.get("groq_api_key")
if not api_key:
    api_key = st.text_input("Digite sua GROQ_API_KEY:", type="password")


# EXIBIÇÃO: Mostra o Histórico de Conversa (o Chat)
# Ignora o System Prompt (primeira mensagem) ao exibir
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CRIA O FORMULÁRIO COM LIMPEZA AUTOMÁTICA (Corrigindo o UX)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Digite sua pergunta:", key="user_input_area")
    submitted = st.form_submit_button("Enviar")

# LÓGICA DE RESPOSTA (Roda se o botão for clicado E houver texto)
if submitted and user_input:
    if not api_key:
        st.error("Por favor, coloque sua GROQ_API_KEY.")
    else:
        # Adiciona a mensagem do usuário ao histórico ANTES de chamar a API
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Exibe a nova mensagem do usuário no chat
        with st.chat_message("user"):
            st.markdown(user_input)
        
        client = Groq(api_key=api_key)
        
        with st.spinner("Gerando resposta..."): 
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                # A API recebe o histórico COMPLETO
                messages=st.session_state.messages, 
            )

        # Pega a resposta do assistente e adiciona ao histórico
        assistant_response = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Exibe a resposta do assistente no chat
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            
        # Força o Streamlit a re-renderizar
        st.rerun()