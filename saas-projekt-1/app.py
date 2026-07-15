import streamlit as st
from groq import Groq
import pypdf

# ==========================================
# 1. SEITENEINSTELLUNGEN (Dein Browsertab-Titel)
# ==========================================
st.set_page_config(
    page_title="SocialCreator AI – PDF zu Social Media Posts",  # Name im Browsertab
    page_icon="🚀",  # Icon im Browsertab
    layout="wide",
)

# Verbindung zu Groq herstellen (Nutzt die verschlüsselten Secrets)
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error("Fehler: Der Groq API-Key konnte nicht in den Secrets gefunden werden.")
    st.stop()


# Funktion, um Text aus der PDF zu extrahieren
def extract_text_from_pdf(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# Funktion, um den Social Media Content via Groq zu generieren
def generate_social_content(input_text, platform):
    prompts = {
        "LinkedIn": (
            "Du bist ein professioneller LinkedIn-Ghostwriter. Erstelle aus dem folgenden Text "
            "einen fesselnden, professionellen LinkedIn-Post. Nutze Absätze, Emojis und "
            "beende den Post mit 3 relevanten Hashtags sowie einer Frage, die Interaktion anregt.\n\n"
            f"Textvorlage:\n{input_text}"
        ),
        "Twitter/X Thread": (
            "Du bist ein Experte für virale Twitter/X-Threads. Erstelle aus dem folgenden Text "
            "einen Thread bestehend aus genau 3 bis 5 durchnummerierten Tweets (1/, 2/, etc.). "
            "Jeder Tweet muss kurz, knackig und unter 280 Zeichen sein.\n\n"
            f"Textvorlage:\n{input_text}"
        ),
        "TikTok/Reels Script": (
            "Du bist ein genialer Kurzvideo-Creator. Erstelle aus dem folgenden Text ein "
            "Videoskript für ein TikTok oder Instagram Reel. Unterteile es klar in:\n"
            "- HOOK (Die ersten 3 Sekunden, um Aufmerksamkeit zu fesseln)\n"
            "- BODY (Der Hauptinhalt, leicht verständlich auf den Punkt gebracht)\n"
            "- CTA (Call to Action, was der Zuschauer tun soll)\n\n"
            f"Textvorlage:\n{input_text}"
        ),
    }

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # <-- Das neue, ultraschnelle Llama 3.1 Modell
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein weltklasse Social-Media-Manager. Antworte immer auf Deutsch.",
                },
                {"role": "user", "content": prompts[platform]},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Fehler bei der Generierung: {str(e)}"


# ==========================================
# 2. WILLKOMMENS-BEREICH & DESIGN (Die Optik)
# ==========================================
st.title("🚀 SocialCreator AI")

# Die schöne, farbige Infobox zur Begrüßung
st.info(
    "👋 **Willkommen!** Dieses Tool verwandelt deine Dokumente in Sekundenschnelle in fertige Social-Media-Beiträge. Lade einfach unten dein PDF hoch, um zu starten."
)

# Der strukturierte Ablauf für den User
st.markdown("""
### So einfach funktioniert es:
1. 📂 **PDF hochladen** (Dein Dokument)
2. 🎯 **Plattform wählen** (LinkedIn, X, TikTok)
3. ✨ **Content kopieren** (Fertig generiert durch Groq AI)
""")

st.divider()

# Grid Layout für die App (Upload und Generierung)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Quelle hochladen")
    uploaded_file = st.file_uploader("Wähle eine PDF-Datei aus", type=["pdf"])

    extracted_text = ""
    if uploaded_file is not None:
        with st.spinner("Extrahiere Text aus PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF erfolgreich geladen!")
            with st.expander("Vorschau des extrahierten Texts"):
                st.write(extracted_text[:1000] + "...")

with col2:
    st.header("2. Content generieren")
    platform = st.selectbox(
        "Für welche Plattform möchtest du Content erstellen?",
        ["LinkedIn", "Twitter/X Thread", "TikTok/Reels Script"],
    )

    if st.button("Content generieren ✨", type="primary"):
        if not extracted_text:
            st.warning("Bitte lade zuerst eine PDF-Datei hoch!")
        else:
            with st.spinner(f"Groq generiert deinen {platform}-Post..."):
                result = generate_social_content(extracted_text, platform)
                st.session_state["result"] = result

# Ergebnisbereich anzeigen
if "result" in st.session_state:
    st.divider()
    st.header("3. Dein fertiger Social-Media-Post")
    st.text_area(
        "Kopiere deinen Text hier:", value=st.session_state["result"], height=300
    )
    st.info(
        "Tipp: Du kannst den Text direkt oben kopieren und für deine Kanäle anpassen!"
    )
