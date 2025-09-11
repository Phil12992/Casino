import streamlit as st
from random import randint, choice
import os
import hashlib

# ==== STREAMLIT SETUP ====
st.set_page_config(page_title="🎰 Streamlit Casino", page_icon="🎲")
st.title("🎰 Willkommen in der Spielehalle!")

# ==== HELPER FUNKTIONEN ====
def hash_passwort(passwort):
    return hashlib.sha256(passwort.encode()).hexdigest()

def check_login(name, passwort):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            if ':' not in line:
                continue
            user, hashed = line.strip().split(":", 1)
            if user == name and hashed == hash_passwort(passwort):
                return True
    return False

def registrieren(name, passwort):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            pass
    with open("users.txt", "r") as f:
        for line in f:
            if ':' not in line:
                continue
            user, _ = line.strip().split(":", 1)
            if user == name:
                return False
    with open("users.txt", "a") as f:
        f.write(f"{name}:{hash_passwort(passwort)}\n")
    return True

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
                    lines.append(f"{name}:{punkte}\n")
                    gefunden = True
                else:
                    lines.append(line)
    if not gefunden:
        lines.append(f"{name}:{punkte}\n")
    with open("points.txt", "w") as f:
        f.writelines(lines)

# ==== LOGIN ====
if "eingeloggt" not in st.session_state:
    st.session_state.eingeloggt = False

if not st.session_state.eingeloggt:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Registrieren"])

    with tab1:
        name = st.text_input("Benutzername")
        passwort = st.text_input("Passwort", type="password")
        if st.button("🔓 Einloggen"):
            if check_login(name, passwort):
                st.success("✅ Login erfolgreich!")
                st.session_state.name = name
                st.session_state.eingeloggt = True
                st.session_state.punkte = load_points(name)
                st.session_state.bombenzahlen = list(range(1, 11))
                st.rerun()
            else:
                st.error("❌ Falscher Benutzername oder Passwort")

    with tab2:
        neuer_name = st.text_input("Neuer Benutzername")
        neues_pw = st.text_input("Neues Passwort", type="password")
        if st.button("🆕 Konto erstellen"):
            if registrieren(neuer_name, neues_pw):
                st.success("✅ Registrierung erfolgreich! Bitte einloggen.")
            else:
                st.error("⚠️ Benutzername bereits vergeben.")

