import streamlit as st
import requests

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
                prompt_instruction = (
                    "You are an expert translator specializing in Dominican Republic Spanish. "
                    "Translate the following English text into authentic Dominican Spanish. "
                    "Crucial: Use local Dominican slang, street language, and informal vocabulary "
                    "(like '¿Qué lo qué?', 'klk', 'tigre', 'wawawa', 'vaina', 'heavy', 'dime a ver'). "
                    "Do NOT use standard formal Spanish (Castilian). Make it sound natural on the streets of Santo Domingo. "
                    f"Text to translate: {user_input}"
                )
            else:
                prompt_instruction = (
                    "You are an expert in Dominican Republic slang and street language. "
                    "Translate the following Dominican slang text into clear, natural English so the user can easily understand "
                    "what the sender means, including the subtext of the street slang used. "
                    f"Text to translate: {user_input}"
                )

            try:
                with st.spinner("Vertalen via Google Gemini..."):
                    # FIX: De URL is nu ALTIJD hetzelfde en kan NOOIT meer breken door een sleutel!
                    url = "https://googleapis.com"
                    
                    # We sturen de sleutel veilig mee via de x-goog-api-key header
                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key.strip()
                    }
                    
                    data = {
                        "contents": [{
                            "parts": [{"text": prompt_instruction}]
                        }]
                    }
                    
                    response = requests.post(url=url, headers=headers, json=data)
                    
                    try:
                        result_json = response.json()
                        
                        if response.status_code == 200 and 'candidates' in result_json:
                            # Haal de tekst op uit de Google JSON structuur
                            translation = result_json['candidates'][0]['content']['parts'][0]['text']
                            st.success("**Vertaling:**")
                            st.code(translation, language="text")
                            st.caption("💡 Tip op je iPhone: Tik op het kopieer-icoontje rechtsboven in het grijze vak hierboven!")
                        else:
                            error_msg = result_json.get('error', {}).get('message', 'Onbekende fout')
                            st.error(f"Fout van Google: {error_msg}")
                            
                    except ValueError:
                        st.error(f"Google stuurde geen geldige data terug (Status {response.status_code}).")
                        
            except Exception as e:
                st.error(f"Er ging iets mis met de verbinding: {e}")
        else:
            st.warning("Typ eerst een tekst om te vertalen.")
else:
    st.info("Vul eerst je Google Gemini API-sleutel in om de app gratis te gebruiken.")
