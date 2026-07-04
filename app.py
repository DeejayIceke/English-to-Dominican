import streamlit as st
from google import genai
from google.genai import types

# 1. Pagina-instellingen voor mobiel (iPhone)
st.set_page_config(
    page_title="Dominican Translate",
    page_icon="🇩🇴",
    layout="centered"
)

# Voeg styling toe voor mooie knoppen op mobiel
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇩🇴 Dominican Slang Translator (Gratis)")
st.write("Vertaal snel tussen Engels en Dominicaanse straattaal (*Qué lo qué!*).")

# 2. Google Gemini API Sleutel invoeren
api_key = st.text_input("Vul je GRATIS Google Gemini API sleutel in (begint met AIzaSy of AQ):", type="password")

if api_key:
    # 3. Kies de vertaalrichting
    direction = st.radio(
        "Kies de richting:",
        ("Engels ➡️ Dominicaanse Straattaal", "Dominicaanse Straattaal ➡️ Engels")
    )

    # 4. Invoervak voor de tekst
    user_input = st.text_area("Typ of plak hier je tekst:", height=100)

    if st.button("Vertaal nu 🔥"):
        if user_input:
            if direction == "Engels ➡️ Dominicaanse Straattaal":
                system_prompt = (
                    "You are an expert translator specializing in Dominican Republic Spanish. "
                    "Translate the following English text into authentic Dominican Spanish. "
                    "Crucial: Use local Dominican slang, street language, and informal vocabulary "
                    "(like '¿Qué lo qué?', 'klk', 'tigre', 'wawawa', 'vaina', 'heavy', 'dime a ver'). "
                    "Do NOT use standard formal Spanish (Castilian). Make it sound natural on the streets of Santo Domingo."
                )
            else:
                system_prompt = (
                    "You are an expert in Dominican Republic slang and street language. "
                    "Translate the following Dominican slang text into clear, natural English so the user can easily understand "
                    "what the sender means, including the subtext of the street slang used."
                )

            try:
                with st.spinner("Vertalen via Google Gemini..."):
                    # We starten de officiële Google Client op met jouw sleutel
                    client = genai.Client(api_key=api_key.strip())
                    
                    # We roepen het model aan via de officiële bibliotheek
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.8
                        )
                    )
                    
                    # Toon de vertaling netjes op het scherm
                    if response.text:
                        st.success("**Vertaling:**")
                        st.code(response.text, language="text")
                        st.caption("💡 Tip op je iPhone: Tik op het kopieer-icoontje rechtsboven in het grijze vak hierboven!")
                    else:
                        st.error("Google stuurde een leeg antwoord terug.")
                        
            except Exception as e:
                st.error(f"Er ging iets mis met het ophalen van de vertaling: {e}")
        else:
            st.warning("Typ eerst een tekst om te vertalen.")
else:
    st.info("Vul eerst je Google Gemini API-sleutel in om de app gratis te gebruiken.")
