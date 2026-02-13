import os
import streamlit as st


# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'


import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

# --- CONFIGURATION & QUESTIONS ---
QUESTIONS = [
    {"question": "Wie nennt man eine Handlung, die verpflichtend ist (Belohnung bei Ausführung, Strafe bei Unterlassung)?", "options": ["Mustahabb", "Mubah", "Wajib", "Makruh"], "answers": ["Wajib"]},
    {"question": "Was bedeutet der Begriff 'Mubah'?", "options": ["Eine verpönte Handlung", "Eine völlig neutrale Handlung", "Eine streng verbotene Handlung", "Eine empfohlene Handlung"], "answers": ["Eine völlig neutrale Handlung"]},
    # {"question": "Welche dieser Urteile gehören zu den 'wad'iyya' (situativen) Urteilen?", "options": ["Haram", "Shart (Bedingung)", "Sabab (Ursache)", "Wajib"], "answers": ["Shart (Bedingung)", "Sabab (Ursache)"]},
    {"question": "Was ist 'Tahara' (Reinheit)?", "options": ["Nur das Entfernen von Schmutz", "Das Entfernen von ritueller Unreinheit und Schmutz", "Nur das Waschen der Hände", "Das Tragen sauberer Kleidung"], "answers": ["Das Entfernen von ritueller Unreinheit und Schmutz"]},    {"question": "Wo ist es verboten, die Notdurft zu verrichten?", "options": ["Auf einem Weg", "In einer geschlossenen Toilette", "In nützlichem Schatten", "Unter einem fruchttragenden Baum"], "answers": ["Auf einem Weg", "In nützlichem Schatten", "Unter einem fruchttragenden Baum"]},
    {"question": "Was ist 'reinigendes Wasser' (Tahur)?", "options": ["Wasser, das durch Seife verfärbt wurde", "Wasser in seinem ursprünglichen Zustand", "Wasser, das mit Urin vermischt ist", "Wasser, das nur zum Trinken erlaubt ist"], "answers": ["Wasser in seinem ursprünglichen Zustand"]},
    {"question": "Was ist 'reines Wasser' im Gegensatz zu 'reinigendem Wasser'?", "options": ["Wasser, das durch etwas Reines verändert wurde", "Wasser in seinem ursprünglichen Zustand", "Wasser, das mit Schmutz vermischt ist", "Wasser aus dem Meer"], "answers": ["Wasser, das durch etwas Reines verändert wurde"]},
    {"question": "Ab welcher Menge gilt Wasser als 'große Menge'?", "options": ["Mehr als 50 Liter", "Mehr als zwei Qullat (ca. 191,25 Liter)", "Genau 100 Liter", "Sobald es in einem Eimer ist"], "answers": ["Mehr als zwei Qullat (ca. 191,25 Liter)"]},
    {"question": "Gefäße aus welchen Materialien dürfen im Islam NICHT verwendet werden?", "options": ["Holz und Stein", "Glas und Plastik", "Gold und Silber", "Kupfer und Eisen"], "answers": ["Gold und Silber"]},
    {"question": "Was ist 'Istinja'?", "options": ["Das Gebet in der Nacht", "Die Reinigung der Privatteile nach der Notdurft", "Das Waschen der Haare", "Die rituellen Waschungen vor dem Essen"], "answers": ["Die Reinigung der Privatteile nach der Notdurft"]},
    {"question": "Was ist eine obligatorische Handlung (Pflicht) zu Beginn des Wudu?", "options": ["Das Waschen der Füße", "Die Nennung des Namens Allahs (Basmala)", "Das dreimalige Waschen der Ohren", "Das Kämmen der Haare"], "answers": ["Die Nennung des Namens Allahs (Basmala)"]},
    {"question": "Wie viele Säulen (Arkan) hat der Wudu laut dem Text?", "options": ["4", "6", "8", "10"], "answers": ["6"]},
    {"question": "Welche gehören zu den Säulen des Wudu?", "options": ["Das Waschen des Gesichts", "Das Abwischen des Kopfes", "Das Tragen sauberer Kleidung", "Die Reihenfolge"], "answers": ["Das Waschen des Gesichts", "Das Abwischen des Kopfes", "Die Reihenfolge"]},
    {"question": "Was macht die rituelle Waschung (Wudu) NICHT ungültig?", "options": ["Verlust des Bewusstseins", "Leichter Schlaf im Stehen", "Das Berühren der Genitalien", "Apostasie"], "answers": ["Leichter Schlaf im Stehen"]},    {"question": "Wann ist das rituelle Ganzkörperbad (Ghusl) verpflichtend?", "options": ["Nach dem Tod (außer bei Märtyrern)", "Nach jedem Schlaf", "Austritt von Menstruationsblut", "Nach dem Verzehr von Fleisch"], "answers": ["Nach dem Tod (außer bei Märtyrern)", "Austritt von Menstruationsblut"]},
    {"question": "Für wen ist das Gebet (Salah) NICHT verpflichtend?", "options": ["Für Reisende", "Für kranke Menschen", "Für menstruierende Frauen", "Für arme Menschen"], "answers": ["Für menstruierende Frauen"]},
    {"question": "Was gehört zu den Bedingungen für die Gültigkeit des Gebets?", "options": ["Reinheit von rituellen Unreinheiten", "Eintritt der Gebetszeit", "Bedeckung der Awrah", "Das Tragen weißer Kleidung"], "answers": ["Reinheit von rituellen Unreinheiten", "Eintritt der Gebetszeit", "Bedeckung der Awrah"]},
    {"question": "Wie viele Säulen (Arkan) hat das Gebet?", "options": ["5", "10", "14", "17"], "answers": ["14"]},
    {"question": "Was gehört zu den Pflichten (Wajibat) des Gebets?", "options": ["Das laute Lesen des Imams", "Das Sagen von 'Subhana Rabbiyal A'la' in der Niederwerfung", "Das Tragen weißer Kleidung", "Das Schließen der Augen"], "answers": ["Das Sagen von 'Subhana Rabbiyal A'la' in der Niederwerfung"]},
    {"question": "Wodurch wird der Beginn des Ramadan festgelegt?", "options": ["Durch den Kalender", "Durch die Sichtung des Neumonds", "Durch die Entscheidung des Lehrers", "Durch das Wetter"], "answers": ["Durch die Sichtung des Neumonds"]},
    {"question": "Wer muss laut Text NICHT fasten, sollte aber stattdessen einen Armen speisen?", "options": ["Kinder unter 10 Jahren", "Menschen mit einer unheilbaren Krankheit", "Menschen, die keine Lust zum Fasten haben", "Sportler während eines Wettkampfs"], "answers": ["Menschen mit einer unheilbaren Krankheit"]},
    {"question": "Welche Handlung macht das Fasten UNGÜLTIG, wenn sie vorsätzlich geschieht?", "options": ["Das Schlucken von Speichel", "Wenn Staub unbeabsichtigt in den Hals gelangt", "Sich selbst zum Erbrechen bringen", "Das Benutzen von Wasser zum Mundspülen"], "answers": ["Sich selbst zum Erbrechen bringen"]}
]

