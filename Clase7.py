import streamlit as st
import groq
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']



def configurar_pagina():
    st.set_page_config(page_title="Mi primer chatbot con Phyton")
    st.title("Bienvenidos a mi chatbot")

def crear_cliente_groq():
    groq_apy_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_apy_key)

def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA favorito")
    modelo = st.sidebar.selectbox('elegí tu modelo',MODELOS,index=0)
    st.write(f'**Elegiste el modelo** {modelo}')
    return modelo

def mostrar_mensajes(role,content):
    with st.chat_message(role):
        st.markdown(content)

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje['rol']):
                st.markdown(mensaje['content'])

def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje al asistente")

def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
    return respuesta.choices[0].message.content

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()

    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()


    if mensaje_usuario:
        agregar_mensajes_previos("user",mensaje_usuario)
        mostrar_mensajes("user",mensaje_usuario)
    
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes)

        agregar_mensajes_previos("assistant",respuesta_contenido)
        mostrar_mensajes("assistant",respuesta_contenido)


if __name__ == '__main__':
    ejecutar_chat()
    








#pip freeze > requirements.txt es un comando para la terminal




