import streamlit as st
from random import randint
import os

# Punkte pro Spieler laden oder 20 vergeben
def load_points(name):
    if not os.path.exists("points.txt"):
        return 20
    with open("points.txt", "r") as f:
        for line in f:
            if line.startswith(name + ":"):
                return int(line.strip().split(":")[1])
    return 20

# Punktestand speichern (ersetzen, nicht anhängen)
def save_points(name, punkte):
    lines = []
    gefunden = False
    if os.path.exists("points.txt"):
        with open("points.txt", "r") as f:
            for line in f:
                if line.startswith(name + ":"):
                    lines.append(f"{name}:{punkte}\n")
                    gefunden = True
                else:
                    lines.append(line)
    if not gefunden:
        lines.append(f"{name}:{punkte}\n")
    with open("points.txt", "w") as f:
        f.writelines(lines)

# SPIELE
def bombenzahl(punkte):
    st.session_state.current_game = "bombenzahl"
    st.session_state.bpunkte = 0
    st.session_state.bombenzahl_num = randint(1, 10)

def wuerfel_spiel(punkte):
    st.session_state.punkte = punkte - 1
    st.session_state.current_game = "wuerfel"
    st.session_state.ergebnis = []
    st.session_state.zahl_gewaehlt = False

def muenzwurf(punkte):
    st.session_state.punkte = punkte - 1
    st.session_state.current_game = "muenzwurf"
    st.session_state.muenzwurf = randint(1, 2)

def slot_machine(punkte):
    st.session_state.punkte = punkte - 2
    st.session_state.current_game = "slot"
    st.session_state.zahlen = []

def greifautomaten(punkte):
    st.session_state.punkte = punkte - 1
    st.session_state.current_game = "greifautomat"
    st.session_state.x = randint(1, 10)
    st.session_state.y = randint(1, 10)
    st.session_state.versuche = 3

# Streamlit UI
st.set_page_config(page_title="Premium Casino", page_icon="🎰", layout="centered")

# CSS für Premium-Look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        color: white;
    }
    .css-1d391kg, .st-b7, .st-c0 {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B, #FF8C00);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #FF8C00, #FF4B4B);
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.1);
        color: white;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialisierung der Session State Variablen
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'punkte' not in st.session_state:
    st.session_state.punkte = 20
if 'current_game' not in st.session_state:
    st.session_state.current_game = None

# Login-Bereich
if not st.session_state.name:
    st.title("🎰 Willkommen im Premium Casino")
    name = st.text_input("Bitte gib deinen Namen ein:")
    if st.button("Spiel starten"):
        st.session_state.name = name
        st.session_state.punkte = load_points(name)
        st.experimental_rerun()
