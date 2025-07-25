import streamlit as st
from random import randint, choice
import os
import hashlib

# ==== STREAMLIT SETUP ====
st.set_page_config(page_title="🎰 Streamlit Casino", page_icon="🎲")
st.title("🎰 Willkommen im Online Casino!")

# ==== HELPER FUNKTIONEN ====
def hash_passwort(passwort):
    return hashlib.sha256(passwort.encode()).hexdigest()

def check_login(name, passwort):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            if ':' not in line:
                continue  # ungültige Zeile überspringen
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

    spiel = st.selectbox("Wähle ein Spiel:", [
        "🎲 Würfel-Spiel",
        "🪙 Münzwurf",
        "🎰 Slot Maschine",
        "💣 Bombenzahl",
        "🤖 Greifautomat",
        "📊 Punktestand speichern"
    ])

    if spiel == "🎲 Würfel-Spiel":
        if st.button("🎲 Würfeln"):
            wurf = randint(1, 6)
            st.write(f"Du hast eine **{wurf}** gewürfelt!")
            if wurf == 6:
                st.session_state.punkte += 5
                st.success("🎉 Du bekommst 5 Punkte!")
            else:
                st.session_state.punkte -= 1
                st.warning("❌ Leider nur -1 Punkt.")

    elif spiel == "🪙 Münzwurf":
        wahl = st.radio("Kopf oder Zahl?", ["Kopf", "Zahl"])
        if st.button("🪙 Werfen"):
            ergebnis = choice(["Kopf", "Zahl"])
            st.write(f"Die Münze zeigt: **{ergebnis}**")
            if wahl == ergebnis:
                st.session_state.punkte += 3
                st.success("🎉 Richtig! +3 Punkte")
            else:
                st.session_state.punkte -= 2
                st.error("❌ Falsch! -2 Punkte")

    elif spiel == "🎰 Slot Maschine":
        if st.button("🎰 Drehen"):
            symbole = ["🍒","🎟️", "🍋", "🔔", "💎"]
            ergebnis = [choice(symbole) for _ in range(3)]
            st.write(" - ".join(ergebnis))
            if len(set(ergebnis)) == 1:
                st.session_state.punkte += 5
                st.success("🎉 Jackpot! +5 Punkte")
            elif len(set(ergebnis)) == 2:
                st.session_state.punkte += 3
                st.info("✨ Zwei gleiche! +3 Punkte")
            else:
                st.session_state.punkte -= 5
                st.error("🙈 Keine Übereinstimmung. -5 Punkte")

    elif spiel == "💣 Bombenzahl":
        if "bombenzahlen" not in st.session_state:
            st.session_state.bombenzahlen = list(range(1, 11))
        bombe = 7  # Kann auch randomisiert werden, z.B. randint(1,10)
        st.write(f"Wähle eine Zahl zwischen 1 und 10 (Bombe versteckt!)")
        for zahl in st.session_state.bombenzahlen:
            if st.button(f"Zahl {zahl}"):
                if zahl == bombe:
                    st.session_state.punkte -= 10
                    st.error("💥 BOOM! Du hast die Bombe getroffen. -10 Punkte")
                    st.session_state.bombenzahlen = list(range(1, 11))
                else:
                    st.session_state.punkte += 2
                    st.success(f"✅ Glück gehabt! +2 Punkte für Zahl {zahl}")
                    st.session_state.bombenzahlen.remove(zahl)
        if not st.session_state.bombenzahlen:
            st.info("🎉 Alle Zahlen durch! Neues Spiel startet...")
            st.session_state.bombenzahlen = list(range(1, 11))

    elif spiel == "🤖 Greifautomat":
        if st.button("🤖 Greifen"):
            chance = randint(1, 5)
            if chance == 1:
                st.session_state.punkte += 15
                st.success("🎁 Du hast ein Geschenk gegriffen! +15 Punkte")
            else:
                st.session_state.punkte -= 4
                st.error("🪙 Leider leer. -4 Punkte")

    elif spiel == "📊 Punktestand speichern":
        save_points(st.session_state.name, st.session_state.punkte)
        st.success("💾 Punktestand gespeichert!")
