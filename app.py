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

# Just displaying the source for the API. Remove this in your final version.
st.markdown(f"Working with {url}")

st.markdown("Now, the rest is up to you. Start creating your page.")


# TODO: Add some titles, introduction, ...


# TODO: Request user input
import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION & QUESTIONS ---
# Using the questions generated from your document
QUESTIONS = [
    {
        "question": "Wie nennt man eine Handlung, die verpflichtend ist (Belohnung bei Ausführung, Strafe bei Unterlassung)?",
        "options": ["Mustahabb", "Mubah", "Wajib", "Makruh"],
        "answer": "Wajib"
    },
    {
        "question": "Was bedeutet der Begriff 'Mubah'?",
        "options": ["Eine verpönte Handlung", "Eine völlig neutrale Handlung", "Eine streng verbotene Handlung", "Eine empfohlene Handlung"],
        "answer": "Eine völlig neutrale Handlung"
    },
    # ... (I will include a few more for the example, you can add all 20 here)
    {
        "question": "Welches dieser Urteile gehört zu den 'wad'iyya' (situativen) Urteilen?",
        "options": ["Haram", "Shart (Bedingung)", "Mustahabb", "Wajib"],
        "answer": "Shart (Bedingung)"
    }
]

def main():
    st.set_page_config(page_title="Quranschule Quiz", page_icon="🌙")

    # Sidebar for Navigation
    menu = st.sidebar.selectbox("Menü", ["Quiz", "Admin Bereich"])

    if menu == "Quiz":
        show_quiz()
    else:
        show_admin()

def show_quiz():
    st.title("🌙 Quranschule Test")
    st.write("Bitte beantworte alle Fragen sorgfältig.")

    # 1. Student Name
    name = st.text_input("Dein vollständiger Name:", placeholder="Vorname Nachname")

    if not name:
        st.warning("Bitte gib deinen Namen ein, um zu starten.")
        return

    # 2. Quiz Form
    with st.form("quiz_form"):
        user_answers = {}
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"### Frage {i+1}")
            user_answers[i] = st.radio(q["question"], q["options"], key=f"q{i}")
            st.write("---")

        submitted = st.form_submit_button("Test abgeben")

        if submitted:
            score = 0
            for i, q in enumerate(QUESTIONS):
                if user_answers[i] == q["answer"]:
                    score += 1
            
            final_score = (score / len(QUESTIONS)) * 100
            
            # Display Result to Student
            st.success(f"Fertig! {name}, du hast {score} von {len(QUESTIONS)} richtig ({final_score:.0f}%).")
            
            # SAVE DATA
            # Note: On Streamlit Cloud, local CSVs are temporary. 
            # For a one-time test, you can use st.write to log it or connect a DB.
            save_result(name, score, len(QUESTIONS))

def show_admin():
    st.title("📊 Lehrer Bereich")
    password = st.text_input("Admin Passwort", type="password")
    
    # You can set this password in your GitHub Secrets or just hardcode it for a one-time use
    if password == "quran2024": 
        st.subheader("Ergebnisse der Schüler")
        try:
            df = pd.read_csv("results.csv")
            st.dataframe(df)
            
            # Option to download as Excel/CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Ergebnisse herunterladen", csv, "ergebnisse.csv", "text/csv")
        except FileNotFoundError:
            st.info("Noch keine Ergebnisse vorhanden.")
    elif password:
        st.error("Falsches Passwort.")

def save_result(name, score, total):
    """
    Saves the result to a local CSV. 
    Warning: This will reset if the Streamlit Cloud app reboots.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[name, score, total, timestamp]], 
                            columns=["Name", "Score", "Total", "Zeitpunkt"])
    
    try:
        df = pd.read_csv("results.csv")
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()

# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package


# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON


# TODO: display the prediction in some fancy way to the user


# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page
