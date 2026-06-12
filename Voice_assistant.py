# ============================================================
#  🤖 JARVIS — Voice Assistant
#  You SPEAK → Jarvis LISTENS → Jarvis REPLIES via speaker
#
#  INSTALL THESE FIRST in VS Code terminal:
#  pip install pyttsx3 SpeechRecognition pyaudio
#
#  If pyaudio fails on Windows, run this instead:
#  pip install pipwin
#  pipwin install pyaudio
# ============================================================
"""
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import sys
import time
 
# ─── Setup Text to Speech Engine ─────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 160)       # Speed of speech
engine.setProperty('volume', 1.0)     # Volume 0.0 to 1.0
 
# Set voice — 0 = Male, 1 = Female (change as you like)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
 
# ─── Setup Microphone / Speech Recognition ───────────────────
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1       # Seconds of silence before stopping
recognizer.energy_threshold = 300    # Mic sensitivity
 
 
# ─────────────────────────────────────────────────────────────
#  SPEAK — Jarvis talks out loud
# ─────────────────────────────────────────────────────────────
def speak(text):
    print(f"\n🤖 Jarvis: {text}\n")
    engine.say(text)
    engine.runAndWait()
 
 
# ─────────────────────────────────────────────────────────────
#  LISTEN — Jarvis listens from your microphone
# ─────────────────────────────────────────────────────────────
def listen():
    with sr.Microphone() as source:
        print("🎤 Listening... (speak now)")
 
        # Adjust for background noise automatically
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
 
        try:
            # Listen — waits up to 5 seconds for speech
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("⏳ Processing your voice...")
 
            # Convert speech to text using Google
            command = recognizer.recognize_google(audio)
            print(f"\n👤 You said: {command}\n")
            return command.lower()
 
        except sr.WaitTimeoutError:
            print("⏰ No speech detected. Please try again.")
            return ""
 
        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please speak clearly.")
            return ""
 
        except sr.RequestError:
            speak("Internet connection needed for speech recognition!")
            return ""
 
        except Exception as e:
            print(f"Error: {e}")
            return ""
 
 
# ─────────────────────────────────────────────────────────────
#  GREETING — based on time of day
# ─────────────────────────────────────────────────────────────
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"
 
 
# ─────────────────────────────────────────────────────────────
#  HANDLE COMMAND — what Jarvis does based on what you say
# ─────────────────────────────────────────────────────────────
def handle_command(command):
    if not command:
        return
 
    # ── Greetings ──────────────────────────────────────────
    if any(w in command for w in ['hello', 'hi', 'hey', 'how are you']):
        speak("I am doing great! How can I help you today?")
 
    # ── Time ───────────────────────────────────────────────
    elif any(w in command for w in ['time', 'what time']):
        t = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {t}")
 
    # ── Date ───────────────────────────────────────────────
    elif any(w in command for w in ['date', 'today', 'what day']):
        d = datetime.datetime.now().strftime('%A, %B %d, %Y')
        speak(f"Today is {d}")
 
    # ── Open YouTube ───────────────────────────────────────
    elif 'youtube' in command:
        speak("Opening YouTube for you!")
        webbrowser.open("https://www.youtube.com")
 
    # ── Open WhatsApp ──────────────────────────────────────
    elif 'whatsapp' in command:
        speak("Opening WhatsApp!")
        webbrowser.open("https://web.whatsapp.com")
 
    # ── Open Google ────────────────────────────────────────
    elif 'google' in command and 'search' not in command:
        speak("Opening Google!")
        webbrowser.open("https://www.google.com")
 
    # ── Search Google ──────────────────────────────────────
    elif any(w in command for w in ['search', 'look up', 'find']):
        query = command
        for w in ['search', 'look up', 'find', 'for']:
            query = query.replace(w, '')
        query = query.strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What would you like me to search for?")
 
    # ── Wikipedia ──────────────────────────────────────────
    elif 'wikipedia' in command:
        query = command.replace('wikipedia', '').strip()
        if query:
            speak(f"Opening Wikipedia for {query}")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
        else:
            speak("What should I look up on Wikipedia?")
 
    # ── Tell a Joke ────────────────────────────────────────
    elif 'joke' in command:
        speak("Why do programmers prefer dark mode? Because light attracts bugs!")
 
    # ── Who are you ────────────────────────────────────────
    elif any(w in command for w in ['your name', 'who are you']):
        speak("I am Jarvis, your personal AI voice assistant!")
 
    # ── What can you do ────────────────────────────────────
    elif any(w in command for w in ['what can you do', 'help', 'commands']):
        speak("I can tell the time, date, search Google, open YouTube, WhatsApp, Wikipedia, and tell jokes!")
 
    # ── Thank you ──────────────────────────────────────────
    elif any(w in command for w in ['thank you', 'thanks']):
        speak("You are welcome! Anything else I can help with?")
 
    # ── Exit ───────────────────────────────────────────────
    elif any(w in command for w in ['bye', 'exit', 'quit', 'goodbye', 'stop']):
        speak("Goodbye Harsha! Have a wonderful day!")
        sys.exit(0)
 
    # ── Unknown ────────────────────────────────────────────
    else:
        speak("I am sorry, I did not understand that. Please try again!") 
 
 
# ─────────────────────────────────────────────────────────────
#  MAIN — Start Jarvis
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  🤖 JARVIS - Voice Assistant")
    print("  Speak into your microphone!")
    print("  Say 'bye' or 'exit' to stop")
    print("=" * 50)
 
    greeting = get_greeting()
    speak(f"{greeting} Harsha! I am Jarvis, your personal voice assistant. How can I help you?")
 
    # ── Main Loop — keeps listening forever ────────────────
    while True:
        command = listen()
        if command:
            handle_command(command)
        time.sleep(0.5)   # Small pause between loops
 
 
if __name__ == '__main__':
    main() 
"""
# ============================================================
#  🤖 JARVIS — Voice Assistant
#  INSTALL: pip install pyttsx3 SpeechRecognition pyaudio
# ============================================================

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import sys
import time

