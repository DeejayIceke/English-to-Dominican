import streamlit as st
from groq import Groq

# 1. Pagina-instellingen voor mobiel (iPhone)
st.set_page_config(
    page_title="Dominicaanse Straattaal",
    page_icon="🇩🇴",
    layout="centered"
)

# CSS-styling voor grotere tekst op knoppen en in het invoervak
st.markdown("""
    <style>
    /* Styling voor de vertaalknop */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-size: 20px;
        font-weight: bold;
    }
    /* Styling voor de tekst binnen het invoervak */
    .stTextArea textarea {
        font-size: 18px !important;
    }
    /* Styling voor de label boven het invoervak */
    .stTextArea label p {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇩🇴 Dominicaanse Straattaal")
st.write("Vertaal, verbeter en begrijp de taal van de Dominicaanse straten.")

# De sleutel wordt hier geruisloos ingeladen.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    st.error("⚠️ API-sleutel niet gevonden in Streamlit Secrets!")
    st.stop()

# Invoervak voor de tekst
user_input = st.text_area("Typ of plak hier je tekst (Engels of Dominicaans):", height=100)

if st.button("🇩🇴 Vertaal nu"):
    if user_input:
        # FIX: De instructies zijn nu extreem streng gemaakt om slechts ÉÉN zin zonder alternatieven te genereren
        system_prompt = (
            "You are an expert translator and language identifier for Dominican Republic street language.\n"
            "CRUCIAL TASK: Analyze the user's input text. Automatically detect if it is in English or in Dominican Spanish slang.\n\n"
            "IF THE INPUT IS IN ENGLISH:\n"
            "1. Improve the English input so it sounds like a natural, confident native English speaker first.\n"
            "2. Translate that improved meaning into authentic Dominican Spanish street language (using terms like klk, tigre, vaina, heavy, dime a ver naturally).\n"
            "3. Translate that exact same meaning into a natural, correct Dutch sentence.\n\n"
            "IF THE INPUT IS IN DOMINICAN SPANISH/SLANG:\n"
            "1. Translate the Dominican street text into clear, natural English.\n"
            "2. Translate that same meaning into a single, natural, and correct Dutch sentence.\n\n"
            "CRUCIAL OUTPUT RULES FOR FORMATTING:\n"
            "You must split your response into exactly two parts using the delimiter '---'.\n"
            "Part 1 (Before '---'): Output ONLY ONE SINGLE, BEST direct translation sentence. Do NOT list multiple options. Do NOT separate alternatives with hyphens (-). Do NOT include notes or markdown formatting like asterisks. Just give the single final sentence to be copied.\n"
            "Part 2 (After '---'): Output ONLY the direct, natural translation of that exact phrase in the Dutch language as ONE single text block. No fluff, just the pure Dutch meaning."
        )

        try:
            with st.spinner("Vertalen..."):
                client = Groq(api_key=api_key)
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )
                
                full_text = response.choices[0].message.content
                
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
                    
        except Exception as e:
            st.error(f"Er ging iets mis met het ophalen van de vertaling: {e}")
    else:
        st.warning("Typ eerst een tekst.")
