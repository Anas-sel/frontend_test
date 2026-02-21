import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# --- QUESTIONS ---
QUESTIONS = [
    {"question": "Was bedeutet 'Tajweed' (تجويد) auf Arabisch?", "options": ["Schnell lesen", "Verschönern und verbessern", "Auswendig lernen", "Übersetzen"]},
    {"question": "Was ist 'Makharij al-Huruf' (مخارج الحروف)?", "options": ["Die Länge der Vokale", "Die Ausspracheorte der Buchstaben", "Die Regeln des Stoppens", "Die Nasallaute"]},
    {"question": "Was bedeutet 'Nun Sakinah' (نون ساكنة)?", "options": ["Ein Nun mit Shadda (شدة)", "Ein Nun ohne Vokal (mit Sukun سكون)", "Ein Nun am Wortende", "Ein Nun mit Fatha (فتحة)"]},
    {"question": "Was ist 'Idgham' (إدغام)?", "options": ["Das Dehnen eines Buchstabens", "Das Zusammenführen/Verschmelzen zweier Buchstaben", "Das Nasalisieren eines Buchstabens", "Das Stoppen beim Lesen"]},
    {"question": "Was ist 'Ikhfa' (إخفاء)?", "options": ["Das vollständige Aussprechen des Nun (نون)", "Das vollständige Verschmelzen des Nun (نون)", "Das versteckte/teilweise Nasalisieren des Nun (نون)", "Das Umwandeln des Nun (نون) in Mim (ميم)"]},
    {"question": "Was ist 'Iqlab' (إقلاب)?", "options": ["Das Dehnen des Alif (ألف)", "Das Umwandeln des Nun Sakinah (نون ساكنة) oder Tanwin (تنوين) in ein Mim (ميم) vor dem Buchstaben Ba (باء)", "Das Verschmelzen des Lam (لام)", "Das Stoppen am Waqf (وقف)"]},
    {"question": "Was ist 'Izhar' (إظهار)?", "options": ["Das versteckte Aussprechen", "Das klare und deutliche Aussprechen des Nun Sakinah (نون ساكنة) ohne Nasalton", "Das Verschmelzen (إدغام)", "Das Umwandeln (إقلاب)"]},
    {"question": "Welche Buchstaben gehören zu den 'Izhar Halqi' (إظهار حلقي) Buchstaben?", "options": ["ب، م، و، ن", "ي، ر، م، ل، و، ن", "ء، ه، ع، ح، غ، خ", "ق، ك، ج، ش، ي"]},
    {"question": "Was ist 'Madd' (مد) im Tajweed (تجويد)?", "options": ["Das Stoppen beim Lesen", "Das Dehnen/Verlängern eines Vokals", "Das Nasalisieren (غنة Ghunna)", "Das Verschmelzen zweier Buchstaben"]},
    {"question": "Was ist der 'Madd Tabii' (مد طبيعي – natürliche Dehnung)?", "options": ["Eine Dehnung von 4-5 Harakah (حركة)", "Eine Dehnung von 2 Harakah (حركة) ohne äußeren Grund", "Eine Dehnung von 6 Harakah (حركة)", "Eine Dehnung nur am Wortende"]},
    {"question": "Was ist 'Ghunna' (غنة)?", "options": ["Ein Kehlkopflaut (حلقي Halqi)", "Der Nasalton der aus der Nase kommt, besonders bei Nun (نون) und Mim (ميم)", "Das Dehnen des Alif (ألف)", "Das Stoppen beim Lesen (وقف Waqf)"]},
    {"question": "Was ist 'Qalqalah' (قلقلة)?", "options": ["Das Dehnen eines Buchstabens (مد Madd)", "Das Vibrieren/Nachklingen bestimmter Buchstaben wenn sie Sukun (سكون) haben", "Das Nasalisieren (غنة Ghunna)", "Das Verschmelzen (إدغام Idgham)"]},
    {"question": "Welche Buchstaben gehören zur 'Qalqalah' (قلقلة)?", "options": ["ب، م، و، ن، ي ", "ق، ط، ب، ج، د ", "ء، ه، ع، ح، غ، خ ", "ل، ر، ن، م، و "]},
    #{"question": "Was ist 'Waqf' (وقف) im Tajweed (تجويد)?", "options": ["Das Beginnen der Rezitation (ابتداء Ibtida)", "Das Stoppen/Pausieren beim Lesen des Qurans", "Das Nasalisieren (غنة Ghunna)", "Das Dehnen (مد Madd)"]},
    #{"question": "Was bedeutet das Zeichen 'مـ' – 'Waqf Lazim' (وقف لازم)?", "options": ["Hier darf man stoppen (وقف جائز Waqf Jaiz)", "Hier muss man stoppen, da das Weiterlesen den Sinn verfälscht", "Hier soll man nicht stoppen (لا وقف La Waqf)", "Hier ist ein langer Madd (مد Madd)"]},
    {"question": "Was ist 'Tafkhim' (تفخيم)?", "options": ["Das dünne/leichte Aussprechen eines Buchstabens (ترقيق Tarqiq)", "Das schwere/dicke Aussprechen eines Buchstabens", "Das Nasalisieren (غنة Ghunna)", "Das Stoppen (وقف Waqf)"]},
    {"question": "Welche der folgenden Buchstaben werden immer mit 'Tafkhim' (تفخيم – schwer/dick) ausgesprochen? (Mehrere Antworten möglich)", "options": [
    "خ",
    "ص",
    "ن",
    "ض",
    ]},
    {"question": "Was ist 'Tarqiq' (ترقيق)?", "options": ["Das schwere Aussprechen (تفخيم Tafkhim)", "Das leichte/dünne Aussprechen eines Buchstabens", "Das Dehnen (مد Madd)", "Das Verschmelzen (إدغام Idgham)"]},
    {"question": "Welche der folgenden Buchstaben werden immer mit 'Tarqiq' (ترقيق – leicht/dünn) ausgesprochen? (Mehrere Antworten möglich)", "options": [
    "ص",
    "ن",
    "ب",
    "ط",
    ]},
    {"question": "Was ist 'Idgham Maal Ghunna' (إدغام مع غنة)?", "options": ["Verschmelzen ohne Nasalton (إدغام بلا غنة Idgham bila Ghunna)", "Verschmelzen mit Nasalton (غنة) bei den Buchstaben ي، ن، م، و (Ya, Nun, Mim, Waw)", "Klares Aussprechen mit Nasalton (إظهار Izhar)", "Umwandeln mit Nasalton (إقلاب Iqlab)"]},
    {"question": "Was ist 'Madd Wajib' (مد واجب)?", "options": [
        "Eine Dehnung von 2 Harakah (حركة) wenn ein Madd-Buchstabe (حرف مد) auf ein Hamza (همزة) trifft",
        "Eine Dehnung von 4 Harakah (حركة) wenn ein Madd-Buchstabe (حرف مد) auf ein Hamza (همزة) trifft",
        "Eine Dehnung von 6 Harakah (حركة) nur am Ende eines Verses (آية Ayah)",
        "Eine Dehnung von 2 Harakah (حركة) ohne besonderen Grund"
    ]},
    {"question": "Welche Buchstaben gehören zu den 'Huruf al-Idgham' (أحرف الإدغام) – den Buchstaben des Verschmelzens nach Nun Sakinah (نون ساكنة) oder Tanwin (تنوين)?", "options": [
    "ء، ه، ع، ح، غ، خ ",
    "ق، ط، ب، ج، د ",
    "ي، ر، م، ل، و، ن",
    "ب، م، و، ن",
    ]},
    # 5 counting-questions (Qur'an examples) to append to your QUESTIONS list
    {
        "question": (
            "Zähle in der Aya (آية, āyah) 104:1: «وَيْلٌ لِّكُلِّ هُمَزَةٍ لُّمَزَةٍ» "
            "wie oft Idghām (إدغام) vorkommt. "
        ),
        "options": ["0", "1", "2", "3"],
    },
    {
        "question": (
            "Zähle in der Aya (آية, āyah) 111:1: «تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ» "
            "wie oft Idghām (إدغام) vorkommt, "
        ),
        "options": ["0", "1", "2", "3"],
    },
    {
        "question": (
            "Zähle in der Aya (آية, āyah) 113:4: «وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ» "
            "wie oft Ikhfāʾ (إخفاء, ikhfāʾ) vorkommt "
        ),
        "options": ["0", "1", "2", "3"],
    },
    {
        "question": (
            "Zähle in der Aya (آية, āyah) 97:5: «سَلَـٰمٌ هِىَ حَتَّىٰ مَطْلَعِ ٱلْفَجْرِ»  "
            "wie oft Qalqalah (قلقلة, qalqalah) vorkommt "
        ),
        "options": ["0", "1", "2", "3"],
    },
    {
        "question": (
            "Zähle in der Aya (آية, āyah) 82:1: «إِذَا السَّمَاءُ انفَطَرَتْ» "
            "wie oft Madd Wājib Muttaṣil (مد واجب متصل) vorkommt "
        ),
        "options": ["0", "1", "2", "3"],
    },
    {
        "question": (
            "Welche von den folgenden Regeln findet man in dieser Aya "
            "لِإِيلَـٰفِ قُرَيْشٍ (١) إِۦلَـٰفِهِمْ رِحْلَةَ ٱلشِّتَآءِ وَٱلصَّيْفِ (٢) فَلْيَعْبُدُوا۟ رَبَّ هَـٰذَا ٱلْبَيْتِ (٣) ٱلَّذِىٓ أَطْعَمَهُم مِّن جُوعٍۢ وَءَامَنَهُم مِّنْ خَوْفٍۭ (٤) "
        ),
        "options": ["Qalqalah (قلقلة)", "Idgham (إدغام)", "Madd Wājib (مد واجب)", "Izhar (إظهار)"],
    },
]

