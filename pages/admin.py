import streamlit as st
import pandas as pd
import os
import json

CONFIG_FILE = "test_config.json"


def set_test_status(status):
    """
    Save the test open/closed status to the config file.

    Parameters
    ----------
    status : bool
        True to open the test, False to close it.
    """
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"test_open": status}, f)


def load_test_status():
    """
    Load the current open/closed status of the test from config file.

    Returns
    -------
    bool
        True if the test is open, False otherwise.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f).get("test_open", False)
    return False


# --- PAGE CONFIG ---
st.set_page_config(page_title="Admin – Quranschule", page_icon="👨‍🏫")
st.title("👨‍🏫 Lehrer-Bereich")

# --- PASSWORD ---
password = st.text_input("Admin-Passwort eingeben:", type="password")
if password != st.secrets["admin_password"]:
    st.error("Falsches Passwort.")
    st.stop()

st.success("✅ Zugriff gewährt.")

# --- TEST CONTROL ---
st.subheader("🔧 Test-Steuerung")
test_open = load_test_status()
status_label = "🟢 Test ist aktuell **offen**" if test_open else "🔴 Test ist aktuell **geschlossen**"
st.markdown(status_label)

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Test ÖFFNEN", use_container_width=True):
        set_test_status(True)
        st.success("Test ist jetzt offen!")
        st.rerun()
with col2:
    if st.button("🔒 Test SCHLIESSEN", use_container_width=True):
        set_test_status(False)
        st.warning("Test ist jetzt geschlossen!")
        st.rerun()

st.write("---")

# --- RESULTS OVERVIEW ---
st.subheader("📊 Ergebnisse Übersicht")

if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")

    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Teilnehmer", len(df))
    col2.metric("Durchschnitt", f"{df['Prozent'].mean():.1f}%")
    col3.metric("Beste Note", f"{df['Prozent'].max():.0f}%")

    st.dataframe(
        df.sort_values("Prozent", ascending=False).reset_index(drop=True),
        use_container_width=True
    )

    st.download_button(
        label="📥 Ergebnisse herunterladen",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ergebnisse.csv",
        mime="text/csv"
    )

    # --- PER-STUDENT ANSWER VIEW ---
    st.write("---")
    st.subheader("🔍 Antworten eines Schülers anzeigen")

    if os.path.exists("answers.csv"):
        answers_df = pd.read_csv("answers.csv")
        student_names = answers_df["Name"].unique().tolist()

        selected_student = st.selectbox(
            "Schüler auswählen:",
            ["-- Bitte auswählen --"] + student_names
        )

        if selected_student != "-- Bitte auswählen --":
            student_answers = answers_df[
                answers_df["Name"] == selected_student
            ].reset_index(drop=True)

            total = len(student_answers)
            correct = (student_answers["Korrekt"] == "✅").sum()
            percent = (correct / total * 100) if total > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Richtig", correct)
            col2.metric("Falsch", total - correct)
            col3.metric("Prozent", f"{percent:.0f}%")

            for _, row in student_answers.iterrows():
                with st.expander(f"{row['Korrekt']} Frage {row['Frage_Nr']}: {row['Frage']}"):
                    st.write(f"**Antwort des Schülers:** {row['Antwort']}")
                    st.write(f"**Richtige Antwort:** {row['Richtige_Antwort']}")
                    st.write(f"**Zeitpunkt:** {row['Zeitpunkt']}")

        st.write("---")
        st.download_button(
            label="📥 Alle Antworten herunterladen",
            data=answers_df.to_csv(index=False).encode("utf-8"),
            file_name="antworten.csv",
            mime="text/csv"
        )
    else:
        st.info("Noch keine detaillierten Antworten gespeichert.")

    # --- DANGER ZONE ---
    st.write("---")
    st.subheader("⚠️ Gefahrenzone")
    if st.checkbox("Alle Daten löschen aktivieren"):
        if st.button("🗑️ Alle Statistiken zurücksetzen", type="primary"):
            if os.path.exists("results.csv"):
                os.remove("results.csv")
            if os.path.exists("answers.csv"):
                os.remove("answers.csv")
            st.success("Alle Daten wurden gelöscht.")
            st.rerun()

else:
    st.info("Noch keine Ergebnisse vorhanden.")
