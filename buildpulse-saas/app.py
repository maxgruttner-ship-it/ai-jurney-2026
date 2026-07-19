import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="BuildPulse AI | Construction SaaS",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MOCK DATA GENERATION (Für den SaaS-Vibe) ---
if "projects" not in st.session_state:
    st.session_state.projects = pd.DataFrame(
        [
            {
                "Projekt": "Südturm Residenz",
                "Status": "In Arbeit",
                "Fortschritt": 65,
                "Budget (€)": 1200000,
                "Risiko": "Niedrig",
            },
            {
                "Projekt": "HafenCity Office",
                "Status": "Verzögert",
                "Fortschritt": 40,
                "Budget (€)": 4500000,
                "Risiko": "Hoch",
            },
            {
                "Projekt": "Kita Sonnenstraße",
                "Status": "Planung",
                "Fortschritt": 12,
                "Budget (€)": 850000,
                "Risiko": "Mittel",
            },
        ]
    )

if "machinery" not in st.session_state:
    st.session_state.machinery = pd.DataFrame(
        [
            {
                "Gerät": "Kran Liebherr 280",
                "Status": "Vermietet",
                "Projekt": "HafenCity Office",
                "Kosten/Tag": 450,
            },
            {
                "Gerät": "Bagger CAT 320",
                "Status": "Verfügbar",
                "Projekt": "-",
                "Kosten/Tag": 250,
            },
            {
                "Gerät": "Betonmischer MAN",
                "Status": "Verfügbar",
                "Projekt": "-",
                "Kosten/Tag": 180,
            },
        ]
    )

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏗️ BuildPulse AI")
st.sidebar.caption("Enterprise Vertical SaaS v1.0.0")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "📄 Angebotserstellung",
        "📐 Bauplan-Freigaben",
        "🚜 Maschinenvermietung",
        "⏱️ Zeiterfassung",
        "🧠 KI-Risiko-Vorhersage",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tipp:** Vertikale SaaS-Plattformen lösen spezifische Branchenprobleme 10x besser als allgemeine Software."
)

