import streamlit as st
from groq import Groq
import time

# Configuración de la página
st.set_page_config(
    page_title="Mi ChatBot - Talento Tec",
    page_icon="🤖",
    layout="centered"
)

# Título principal
st.title("🤖 Mi ChatBot Personalizado")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("🔧 Configuración")
    
    # Obtener API Key de secrets.toml
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("✅ API Key cargada correctamente")
    except Exception as e:
        st.error("❌ No se pudo cargar la API Key")
        st.stop()
    
    # 🎯 MODELOS QUE SÍ FUNCIONAN (de tu detección)
    modelo = st.selectbox(
        "Selecciona el modelo:",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "qwen/qwen3-32b",
            "meta-llama/llama-4-maverick-17b-128e-instruct"
        ],
        index=0
    )
    
    # Configuraciones adicionales
    temperatura = st.slider("Creatividad:", 0.1, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Longitud respuesta:", 100, 2000, 1024, 100)
    
    # Botón para limpiar chat
    if st.button("🧹 Limpiar Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! 👋 El chat ha sido limpiado. ¿En qué puedo ayudarte?"}
        ]
        st.rerun()

# Estado inicial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu ChatBot personalizado. ¿En qué puedo ayudarte?"}
    ]

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Procesar con Groq
    try:
        # Configurar cliente (usa la API Key de secrets.toml)
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # Mostrar respuesta
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("💭 Pensando...")
            
            # Llamar a la API con system message para evitar repeticiones
            messages_with_system = [
                {"role": "system", "content": "Eres un asistente útil y amigable. Responde de manera natural en español."}
            ] + st.session_state.messages
            
            response = client.chat.completions.create(
                model=modelo,
                messages=messages_with_system,
                temperature=temperatura,
                max_tokens=max_tokens,
                stream=False
            )
            
            respuesta = response.choices[0].message.content
            message_placeholder.markdown(respuesta)
        
        # Agregar al historial
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        
        # 🖨️ Salida por terminal (para la captura)
        print("=" * 60)
        print("🚀 CHATBOT - Talento Tec")
        print(f"📝 Modelo: {modelo}")
        print(f"👤 Usuario: {prompt}")
        print(f"🤖 Respuesta: {respuesta}")
        print("=" * 60)
        
        # Recargar para mostrar el nuevo mensaje
        st.rerun()
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        st.error(f"❌ {error_msg}")
        print(f"🚫 ERROR: {error_msg}")

# Footer
st.markdown("---")
st.caption("🎓 Desafío 9 - ChatBot con IA - Talento Tec")