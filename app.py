import streamlit as st
from google import genai
from google.genai import types

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

# Laad het token uit de Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    token = st.secrets["GEMINI_API_KEY"].strip()
else:
    st.error("⚠️ Token niet gevonden in Streamlit Secrets!")
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
                "Step 2: Translate that improved meaning into authentic Dominican Spanish street slang.\n"
                "Step 3: Translate that exact same meaning into a single, natural, and correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw Dominican translation. No formatting, no asterisks, no notes.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the entire phrase in the Dutch language. Do NOT use bullet points, do NOT list individual words, and do NOT write English explanations. Just write ONE single, complete Dutch text/sentence that explains the total meaning."
            )
        else:
            system_prompt = (
                "You are an expert in Dominican Republic slang.\n"
                "Step 1: Translate the Dominican slang text into clear, natural English.\n"
                "Step 2: Translate that same meaning into a single, natural, and correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw English translation.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the phrase in the Dutch language as ONE single text. No bullet points, no individual word breakdowns, no fluff."
            )

        try:
            with st.spinner("Vertalen..."):
                # FIX: We geven de 'AQ...' code nu expliciet mee als OAuth/Access token aan de client
                client = genai.Client(http_options={'headers': {'Authorization': f'Bearer {token}'}})
                
                try:
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.8
                        )
                    )
                except Exception:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.8
                        )
                    )
                
                if response.text:
                    full_text = response.text
                    
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
                    st.info(f"**Wat betekent dit in het Nederlands:**\n\n{cleaned_dutch}")
                else:
                    st.error("Google stuurde een leeg antwoord terug.")
                    
        except Exception as e:
            st.error(f"Er ging iets mis met je token: {e}")
else:
    st.info("Voeg eerst je token toe aan de Secrets.")
