import streamlit as st
import requests
import json

# 1. Pagina-instellingen voor mobiel (iPhone)
st.set_page_config(
    page_title="Dominican Translate",
    page_icon="🇩🇴",
    layout="centered"
)

# Voeg strakke styling toe voor iOS knoppen
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇩🇴 Dominican Translator")
st.write("Vertaal, verbeter en begrijp Dominicaanse straattaal.")

# Laad de Groq sleutel uit de Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    st.error("⚠️ API-sleutel niet gevonden in Streamlit Secrets!")
    st.stop()

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
                "You are an expert translator and language improver for Dominican Republic street slang.\n"
                "Step 1: Improve the user's English input so it sounds like a natural English speaker.\n"
                "Step 2: Translate that improved meaning into authentic Dominican Spanish street slang (using terms like klk, tigre, vaina, heavy, dime a ver).\n"
                "Step 3: Translate that exact same meaning into a natural, correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw Dominican translation. No formatting, no asterisks, no notes.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the phrase in the Dutch language. No bullet points, no grammatical explanations, no extra fluff. Just the pure Dutch sentence."
            )
        else:
            system_prompt = (
                "You are an expert in Dominican Republic slang.\n"
                "Step 1: Translate the Dominican slang text into clear, natural English.\n"
                "Step 2: Translate that same meaning into a natural, correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw English translation.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the phrase in the Dutch language as ONE single text. No fluff, just the pure Dutch sentence."
            )

        try:
            with st.spinner("Vertalen..."):
                url = "https://groq.com"
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7
                }
                
                response = requests.post(url=url, headers=headers, json=data)
                result_json = response.json()
                
                if response.status_code == 200 and 'choices' in result_json:
                    full_text = result_json['choices'][0]['message']['content']
                    
                    # FIX: Hier splitsen en strippen we de tekst nu per onderdeel correct op zonder te crashen
                    if "---" in full_text:
                        parts = full_text.split("---")
                        translation_part = parts[0].strip()
                        explanation_part = parts[1].strip()
                    else:
                        translation_part = full_text.strip()
                        explanation_part = "Geen Nederlandse vertaling beschikbaar."

                    cleaned_translation = translation_part.replace("**", "").replace("*", "").strip()
                    cleaned_dutch = explanation_part.replace("**", "").replace("*", "").strip()
                    
                    st.write("📋 **Kopieer de vertaling hieronder voor de afzender:**")
                    st.code(cleaned_translation, language="text")
                    st.info(f"**Betekenis in het Nederlands:**\n\n{cleaned_dutch}")
                else:
                    error_msg = result_json.get('error', {}).get('message', 'Onbekende fout')
                    st.error(f"Fout van server: {error_msg}")
                    
        except Exception as e:
            st.error(f"Er ging iets mis met de verbinding: {e}")
    else:
        st.warning("Typ eerst een tekst.")
