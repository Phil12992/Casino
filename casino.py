import streamlit as st
from random import randint
import os

# Punktespeicherung
def load_points(name):
    if not os.path.exists("points.txt"):
        return 20
    with open("points.txt", "r") as f:
        for line in f:
            if line.startswith(name + ":"):
                return int(line.strip().split(":")[1])
    return 20

def save_points(name, punkte):
    lines = []
    gefunden = False
    if os.path.exists("points.txt"):
        with open("points.txt", "r") as f:
            for line in f:
                if line.startswith(name + ":"):
                    lines.append(f"{name}: {punkte}\n")
                    gefunden = True
                else:
                    lines.append(line)
    if not gefunden:
        lines.append(f"{name}: {punkte}\n")
    with open("points.txt", "w") as f:
        f.writelines(lines)

# Streamlit UI
st.set_page_config(page_title="🎰 Online Casino", page_icon="🎲", layout="centered")
st.title("🎰 Willkommen im Online-Casino!")

name = st.text_input("🧑 Bitte gib deinen Namen ein:", key="name_input")

if name:
    if "punkte" not in st.session_state:
        st.session_state.punkte = load_points(name)

    st.success(f"Hallo {name}, du hast aktuell {st.session_state.punkte} Punkte.")

    spiel = st.radio("🎮 Wähle dein Spiel:", [
        "Würfel-Spiel 🎲",
        "Münzwurf 🪙",
        "Slot Maschine 🎰",
        "Bombenzahl 💣",
        "Greifautomat 🤖",
        "Punktestand anzeigen 📊"
    ])

    st.markdown("---")

    if spiel == "Würfel-Spiel 🎲":
        st.session_state.punkte -= 1
        save_points(name, st.session_state.punkte)
        zahl1 = st.number_input("Wähle eine Zahl von 1 bis 6", 1, 6, step=1)
        if st.button("🎲 Würfeln!"):
            ergebnis = [randint(1, 6) for _ in range(6)]
            anzahl = ergebnis.count(int(zahl1))
            if anzahl == 0:
                p1 = 0
            elif anzahl < 4:
                p1 = 1
            elif anzahl < 6:
                p1 = 2
            else:
                p1 = 5
            st.session_state.punkte += p1
            save_points(name, st.session_state.punkte)
            st.info(f"🎯 Geworfen: {ergebnis}")
            st.success(f"Die Zahl {zahl1} kam {anzahl}x vor → +{p1} Punkte")

    elif spiel == "Münzwurf 🪙":
        st.session_state.punkte -= 1
        save_points(name, st.session_state.punkte)
        wahl = st.radio("Kopf oder Zahl?", ["Kopf", "Zahl"])
        if st.button("🪙 Münze werfen"):
            ergebnis = randint(1, 2)
            ergebnis_text = "Kopf" if ergebnis == 1 else "Zahl"
            if wahl == ergebnis_text:
                st.session_state.punkte += 1
                st.success(f"✅ Die Münze zeigt {ergebnis_text}. Du gewinnst 1 Punkt!")
            else:
                st.warning(f"❌ Die Münze zeigt {ergebnis_text}. Leider kein Punkt.")
            save_points(name, st.session_state.punkte)

    elif spiel == "Slot Maschine 🎰":
        if st.button("🎰 Hebel ziehen (-2 Punkte)"):
            st.session_state.punkte -= 2
            zahlen = [randint(1, 6) for _ in range(3)]
            if zahlen[0] == zahlen[1] == zahlen[2]:
                st.session_state.punkte += 10
                st.balloons()
                st.success(f"💥 JACKPOT! Zahlen: {zahlen} → +10 Punkte")
            else:
                st.warning(f"🤏 Keine drei gleichen. Gezogene Zahlen: {zahlen}")
            save_points(name, st.session_state.punkte)

    elif spiel == "Bombenzahl 💣":
        if "bombenzahl_num" not in st.session_state:
            st.session_state.bombenzahl_num = randint(1, 10)

        zahl = st.number_input("Wähle eine Zahl zwischen 1 und 10", 1, 10, step=1)
        if st.button("💣 Entschärfen"):
            if int(zahl) == st.session_state.bombenzahl_num:
                st.session_state.punkte -= 1
                st.warning("💥 Die Bombe ist explodiert! -1 Punkt")
                st.session_state.bombenzahl_num = randint(1, 10)
            else:
                st.session_state.punkte += 1
                st.success("✅ Nicht explodiert! +1 Punkt")
            save_points(name, st.session_state.punkte)

    elif spiel == "Greifautomat 🤖":
        if "greif_x" not in st.session_state:
            st.session_state.greif_x = randint(1, 10)
            st.session_state.greif_y = randint(1, 10)
            st.session_state.greif_versuche = 3

        x = st.number_input("🕹️ Zahl für X (1–10)", 1, 10, step=1, key="x")
        y = st.number_input("🕹️ Zahl für Y (1–10)", 1, 10, step=1, key="y")

        if st.button("🤖 Greifen"):
            if int(x) == st.session_state.greif_x and int(y) == st.session_state.greif_y:
                st.session_state.punkte += 5
                st.balloons()
                st.success("🎉 Du hast das Kuscheltier gegriffen! +5 Punkte!")
                st.session_state.greif_versuche = 0
            else:
                st.session_state.greif_versuche -= 1
                st.warning(f"🧤 Verfehlt! Noch {st.session_state.greif_versuche} Versuche.")
                if st.session_state.greif_versuche == 0:
                    st.error(f"😢 Leider verloren. Richtige Position: X={st.session_state.greif_x}, Y={st.session_state.greif_y}")
            save_points(name, st.session_state.punkte)

    elif spiel == "Punktestand anzeigen 📊":
        st.metric(label="📊 Dein aktueller Punktestand", value=st.session_state.punkte)
        save_points(name, st.session_state.punkte)