CONFIG_FILE = "test_config.json"


def load_answers():
    """
    Load correct answers from st.secrets and resolve indices to option strings.

    Returns
    -------
    dict
        A dictionary mapping question index (int) to list of correct answer
        strings, resolved from the options list using stored indices.
    """
    raw = st.secrets["answers"]  # list of lists of indices
    return {
        i: [QUESTIONS[i]["options"][idx] for idx in indices]
        for i, indices in enumerate(raw)
    }


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


def save_result(name, score, total, percentage, answers):
    """
    Save student result summary and detailed answers to CSV files.

    Parameters
    ----------
    name : str
        Student's name.
    score : int
        Number of correct answers.
    total : int
        Total number of questions.
    percentage : float
        Score as a percentage.
    answers : dict
        Dictionary mapping question index (int) to list of selected answer strings.
    """
    ANSWERS = load_answers()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save summary to results.csv
    new_data = pd.DataFrame(
        [[name, score, total, percentage, timestamp]],
        columns=["Name", "Score", "Total", "Prozent", "Zeitpunkt"]
    )
    if os.path.exists("results.csv"):
        df = pd.read_csv("results.csv")
        pd.concat([df, new_data], ignore_index=True).to_csv("results.csv", index=False)
    else:
        new_data.to_csv("results.csv", index=False)

    # Save detailed answers to answers.csv
    rows = []
    for i, q in enumerate(QUESTIONS):
        user_ans = answers.get(i, [])
        correct_ans = ANSWERS[i]
        is_correct = set(user_ans) == set(correct_ans)
        rows.append({
            "Name": name,
            "Frage_Nr": i + 1,
            "Frage": q["question"],
            "Antwort": ", ".join(user_ans) if user_ans else "(keine)",
            "Richtige_Antwort": ", ".join(correct_ans),
            "Korrekt": "✅" if is_correct else "❌",
            "Zeitpunkt": timestamp
        })
    new_answers = pd.DataFrame(rows)
    if os.path.exists("answers.csv"):
        df = pd.read_csv("answers.csv")
        pd.concat([df, new_answers], ignore_index=True).to_csv("answers.csv", index=False)
    else:
        new_answers.to_csv("answers.csv", index=False)


