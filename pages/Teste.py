import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["gemini"]["gemini_key"])

modelos = [
    m.name.replace("models/", "")
    for m in genai.list_models()
    if "generateContent" in m.supported_generation_methods
]

st.write(modelos)

if modelos:
    modelo = genai.GenerativeModel(modelos[0])
    r = modelo.generate_content("Responda apenas: OK")
    st.write(r.text)