CONFIG_FILE = "test_config.json"

def load_test_status():
    """Load test open/closed status from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get("test_open", False)
    return False

def save_test_status(status):
    """Save test open/closed status to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"test_open": status}, f)

def main():
    st.set_page_config(page_title="Quranschule Quiz", page_icon="🌙")

    # Initialize session state
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "student_name" not in st.session_state:
        st.session_state.student_name = ""

    menu = st.sidebar.selectbox("Menü", ["Quiz", "Admin Bereich"])

    if menu == "Quiz":
        show_quiz()
    else:
        show_admin()

def show_quiz():
    # Check if test is open
    test_open = load_test_status()

    if not test_open:
        st.title("🌙 Quranschule Test")
        st.warning("⏸️ Der Test ist derzeit geschlossen. Bitte warte, bis dein Lehrer den Test öffnet.")
        st.info("Aktualisiere die Seite, um zu prüfen, ob der Test geöffnet wurde.")
        return

    st.title("🌙 Quranschule Test")
    st.write("Beantworte die 20 Fragen. Du kannst bei jeder Frage eine oder mehrere Antworten auswählen.")
    st.info("ℹ️ **Hinweis:** Wähle alle richtigen Antworten aus. Manche Fragen haben nur eine richtige Antwort, andere mehrere.")

    # Name input (only if not submitted)
    if not st.session_state.submitted:
        name = st.text_input("Dein vollständiger Name:", placeholder="Vorname Nachname", value=st.session_state.student_name)
        st.session_state.student_name = name

        if not name:
            st.warning("Bitte gib deinen Namen ein, um zu starten.")
            return
    else:
        st.success(f"Test abgeschlossen von: **{st.session_state.student_name}**")

    # Quiz questions
    if not st.session_state.submitted:
        # Active quiz mode
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(QUESTIONS):
                st.markdown(f"#### {i+1}. {q['question']}")
                selected = []
                for opt in q["options"]:
                    if st.checkbox(opt, key=f"q{i}_{opt}"):
                        selected.append(opt)
                user_answers[i] = selected
                st.write("---")

            if st.form_submit_button("Test abgeben", type="primary"):
                # Save answers to session state
                st.session_state.user_answers = user_answers
                st.session_state.submitted = True

                # Calculate score
                score = sum(1 for i, q in enumerate(QUESTIONS) if set(user_answers[i]) == set(q["answers"]))
                percent = (score / len(QUESTIONS)) * 100

                # Save to CSV
                save_result(st.session_state.student_name, score, len(QUESTIONS), percent)

                st.rerun()
    else:
        # Locked view mode - show results
        score = sum(1 for i, q in enumerate(QUESTIONS) if set(st.session_state.user_answers[i]) == set(q["answers"]))
        percent = (score / len(QUESTIONS)) * 100

        st.success(f"### 🎉 Ergebnis: {score}/{len(QUESTIONS)} richtig ({percent:.0f}%)")

        st.write("---")
        st.subheader("Deine Antworten (gesperrt)")

        # Display all questions with locked answers
        for i, q in enumerate(QUESTIONS):
            user_ans = set(st.session_state.user_answers[i])
            correct_ans = set(q["answers"])
            is_correct = user_ans == correct_ans

            # Question header with result indicator
            if is_correct:
                st.markdown(f"#### ✅ {i+1}. {q['question']}")
            else:
                st.markdown(f"#### ❌ {i+1}. {q['question']}")

            # Show all options with indicators
            for opt in q["options"]:
                is_correct_option = opt in correct_ans
                was_selected = opt in user_ans

                if is_correct_option and was_selected:
                    st.markdown(f"✅ **{opt}** *(richtig ausgewählt)*")
                elif is_correct_option and not was_selected:
                    st.markdown(f"🔵 **{opt}** *(richtig, aber nicht ausgewählt)*")
                elif not is_correct_option and was_selected:
                    st.markdown(f"❌ {opt} *(falsch ausgewählt)*")
                else:
                    st.markdown(f"⚪ {opt}")

            st.write("---")

        # Option to restart (new attempt)
        if st.button("Neuen Test starten (neue Person)"):
            st.session_state.submitted = False
            st.session_state.user_answers = {}
            st.session_state.student_name = ""
            st.rerun()

