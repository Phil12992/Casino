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
            user, hashed = line.strip().split(":")
            if user == name and hashed == hash_passwort(passwort):
                return True
    return False

def registrieren(name, passwort):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w"): pass
    with open("users.txt", "r") as f:
        for line in f:
            user, _ = line.strip().split(":")
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

# ==== SPIELE ====
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
            st.write(f"Du hast eine **{wurf}** geworfen.")
            if wurf == 6:
                st.success("Jackpot! +5 Punkte")
                st.session_state.punkte += 5
            elif wurf == 1:
                st.warning("-2 Punkte")
                st.session_state.punkte -= 2
            else:
                st.info("+1 Punkt")
                st.session_state.punkte += 1

    elif spiel == "🪙 Münzwurf":
        if st.button("🪙 Münze werfen"):
            ergebnis = choice(["Kopf", "Zahl"])
            st.write(f"Die Münze zeigt: **{ergebnis}**")
            if ergebnis == "Kopf":
                st.session_state.punkte += 2
                st.success("+2 Punkte")
            else:
                st.session_state.punkte -= 1
                st.error("-1 Punkt")

    elif spiel == "🎰 Slot Maschine":
        if st.button("🎰 Drehen"):
            symbole = ["🍒", "🍋", "🔔", "⭐", "💎"]
            spalte = [choice(symbole) for _ in range(3)]
            st.write(f"{' | '.join(spalte)}")
            if len(set(spalte)) == 1:
                st.balloons()
                st.session_state.punkte += 10
                st.success("Jackpot! +10 Punkte")
            elif len(set(spalte)) == 2:
                st.session_state.punkte += 4
                st.info("Zwei gleiche! +4 Punkte")
            else:
                st.session_state.punkte -= 3
                st.warning("Leider nichts! -3 Punkte")

    elif spiel == "💣 Bombenzahl":
        if "bombenzahl" not in st.session_state:
            st.session_state.bombenzahl = randint(1, 10)
            st.session_state.bombenzahlen = list(range(1, 11))

        if st.session_state.bombenzahlen:
            zahl = st.selectbox("Wähle eine Zahl (1–10):", st.session_state.bombenzahlen)
            if st.button("💣 Testen"):
                if zahl == st.session_state.bombenzahl:
                    st.error("💥 Boom! Du hast die Bombe getroffen!")
                    st.session_state.punkte -= 5
                    st.session_state.bombenzahlen = []
                else:
                    st.success("✅ Sicher! +1 Punkt")
                    st.session_state.punkte += 1
                    st.session_state.bombenzahlen.remove(zahl)
        else:
            if st.button("🔁 Neues Spiel starten"):
                st.session_state.bombenzahl = randint(1, 10)
                st.session_state.bombenzahlen = list(range(1, 11))
                st.rerun()

    elif spiel == "🤖 Greifautomat":
        if st.button("🤖 Start"):
            gewinn = choice([True, False, False])
            if gewinn:
                st.success("🎁 Du hast ein Geschenk gezogen! +7 Punkte")
                st.session_state.punkte += 7
            else:
                st.warning("😞 Leider leer. -2 Punkte")
                st.session_state.punkte -= 2

    elif spiel == "📊 Punktestand speichern":
        save_points(st.session_state.name, st.session_state.punkte)
        st.success("💾 Punktestand gespeichert!")

