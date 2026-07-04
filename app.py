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
st.write("Vertaal, verbeter en begrijp Dominicaanse straattaal (*Qué lo qué!*).")

# 2. Google Gemini API Sleutel invoeren
api_key = st.text_input("Vul je GRATIS Google Gemini API sleutel in:", type="password")

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
                    "You are an expert translator and language improver for Dominican Republic street slang.\n"
                    "Step 1: Analyze the user's English input. If it has typos, bad grammar, or sounds unnatural, improve it so it sounds like a confident native English speaker first.\n"
                    "Step 2: Translate that improved meaning into authentic Dominican Spanish street slang.\n"
                    "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using a special delimiter '---'.\n"
                    "Part 1 (Before '---'): Output ONLY the clean, raw Dominican translation. No formatting, no asterisks, no notes. This will be copied to clipboard.\n"
                    "Part 2 (After '---'): Provide a brief, helpful explanation in English or Dutch explaining the slang used (like klk, tigre, vaina) and any nuances, so the user learns the street context."
                )
            else:
                system_prompt = (
                    "You are an expert in Dominican Republic slang.\n"
                    "Step 1: Translate the Dominican slang text into clear, natural, and grammatically correct English.\n"
                    "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using a special delimiter '---'.\n"
                    "Part 1 (Before '---'): Output ONLY the clean, raw English translation. No formatting or notes.\n"
                    "Part 2 (After '---'): Provide a brief explanation of the original Dominican slang terms used and what they imply on the streets."
                )

            try:
                with st.spinner("Vertalen en analyseren..."):
                    client = genai.Client(api_key=api_key.strip())
                    
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
                        
                        # We splitsen het antwoord van de AI op het '---' teken
                        if "---" in full_text:
                            parts = full_text.split("---")
                            translation_part = parts[0].strip()
                            explanation_part = parts[1].strip()
                        else:
                            translation_part = full_text.strip()
                            explanation_part = "Geen extra uitleg beschikbaar."

                        # Haal ongewenste symbolen uit het kopieergedeelte
                        cleaned_translation = translation_part.replace("**", "").replace("*", "").strip()
                        
                        st.success("**Klaar!**")
                        
                        # 📲 Schone kopieerbox voor WhatsApp (ZONDER de uitleg)
                        st.text_input(
                            label="Tik hierop om te kopiëren voor de afzender:", 
                            value=cleaned_translation, 
                            key="output_text"
                        )
                        
                        # 📖 De uitleg zetten we er netjes apart onder
                        st.info("**Wat betekent dit precies?**")
                        st.write(explanation_part)
                        
                    else:
                        st.error("Google stuurde een leeg antwoord terug.")
                        
            except Exception as e:
                st.error(f"Er ging iets mis: {e}")
        else:
            st.warning("Typ eerst een tekst.")
else:
    st.info("Vul eerst je Google Gemini API-sleutel in.")
