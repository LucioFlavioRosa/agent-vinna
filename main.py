import streamlit as st
import agent_vinna

import pandas as pd

# Título do aplicativo
st.title("Bem Vindo ao AGENT VINNA")

# Texto exibido
st.write("Aqui você pode conversar com seu dado")

image_path = "vinna.png"
st.image(image_path, use_column_width='always')

pergunta = st.text_input("Qual a sua pergunta?")

if pergunta:

    #with st.spinner('O agente está buscando a melhor maneira de responder a sua pergunta!...'):
    response = agent_vinna.main(question=pergunta)
    
    if type(response) == pd.DataFrame:
        st.dataframe(response)
    elif hasattr(response, 'plot'):
        st.pyplot(response)
    else:
        st.write(response)