# ==========================================
# 📊 DASHBOARD
# ==========================================
if menu == "📊 Dashboard":
    st.title("📊 Bauprojekt-Dashboard")
    st.subheader("Echtzeit-Übersicht über alle aktiven Baustellen")

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aktive Projekte", "3", "+1 diesen Monat")
    col2.metric("Gesamtbudget verwaltet", "6.55 Mio. €", "Innerhalb des Rahmens")
    col3.metric("Maschinen-Auslastung", "66%", "Optimal")
    col4.metric(
        "Kritische Verzögerungen",
        "1 Projekt",
        "Aktion erforderlich",
        delta_color="inverse",
    )

    st.markdown("---")

    # Charts & Tables
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### 📈 Projektfortschritt vs. Budget")
        fig = px.bar(
            st.session_state.projects,
            x="Projekt",
            y="Budget (€)",
            color="Status",
            text="Fortschritt",
            color_discrete_map={
                "In Arbeit": "#2ecc71",
                "Verzögert": "#e74c3c",
                "Planung": "#3498db",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### ⚠️ Risikobewertung")
        fig_pie = px.pie(
            st.session_state.projects,
            names="Risiko",
            color="Risiko",
            color_discrete_map={
                "Niedrig": "#2ecc71",
                "Mittel": "#f1c40f",
                "Hoch": "#e74c3c",
            },
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# 📄 ANGEBOTSERSTELLUNG
# ==========================================
elif menu == "📄 Angebotserstellung":
    st.title("📄 Smarte Angebotserstellung")
    st.subheader("Erstelle kalkulierte Angebote für Ausschreibungen in Minuten")

    with st.form("quote_form"):
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input(
                "Projektname / Bauvorhaben", placeholder="z.B. Wohnpark Alster"
            )
            client = st.text_input(
                "Auftraggeber", placeholder="z.B. Stadtentwicklungs GmbH"
            )
        with col2:
            square_meters = st.number_input(
                "Geplante Fläche (in m²)", min_value=10, value=500
            )
            building_type = st.selectbox(
                "Bauart", ["Wohnungsbau", "Gewerbebau", "Infrastruktur"]
            )

        st.markdown("#### Kostenfaktoren kalkulieren")
        c1, c2, c3 = st.columns(3)
        material_cost = c1.number_input("Materialkosten pro m² (€)", value=150)
        labor_hours = c2.number_input("Geschätzte Arbeitsstunden", value=1200)
        hourly_rate = c3.number_input("Stundensatz ø (€)", value=65)

        submit_quote = st.form_submit_button("💼 Angebot kalkulieren & generieren")

    if submit_quote:
        total_material = square_meters * material_cost
        total_labor = labor_hours * hourly_rate
        subtotal = total_material + total_labor
        margin = subtotal * 0.15  # 15% SaaS Marge berechnet
        total_price = subtotal + margin

        st.success("🎉 Angebot erfolgreich kalkuliert!")

        # SaaS Vibe Rechnungs-Vorschau
        st.markdown(f"""
        ### 📋 Angebotsübersicht: **{project_name}**
        **Kunde:** {client} | **Typ:** {building_type}
        
        | Posten | Berechnung | Summe |
        | :--- | :--- | :--- |
        | **Materialkosten** | {square_meters} m² x {material_cost}€ | **{total_material:,.2f} €** |
        | **Personalkosten** | {labor_hours} Std. x {hourly_rate}€ | **{total_labor:,.2f} €** |
        | **Risiko- & Gewinnmarge** | 15% Overhead | **{margin:,.2f} €** |
        | 🏢 **Gesamtangebotssumme (netto)** | | **{total_price:,.2f} €** |
        """)

# ==========================================
# 📐 BAUPLAN-FREIGABEN
# ==========================================
elif menu == "📐 Bauplan-Freigaben":
    st.title("📐 Digitale Bauplan-Freigaben")
    st.subheader("Vermeide teure Fehler durch strukturierte Freigabeketten")

    # File Uploader
    uploaded_file = st.file_uploader(
        "Neuen Bauplan hochladen (PDF, DWG, PNG)", type=["pdf", "png", "jpg"]
    )
    if uploaded_file:
        st.info(
            f"Datei '{uploaded_file.name}' hochgeladen. KI scannt nach Formatfehlern..."
        )
        st.success(
            "KI-Prüfung bestanden: Keine statischen Konflikte im Text-Layer gefunden."
        )

    st.markdown("---")
    st.markdown("### Aktuelle Pläne im Prüfzyklus")

    # Mock Workflow Table
    plan_data = pd.DataFrame(
        [
            {
                "Plan-ID": "PL-082",
                "Gewerk": "Rohbau",
                "Version": "v2.1",
                "Prüfer": "Dr. M. Weber (Statiker)",
                "Status": "Wartet auf Freigabe",
            },
            {
                "Plan-ID": "PL-085",
                "Gewerk": "Elektro",
                "Version": "v1.0",
                "Prüfer": "Dipl.-Ing. Sarah König",
                "Status": "Freigegeben",
            },
            {
                "Plan-ID": "PL-089",
                "Gewerk": "Sanitär",
                "Version": "v1.4",
                "Prüfer": "T. Kraft (Bauleiter)",
                "Status": "Abgewiesen (Revision nötig)",
            },
        ]
    )

    for idx, row in plan_data.iterrows():
        with st.expander(f"{row['Plan-ID']} - {row['Gewerk']} ({row['Status']})"):
            st.write(
                f"**Version:** {row['Version']} | **Zuständiger Prüfer:** {row['Prüfer']}"
            )
            if row["Status"] == "Wartet auf Freigabe":
                c1, c2 = st.columns(2)
                if c1.button("🟢 Plan jetzt freigeben", key=f"app_{idx}"):
                    st.success("Plan freigegeben! Bauleiter wurde benachrichtigt.")
                if c2.button("🔴 Plan abweisen", key=f"rej_{idx}"):
                    st.error("Plan abgewiesen. Benachrichtigung zur Revision gesendet.")

# ==========================================
# 🚜 MASCHINENVERMIETUNG
# ==========================================
elif menu == "🚜 Maschinenvermietung":
    st.title("🚜 Interner Fuhrpark- & Mietmanager")
    st.subheader(
        "Optimiere die Auslastung deiner Maschinen über alle Baustellen hinweg"
    )

    st.dataframe(st.session_state.machinery, use_container_width=True)

    st.markdown("### ⚡ Express-Buchung für Baustelle")
    with st.form("rent_form"):
        selected_machine = st.selectbox(
            "Verfügbare Maschine wählen",
            st.session_state.machinery[
                st.session_state.machinery["Status"] == "Verfügbar"
            ]["Gerät"],
        )
        target_project = st.selectbox(
            "Ziel-Baustelle", st.session_state.projects["Projekt"]
        )
        days = st.slider("Mietdauer (Tage)", 1, 30, 5)

        submit_rent = st.form_submit_button("Maschine anfordern")
        if submit_rent:
            st.success(
                f"Erfolgreich gebucht! {selected_machine} wird für {days} Tage an das Projekt '{target_project}' überstellt."
            )

# ==========================================
# ⏱️ ZEITERFASSUNG
# ==========================================
elif menu == "⏱️ Zeiterfassung":
    st.title("⏱️ Mitarbeiter-Zeiterfassung")
    st.subheader("Digitales Stechkarten-System für die Kolonnen auf dem Bau")

    col1, col2, col3 = st.columns(3)
    worker = col1.text_input("Name des Mitarbeiters", placeholder="z.B. Max Mustermann")
    project = col2.selectbox("Baustelle", st.session_state.projects["Projekt"])
    hours = col3.number_value = st.number_input(
        "Gearbeitete Stunden", min_value=0.5, max_value=16.0, value=8.0, step=0.5
    )

    activity = st.selectbox(
        "Tätigkeit",
        [
            "Rohbau / Maurerarbeiten",
            "Betonieren",
            "Estrich",
            "Verkabelung",
            "Projektleitung/Pause",
        ],
    )

    if st.button("⏱️ Zeitbuchung loggen"):
        st.success(
            f"Erfolgreich erfasst: {worker} hat {hours} Stunden auf '{project}' für '{activity}' gebucht. (GPS-Verifizierung: OK)"
        )

# ==========================================
# 🧠 KI-RISIKO-VORHERSAGE (Jetzt mit Groq API!)
# ==========================================
elif menu == "🧠 KI-Risiko-Vorhersage":
    st.title("🧠 KI-gestützte Verzögerungsvorhersage")
    st.subheader("Real-Time Predictive Analytics via Groq Llama 3")

    # Prüfen, ob der API Key vorhanden ist
    if "GROQ_API_KEY" not in st.secrets:
        st.error(
            "🔑 Groq API Key nicht gefunden! Bitte füge ihn in den Streamlit Secrets oder in .streamlit/secrets.toml hinzu."
        )
    else:
        from groq import Groq

        # Groq Client initialisieren
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        st.info(
            "Das KI-Modell analysiert Ihre Eingaben und generiert eine professionelle SaaS-Risikoanalyse."
        )

        # Inputs für die API
        st.markdown("### 📊 Aktuelle Projektparameter")
        c1, c2 = st.columns(2)
        with c1:
            selected_proj = st.selectbox(
                "Zu analysierendes Projekt", st.session_state.projects["Projekt"]
            )
            weather_days = st.slider(
                "Erwartete Schlechtwetter-Tage (nächste 30 Tage)", 0, 30, 5
            )
        with c2:
            material_status = st.select_slider(
                "Lieferketten-Status (Material)",
                options=["Optimal", "Leichte Verzögerung", "Kritischer Engpass"],
            )
            staff_quota = st.slider("Aktuelle Krankheitsquote im Team (%)", 0, 40, 8)

        if st.button("🧠 KI-Analyse via Groq starten"):
            with st.spinner("Verbinde mit Groq-Clustern... Generiere Vorhersage..."):
                try:
                    # Prompt für die Bau-KI
                    prompt = f"""
                    Du bist die integrierte KI eines Enterprise Vertical SaaS für die Baubranche.
                    Analysiere folgendes Szenario für das Projekt '{selected_proj}':
                    - Erwartete Schlechtwetter-Tage: {weather_days}
                    - Lieferketten-Status: {material_status}
                    - Krankheitsquote: {staff_quota}%
                    
                    Gib eine strukturierte Antwort im Markdown-Format zurück:
                    1. **Risiko-Score (in %)**: Eine geschätzte Zahl von 0 bis 100%.
                    2. **Hauptursache**: Welcher Faktor wiegt am schwersten?
                    3. **SaaS-Handlungsempfehlung**: 2-3 konkrete, knappe Schritte für den Bauleiter, um die Verzögerung abzuwenden.
                    Antworte im professionellen, prägnanten B2B-SaaS-Stil.
                    """

                    # API Call an Groq
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "Du bist ein präzises KI-Modell für Bau-Projektmanagement-Risikoanalysen.",
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                        model="llama3-8b-8192",
                        temperature=0.2,  # Niedrige Temp für konsistente Business-Antworten
                    )

                    # Ergebnis anzeigen
                    st.markdown("---")
                    st.markdown("### 🔮 Live-KI-Prognose")
                    st.success("Analyse erfolgreich abgeschlossen!")
                    st.markdown(chat_completion.choices[0].message.content)

                except Exception as e:
                    st.error(f"Fehler beim Aufruf der Groq API: {e}")