else:
    # Hauptmenü
    st.title(f"🎰 Willkommen, {st.session_state.name}!")
    st.subheader(f"Dein aktueller Punktestand: {st.session_state.punkte} Punkte")
    
    if st.session_state.current_game is None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Würfel-Spiel (-1 Punkt)"):
                wuerfel_spiel(st.session_state.punkte)
            if st.button("🪙 Münzwurf (-1 Punkt)"):
                muenzwurf(st.session_state.punkte)
            if st.button("💣 Bombenzahl (-1 Punkt)"):
                bombenzahl(st.session_state.punkte)
        with col2:
            if st.button("🎰 Slot Maschine (-2 Punkte)"):
                slot_machine(st.session_state.punkte)
            if st.button("🕹️ Greifautomaten (-1 Punkt)"):
                greifautomaten(st.session_state.punkte)
            if st.button("🏆 Punktestand speichern"):
                save_points(st.session_state.name, st.session_state.punkte)
                st.success("Punktestand gespeichert!")
            if st.button("🚪 Casino verlassen"):
                save_points(st.session_state.name, st.session_state.punkte)
                st.session_state.name = ""
                st.session_state.current_game = None
                st.experimental_rerun()
    
    # Spiellogik
    elif st.session_state.current_game == "wuerfel":
        st.subheader("🎲 Würfel-Spiel")
        if not hasattr(st.session_state, 'zahl_gewaehlt') or not st.session_state.zahl_gewaehlt:
            zahl = st.number_input("Wähle eine Zahl zwischen 1 und 6:", min_value=1, max_value=6)
            if st.button("Würfeln"):
                st.session_state.ergebnis = [randint(1, 6) for _ in range(6)]
                st.session_state.zahl_gewaehlt = True
                st.session_state.anzahl = st.session_state.ergebnis.count(zahl)
                
                if st.session_state.anzahl == 0:
                    p1 = 0
                elif st.session_state.anzahl < 4:
                    st.session_state.punkte += 1
                    p1 = 1
                elif st.session_state.anzahl < 6:
                    st.session_state.punkte += 2
                    p1 = 2
                elif st.session_state.anzahl == 6:
                    st.session_state.punkte += 5
                    p1 = 5
                
                st.session_state.punkte_gewonnen = p1
                st.experimental_rerun()
        
        if hasattr(st.session_state, 'zahl_gewaehlt') and st.session_state.zahl_gewaehlt:
            st.write(f"Würfelergebnis: {st.session_state.ergebnis}")
            st.write(f"Die gewählte Zahl wurde {st.session_state.anzahl} mal geworfen.")
            st.success(f"Du hast {st.session_state.punkte_gewonnen} Punkte gewonnen!")
            if st.button("Zurück zum Menü"):
                save_points(st.session_state.name, st.session_state.punkte)
                st.session_state.current_game = None
                st.experimental_rerun()
    
    elif st.session_state.current_game == "muenzwurf":
        st.subheader("🪙 Münzwurf")
        choice = st.radio("Wähle:", ("Kopf", "Zahl"))
        if st.button("Münze werfen"):
            if (choice == "Kopf" and st.session_state.muenzwurf == 1) or (choice == "Zahl" and st.session_state.muenzwurf == 2):
                st.session_state.punkte += 1
                st.success("Gewonnen! +1 Punkt")
            else:
                st.error("Verloren!")
            st.write("Ergebnis:", "Kopf" if st.session_state.muenzwurf == 1 else "Zahl")
            if st.button("Zurück zum Menü"):
                save_points(st.session_state.name, st.session_state.punkte)
                st.session_state.current_game = None
                st.experimental_rerun()
    
    elif st.session_state.current_game == "slot":
        st.subheader("🎰 Slot Maschine")
        if st.button("Hebel betätigen"):
            st.session_state.zahlen = [randint(1, 6) for _ in range(3)]
            if st.session_state.zahlen[0] == st.session_state.zahlen[1] == st.session_state.zahlen[2]:
                st.session_state.punkte += 10
                st.success(f"Jackpot! +10 Punkte (Zahlen: {st.session_state.zahlen})")
            else:
                st.error(f"Verloren! (Zahlen: {st.session_state.zahlen})")
        
        if st.button("Zurück zum Menü"):
            save_points(st.session_state.name, st.session_state.punkte)
            st.session_state.current_game = None
            st.experimental_rerun()
    
    elif st.session_state.current_game == "bombenzahl":
        st.subheader("💣 Bombenzahl")
        if not hasattr(st.session_state, 'bpunkte'):
            st.session_state.bpunkte = 0
        
        zahl = st.number_input("Wähle eine Zahl zwischen 1 und 10:", min_value=1, max_value=10)
        if st.button("Zahl bestätigen"):
            if zahl == st.session_state.bombenzahl_num:
                st.session_state.punkte -= 1
                st.session_state.bpunkte -= 1
                st.error("Die Bombe ist explodiert! -1 Punkt")
                st.session_state.current_game = None
                save_points(st.session_state.name, st.session_state.punkte)
                st.experimental_rerun()
            else:
                st.session_state.punkte += 1
                st.session_state.bpunkte += 1
                st.success(f"Die Bombe ist nicht explodiert! Du hast {st.session_state.bpunkte} Punkte gewonnen.")
                
                if st.button("Weiter spielen"):
                    st.experimental_rerun()
                if st.button("Beenden"):
                    save_points(st.session_state.name, st.session_state.punkte)
                    st.session_state.current_game = None
                    st.experimental_rerun()
    
    elif st.session_state.current_game == "greifautomat":
        st.subheader("🕹️ Greifautomaten")
        st.write(f"Du hast {st.session_state.versuche} Versuche übrig.")
        
        col1, col2 = st.columns(2)
        with col1:
            x = st.number_input("X-Koordinate (1-10):", min_value=1, max_value=10)
        with col2:
            y = st.number_input("Y-Koordinate (1-10):", min_value=1, max_value=10)
        
        if st.button("Versuchen"):
            st.session_state.versuche -= 1
            if x == st.session_state.x and y == st.session_state.y:
                st.session_state.punkte += 5
                st.success(f"Gewonnen! +5 Punkte (richtige Koordinaten: {st.session_state.x},{st.session_state.y})")
                if st.button("Zurück zum Menü"):
                    save_points(st.session_state.name, st.session_state.punkte)
                    st.session_state.current_game = None
                    st.experimental_rerun()
            else:
                st.error("Falsche Koordinaten!")
                if st.session_state.versuche == 0:
                    st.error(f"Keine Versuche mehr! Richtige Koordinaten: {st.session_state.x},{st.session_state.y}")
                    if st.button("Zurück zum Menü"):
                        save_points(st.session_state.name, st.session_state.punkte)
                        st.session_state.current_game = None
                        st.experimental_rerun()