# --- PAGE CONFIG ---
st.set_page_config(page_title="Quranschule Quiz", page_icon="🌙")

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("🌙 Quranschule – Tajweed Test")

# --- CHECK TEST STATUS ---
if not load_test_status():
    st.warning("⏸️ Der Test ist derzeit geschlossen. Bitte warte auf die Freigabe durch den Lehrer.")
    st.stop()

# --- STEP 1: Name Input ---
if not st.session_state.student_name:
    st.write("Willkommen zum Tajweed-Test! Beantworte die Fragen so gut du kannst. 🌟")
    st.info("ℹ️ **Hinweis:** Wähle alle richtigen Antworten aus. Manche Fragen haben nur eine richtige Antwort, andere mehrere.")
    name_input = st.text_input("Dein vollständiger Name:", placeholder="Vorname Nachname")
    if st.button("Test starten", type="primary"):
        if name_input.strip():
            st.session_state.student_name = name_input.strip()
            st.rerun()
        else:
            st.warning("Bitte gib deinen Namen ein.")
    st.stop()

# --- STEP 2: Quiz Form ---
if not st.session_state.submitted:
    st.write(f"Hallo **{st.session_state.student_name}**, viel Erfolg! 🌟")
    st.info("ℹ️ Wähle alle richtigen Antworten aus. Manche Fragen haben nur eine richtige Antwort, andere mehrere.")

    with st.form("quiz_form"):
        current_answers = {}
        for i, q in enumerate(QUESTIONS):
            st.markdown(f"#### {i+1}. {q['question']}")
            selected = []
            for opt in q["options"]:
                if st.checkbox(str(opt), key=f"q{i}_{opt}"):
                    selected.append(str(opt))
            current_answers[i] = selected
            st.write("---")

        if st.form_submit_button("✅ Test abgeben", type="primary"):
            ANSWERS = load_answers()
            st.session_state.user_answers = current_answers
            st.session_state.submitted = True
            score = sum(
                1 for i in range(len(QUESTIONS))
                if set(current_answers[i]) == set(ANSWERS[i])
            )
            st.session_state.score = score
            percent = (score / len(QUESTIONS)) * 100
            save_result(
                st.session_state.student_name,
                score,
                len(QUESTIONS),
                percent,
                current_answers
            )
            st.rerun()

# --- STEP 3: Results (locked) ---
else:
    ANSWERS = load_answers()
    score = st.session_state.score
    total = len(QUESTIONS)
    percent = (score / total) * 100

    st.success(f"Test abgeschlossen von: **{st.session_state.student_name}**")
    st.success(f"### 🎉 Ergebnis: {score}/{total} richtig ({percent:.0f}%)")
    st.write("---")
    st.subheader("Deine Antworten (gesperrt)")

    for i, q in enumerate(QUESTIONS):
        user_ans = set(st.session_state.user_answers.get(i, []))
        correct_ans = set(ANSWERS[i])
        is_correct = user_ans == correct_ans

        st.markdown(f"#### {'✅' if is_correct else '❌'} {i+1}. {q['question']}")
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

    if st.button("🔄 Neuen Test starten (neue Person)"):
        st.session_state.submitted = False
        st.session_state.user_answers = {}
        st.session_state.student_name = ""
        st.session_state.score = 0
        st.rerun()