# ─── Setup Text to Speech Engine ─────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ─── Setup Speech Recognition ────────────────────────────────
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1
recognizer.dynamic_energy_threshold = True   # ✅ FIX 1: auto-adjusts sensitivity
recognizer.energy_threshold = 4000           # ✅ FIX 2: correct default threshold


# ─────────────────────────────────────────────────────────────
#  SPEAK
# ─────────────────────────────────────────────────────────────
def speak(text):
    print(f"\n🤖 Jarvis: {text}\n")
    engine.say(text)
    engine.runAndWait()


# ─────────────────────────────────────────────────────────────
#  LISTEN — with mic debug info
# ─────────────────────────────────────────────────────────────
def listen():
    with sr.Microphone() as source:
        print("🎤 Listening... (speak now)")

        # ✅ FIX 3: increased ambient noise calibration to 1.5 seconds
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print(f"🔊 Mic sensitivity set to: {int(recognizer.energy_threshold)}")

        try:
            # ✅ FIX 4: increased timeout and phrase limit
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            print("⏳ Processing your voice...")

            command = recognizer.recognize_google(audio)
            print(f"\n👤 You said: {command}\n")
            return command.lower()

        except sr.WaitTimeoutError:
            print("⏰ No speech detected. Please try again.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please speak clearly.")
            return ""

        except sr.RequestError:
            speak("Internet connection needed for speech recognition!")
            return ""

        except Exception as e:
            print(f"Error: {e}")
            return ""


# ─────────────────────────────────────────────────────────────
#  GREETING
# ─────────────────────────────────────────────────────────────
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


# ─────────────────────────────────────────────────────────────
#  HANDLE COMMAND
# ─────────────────────────────────────────────────────────────
def handle_command(command):
    if not command:
        return

    if any(w in command for w in ['hello', 'hi', 'hey', 'how are you']):
        speak("I am doing great! How can I help you today?")

    elif any(w in command for w in ['time', 'what time']):
        t = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {t}")

    elif any(w in command for w in ['date', 'today', 'what day']):
        d = datetime.datetime.now().strftime('%A, %B %d, %Y')
        speak(f"Today is {d}")

    elif 'youtube' in command:
        speak("Opening YouTube for you!")
        webbrowser.open("https://www.youtube.com")

    elif 'whatsapp' in command:
        speak("Opening WhatsApp!")
        webbrowser.open("https://web.whatsapp.com")

    elif 'google' in command and 'search' not in command:
        speak("Opening Google!")
        webbrowser.open("https://www.google.com")

    elif any(w in command for w in ['search', 'look up', 'find']):
        query = command
        for w in ['search', 'look up', 'find', 'for']:
            query = query.replace(w, '')
        query = query.strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What would you like me to search for?")

    elif 'wikipedia' in command:
        query = command.replace('wikipedia', '').strip()
        if query:
            speak(f"Opening Wikipedia for {query}")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
        else:
            speak("What should I look up on Wikipedia?")

    elif 'joke' in command:
        speak("Why do programmers prefer dark mode? Because light attracts bugs!")

    elif any(w in command for w in ['your name', 'who are you']):
        speak("I am Jarvis, your personal AI voice assistant!")

    elif any(w in command for w in ['what can you do', 'help', 'commands']):
        speak("I can tell the time, date, search Google, open YouTube, WhatsApp, Wikipedia, and tell jokes!")

    elif any(w in command for w in ['thank you', 'thanks']):
        speak("You are welcome! Anything else I can help with?")

    elif any(w in command for w in ['bye', 'exit', 'quit', 'goodbye', 'stop']):
        speak("Goodbye Harsha! Have a wonderful day!")
        sys.exit(0)

    else:
        speak("I am sorry, I did not understand that. Please try again!")


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  🤖 JARVIS - Voice Assistant")
    print("  Speak into your microphone!")
    print("  Say 'bye' or 'exit' to stop")
    print("=" * 50)

    # ✅ FIX 5: list available mics so you can verify yours is detected
    print("\n📋 Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {name}")
    print()

    greeting = get_greeting()
    speak(f"{greeting} Harsha! I am Jarvis, your personal voice assistant. How can I help you?")

    while True:
        command = listen()
        if command:
            handle_command(command)
        time.sleep(0.5)


if __name__ == '__main__':
    main()