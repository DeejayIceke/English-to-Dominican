import streamlit as st
import requests
import json

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

# 2. OpenRouter API Sleutel invoeren
api_key = st.text_input("Vul je GRATIS OpenRouter API sleutel in:", type="password")

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
                with st.spinner("Vertalen..."):
                    # We schieten de aanroep rechtstreeks naar OpenRouter via een HTTP POST-request
                    headers = {
                        "Authorization": f"Bearer {api_key.strip()}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "model": "google/gemini-2.5-flash:free",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": 0.8
                    }
                    
                    response = requests.post(
                        url="https://openrouter.ai",
                        headers=headers,
                        data=json.dumps(data)
                    )
                    
                    # Verwerk het resultaat
                    result_json = response.json()
                    
                    if response.status_code == 200 and 'choices' in result_json:
                        translation = result_json['choices'][0]['message']['content']
                        st.success("**Vertaling:**")
                        st.code(translation, language="text")
                        st.caption("💡 Tip op je iPhone: Tik op het kopieer-icoontje rechtsboven in het grijze vak hierboven!")
                    else:
                        # Toon de exacte foutboodschap van OpenRouter als het misgaat
                        error_msg = result_json.get('error', {}).get('message', 'Onbekende fout')
                        st.error(f"Fout van OpenRouter: {error_msg}")
                        
            except Exception as e:
                st.error(f"Er ging iets mis met de verbinding: {e}")
        else:
            st.warning("Typ eerst een tekst om te vertalen.")
else:
    st.info("Vul eerst je OpenRouter API-sleutel in om de app gratis te gebruiken.")