def show_admin():
    st.title("📊 Lehrer Bereich")
    password = st.text_input("Admin Passwort", type="password")

    if password == st.secrets.admin_password:
        # Test Control Section
        st.subheader("🎮 Test Steuerung")
        test_open = load_test_status()

        col1, col2 = st.columns([3, 1])
        with col1:
            if test_open:
                st.success("✅ Der Test ist derzeit **GEÖFFNET**")
            else:
                st.error("🔒 Der Test ist derzeit **GESCHLOSSEN**")

        with col2:
            if test_open:
                if st.button("🔒 Test schließen", type="secondary"):
                    save_test_status(False)
                    st.rerun()
            else:
                if st.button("✅ Test öffnen", type="primary"):
                    save_test_status(True)
                    st.rerun()

        st.write("---")

        # Results Section
        st.subheader("📈 Ergebnisse")

        if os.path.exists("results.csv"):
            df = pd.read_csv("results.csv")

            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Teilnehmer", len(df))
            with col2:
                st.metric("Durchschnitt", f"{df['Prozent'].mean():.1f}%")
            with col3:
                st.metric("Beste Note", f"{df['Prozent'].max():.0f}%")

            # Results table
            st.dataframe(df.sort_values("Prozent", ascending=False), use_container_width=True)

            # Download button
            st.download_button(
                "📥 Ergebnisse herunterladen",
                df.to_csv(index=False).encode('utf-8'),
                "ergebnisse.csv",
                "text/csv"
            )

            # Reset section
            st.write("---")
            st.subheader("⚠️ Gefahrenzone")
            confirm = st.checkbox("Ich möchte alle Statistiken unwiderruflich löschen.")
            if st.button("🗑️ Statistiken zurücksetzen", type="primary", disabled=not confirm):
                os.remove("results.csv")
                st.success("Alle Statistiken wurden gelöscht.")
                st.rerun()
        else:
            st.info("Noch keine Ergebnisse vorhanden.")
    elif password:
        st.error("❌ Falsches Passwort.")

def save_result(name, score, total, percentage):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[name, score, total, percentage, timestamp]],
                            columns=["Name", "Score", "Total", "Prozent", "Zeitpunkt"])

    if os.path.exists("results.csv"):
        df = pd.read_csv("results.csv")
        pd.concat([df, new_data], ignore_index=True).to_csv("results.csv", index=False)
    else:
        new_data.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()
