import streamlit as st
from groq import Groq

# 1. Pagina-instellingen voor mobiel (iPhone)
st.set_page_config(
    page_title="Dominicaanse Straattaal",
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

st.title("🇩🇴 Dominicaanse Straattaal")
st.write("Vertaal, verbeter en begrijp de taal van de Dominicaanse straten.")

# De sleutel wordt hier geruisloos ingeladen. Als hij ontbreekt, stopt de app direct met een foutmelding.
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
                "You are an expert translator and language improver for Dominican Republic street language.\n"
                "Step 1: Improve the user's English input so it sounds like a natural English speaker.\n"
                "Step 2: Translate that improved meaning into authentic Dominican Spanish street language (using terms like klk, tigre, vaina, heavy, dime a ver).\n"
                "Step 3: Translate that exact same meaning into a single, natural, and correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw Dominican translation. No formatting, no asterisks, no notes.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the phrase in the Dutch language. No bullet points, no grammatical explanations, no extra fluff. Just write ONE single, complete Dutch text/sentence that explains the total meaning."
            )
        else:
            system_prompt = (
                "You are an expert in Dominican Republic street language.\n"
                "Step 1: Translate the Dominican street text into clear, natural English.\n"
                "Step 2: Translate that same meaning into a single, natural, and correct Dutch sentence.\n"
                "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
                "Part 1 (Before '---'): Output ONLY the clean, raw English translation.\n"
                "Part 2 (After '---'): Output ONLY the direct, natural translation of the phrase in the Dutch language as ONE single text. No fluff, just the pure Dutch sentence."
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
                
                # FIX: We hebben hier [0] toegevoegd om de eerste keuze correct uit de lijst te pakken
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
