import streamlit as st
from groq import Groq

# 1. SETUP & KONFIGURATION
# Hier hinterlegst du deinen geheimen API-Schlüssel für die KI
# (In einem echten SaaS holt man das sicher aus einer .env Datei!)
# Streamlit holt sich den Schlüssel jetzt automatisch aus der secrets.toml
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Verbindung zum KI-Anbieter (Groq) herstellen
client = Groq(api_key=GROQ_API_KEY)

# 2. FRONTEND: DIE WEBSITE GESTALTEN
st.set_page_config(page_title="ImmoText AI", page_icon="🏠")
st.title("🏠 ImmoText AI — Der Exposé-Schreiber")
st.write(
    "Gib die Daten deiner Immobilie ein und lass die KI ein professionelles Exposé schreiben."
)

# Eingabefelder für den Makler erstellen
quadratmeter = st.number_input(
    "Quadratmeter (qm):", min_value=10, max_value=1000, value=75
)
zimmer = st.text_input(
    "Zimmer & Besonderheiten:", placeholder="z.B. 3 Zimmer, Balkon, Einbauküche"
)
zustand = st.selectbox(
    "Zustand der Immobilie:",
    ["Erstbezug / Neubau", "Gepflegt / Renoviert", "Renovierungsbedürftig"],
)

# Ein schöner blauer Button zum Starten
button_geklickt = st.button("Professionellen Text generieren", type="primary")

# 3. LOGIK: DATEN AN DIE KI SENDEN
if button_geklickt:
    # Wir zeigen eine kleine Lade-Animation an
    with st.spinner("Die KI schreibt dein Exposé..."):

        # Der "geheime" Befehl (Prompt) an das KI-Modell
        system_prompt = "Du bist ein professioneller deutscher Immobilienmakler. Schreibe ein einladendes, hochwertiges Exposé."
        user_prompt = f"Erstelle einen Text für ein Objekt mit {quadratmeter}qm, folgenden Merkmalen: {zimmer}. Zustand: {zustand}."

        # Der API-Aufruf: Wir schicken die Daten in die Cloud
        antwort = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Das KI-Modell, das wir nutzen wollen
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,  # Kreativität der KI (0.0 = sachlich, 1.0 = sehr kreativ)
        )

        # Wir holen den reinen Text aus der Antwort heraus
        fertiger_text = antwort.choices[0].message.content

        # 4. AUSGABE: TEXT DEM KUNDEN ANZEIGEN
        st.success("Fertig generiert!")
        st.subheader("Dein fertiges Exposé:")
        st.text_area(
            label="Kopiere den Text hier heraus:", value=fertiger_text, height=300
        )
