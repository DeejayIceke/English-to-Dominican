import streamlit as st
from groq import Groq

# 1. Pagina-instellingen voor mobiel (iPhone)
st.set_page_config(
    page_title="Dominicaanse Straattaal",
    page_icon="🇩🇴",
    layout="centered"
)

st.title("🇩🇴 Dominicaanse Straattaal")
st.write("Vertaal, verbeter en begrijp de taal van de Dominicaanse straten.")

# De sleutel wordt hier geruisloos ingeladen.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
else:
    st.error("⚠️ API-sleutel niet gevonden in Streamlit Secrets!")
    st.stop()

# 2. Invoervak voor de tekst (De radio-knoppen en de drukknop zijn nu weg!)
user_input = st.text_area("Typ of plak hier je tekst (Engels of Dominicaans):", height=100)

# FIX: Geen st.button meer nodig! De app begint direct te lopen zodra er tekst in het vak staat.
if user_input:
    # We geven de AI één slimme, gecombineerde instructie om de taal zelf te detecteren
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
        "CRUCIAL OUTPUT FORMAT: You must split your response into exactly two parts using the delimiter '---'.\n"
        "Part 1 (Before '---'): Output ONLY the clean, raw translation (Dominican Spanish if input was English, or English if input was Dominican). No formatting, no asterisks, no notes. This will be copied to clipboard.\n"
        "Part 2 (After '---'): Output ONLY the direct, natural translation of the entire phrase in the Dutch language as ONE single text block. Do NOT use bullet points, do NOT list individual words, and do NOT write English explanations. Just write ONE single, complete Dutch text/sentence that explains the total meaning."
    )

    try:
        with st.spinner("Taal herkennen en live vertalen..."):
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
