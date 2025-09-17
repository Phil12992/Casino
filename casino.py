import streamlit as st
import random

# Punkte persistent speichern
if 'punkte' not in st.session_state:
    st.session_state.punkte = 100

st.title("🎰 Casino App")

st.write(f"**Punkte:** {st.session_state.punkte}")

def wuerfeln(einsatz):
    wurf = random.randint(1, 6)
    st.write(f"Gewürfelt: {wurf}")
    if wurf >= 4:
        st.success(f"Du gewinnst {einsatz} Punkte!")
        st.session_state.punkte += einsatz
    else:
        st.error(f"Du verlierst {einsatz} Punkte!")
        st.session_state.punkte -= einsatz

def muenzwurf(einsatz, tipp):
    wurf = random.choice(["Kopf", "Zahl"])
    st.write(f"Münzwurf: {wurf}")
    if tipp.lower() == wurf.lower():
        st.success(f"Du gewinnst {einsatz} Punkte!")
        st.session_state.punkte += einsatz
    else:
        st.error(f"Du verlierst {einsatz} Punkte!")
        st.session_state.punkte -= einsatz

def slotmaschine(einsatz):
    symbole = ["🍒", "🍋", "🔔", "⭐"]
    auswahl = [random.choice(symbole) for _ in range(3)]
    st.write(" | ".join(auswahl))
    if len(set(auswahl)) == 1:
        gewinn = einsatz * 5
        st.success(f"Jackpot! Du gewinnst {gewinn} Punkte!")
        st.session_state.punkte += gewinn
    else:
        st.error(f"Leider nichts, du verlierst {einsatz} Punkte!")
        st.session_state.punkte -= einsatz

def bombenzahl(einsatz, tipp):
    zahl = random.randint(1, 6)
    st.write(f"Gewürfelt: {zahl}")
    if tipp == zahl:
        gewinn = einsatz * 6
        st.success(f"Treffer! Du gewinnst {gewinn} Punkte!")
        st.session_state.punkte += gewinn
    else:
        st.error(f"Leider daneben, du verlierst {einsatz} Punkte!")
        st.session_state.punkte -= einsatz

def greifautomat(einsatz):
    chance = random.randint(1, 5)
    if chance == 1:
        gewinn = einsatz * 4
        st.success(f"Gewonnen! Du bekommst {gewinn} Punkte!")
        st.session_state.punkte += gewinn
    else:
        st.error(f"Leider verloren, du verlierst {einsatz} Punkte!")
        st.session_state.punkte -= einsatz

# Auswahl des Spiels
spiel = st.selectbox("Wähle ein Spiel", ["Würfeln", "Münzwurf", "Slotmaschine", "Bombenzahl", "Greifautomat"])
einsatz = st.number_input("Einsatz", min_value=1, max_value=st.session_state.punkte, value=1)

if spiel == "Münzwurf":
    tipp = st.selectbox("Kopf oder Zahl?", ["Kopf", "Zahl"])

if spiel == "Bombenzahl":
    tipp = st.number_input("Tipp eine Zahl zwischen 1-6", min_value=1, max_value=6, value=1)

if st.button("Spielen"):
    if spiel == "Würfeln":
        wuerfeln(einsatz)
    elif spiel == "Münzwurf":
        muenzwurf(einsatz, tipp)
    elif spiel == "Slotmaschine":
        slotmaschine(einsatz)
    elif spiel == "Bombenzahl":
        bombenzahl(einsatz, tipp)
    elif spiel == "Greifautomat":
        greifautomat(einsatz)