else:
    st.success(f"🎉 Eingeloggt als `{st.session_state.name}`")
    st.markdown(f"**Punktestand:** `{st.session_state.punkte}` Punkte")

    def punkte_update(neuer_wert):
        st.session_state.punkte = neuer_wert
        save_points(st.session_state.name, st.session_state.punkte)

    spiel = st.selectbox("Wähle ein Spiel:", [
        "🎲 Würfel-Spiel",
        "🪙 Münzwurf",
        "🎰 Slot Maschine",
        "💣 Bombenzahl",
        "🤖 Greifautomat",
        "🎰 Roulette",
        "📊 Punktestand speichern"
    ])

    if spiel == "🎲 Würfel-Spiel":
        if st.button("🎲 Würfeln"):
            wurf = randint(1, 6)
            st.write(f"Du hast eine **{wurf}** geworfen!")
            if wurf == 6:
                punkte_update(st.session_state.punkte + 5)
                st.success("🎉 Du bekommst 5 Punkte!")
            else:
                punkte_update(st.session_state.punkte - 1)
                st.warning("❌ Leider nur -1 Punkt.")

    elif spiel == "🪙 Münzwurf":
        wahl = st.radio("Kopf oder Zahl?", ["Kopf", "Zahl"])
        if st.button("🪙 Werfen"):
            ergebnis = choice(["Kopf", "Zahl"])
            st.write(f"Die Münze zeigt: **{ergebnis}**")
            if wahl == ergebnis:
                punkte_update(st.session_state.punkte + 3)
                st.success("🎉 Richtig! +3 Punkte")
            else:
                punkte_update(st.session_state.punkte - 2)
                st.error("❌ Falsch! -2 Punkte")

    elif spiel == "🎰 Slot Maschine":
        if st.button("🎰 Drehen"):
            symbole = ["🍒","🎟️", "🍋", "🔔", "💎"]
            ergebnis = [choice(symbole) for _ in range(3)]
            st.write(" - ".join(ergebnis))
            if len(set(ergebnis)) == 1:
                punkte_update(st.session_state.punkte + 5)
                st.success("🎉 Jackpot! +5 Punkte")
            elif len(set(ergebnis)) == 2:
                punkte_update(st.session_state.punkte + 3)
                st.info("✨ Zwei gleiche! +3 Punkte")
            else:
                punkte_update(st.session_state.punkte - 5)
                st.error("🙈 Keine Übereinstimmung. -5 Punkte")

    elif spiel == "💣 Bombenzahl":
        if "bombenzahlen" not in st.session_state:
            st.session_state.bombenzahlen = list(range(1, 11))
        bombe = 7
        st.write(f"Wähle eine Zahl zwischen 1 und 10 (Bombe versteckt!)")
        for zahl in st.session_state.bombenzahlen:
            if st.button(f"Zahl {zahl}"):
                if zahl == bombe:
                    punkte_update(st.session_state.punkte - 10)
                    st.error("💥 BOOM! Du hast die Bombe getroffen. -10 Punkte")
                    st.session_state.bombenzahlen = list(range(1, 11))
                else:
                    punkte_update(st.session_state.punkte + 2)
                    st.success(f"✅ Glück gehabt! +2 Punkte für Zahl {zahl}")
                    st.session_state.bombenzahlen.remove(zahl)
        if not st.session_state.bombenzahlen:
            st.info("🎉 Alle Zahlen durch! Neues Spiel startet...")
            st.session_state.bombenzahlen = list(range(1, 11))

    elif spiel == "🤖 Greifautomat":
        if st.button("🤖 Greifen"):
            chance = randint(1, 5)
            if chance == 1:
                punkte_update(st.session_state.punkte + 15)
                st.success("🎁 Du hast ein Geschenk gegriffen! +15 Punkte")
            else:
                punkte_update(st.session_state.punkte - 4)
                st.error("🪙 Leider leer. -4 Punkte")

   elif spiel == "🎰 Roulette":
    st.subheader("🎰 Roulette-Spiel")
    bet_type = st.selectbox("Wähle deine Wette:", ["Nummer (0-36)", "Rot/Schwarz", "Gerade/Ungerade"])
    bet_value = None
    
    if bet_type == "Nummer (0-36)":
        bet_value = st.number_input("Wähle eine Zahl (0-36):", min_value=0, max_value=36, step=1)
    
    elif bet_type == "Rot/Schwarz":
        bet_value = st.radio("Rot oder Schwarz?", ["Rot", "Schwarz"])
    
    elif bet_type == "Gerade/Ungerade":
        bet_value = st.radio("Gerade oder Ungerade?", ["Gerade", "Ungerade"])
    
    if st.button("🎰 Drehen"):
        # Spin the roulette wheel (0-36)
        winning_number = randint(0, 36)
        # Determine the color and parity of the winning number
        winning_color = "Rot" if winning_number % 2 == 0 else "Schwarz"
        winning_parity = "Gerade" if winning_number % 2 == 0 else "Ungerade"
        
        st.write(f"Das Gewinnzahl ist: **{winning_number}**")
        st.write(f"Farbe: **{winning_color}**")
        st.write(f"Parität: **{winning_parity}**")

        # Check if the user's bet matches the winning number/color/parity
        if bet_type == "Nummer (0-36)" and bet_value == winning_number:
            punkte_update(st.session_state.punkte + 35)
            st.success(f"🎉 Du hast auf {winning_number} gesetzt und gewonnen! +35 Punkte")
        elif bet_type == "Rot/Schwarz" and bet_value == winning_color:
            punkte_update(st.session_state.punkte + 10)
            st.success(f"🎉 Die Farbe war {winning_color}. Du hast gewonnen! +10 Punkte")
        elif bet_type == "Gerade/Ungerade" and bet_value == winning_parity:
            punkte_update(st.session_state.punkte + 5)
            st.success(f"🎉 Die Parität war {winning_parity}. Du hast gewonnen! +5 Punkte")
        else:
            punkte_update(st.session_state.punkte - 5)
            st.error("❌ Du hast verloren. -5 Punkte")
        
        if st.button("🎰 Drehen"):
            # Spin the roulette wheel (0-36)
            winning_number = randint(0, 36)
            winning_color = "Rot" if winning_number % 2 == 0 else "Schwarz"
            winning_parity = "Gerade" if winning_number % 2 == 

