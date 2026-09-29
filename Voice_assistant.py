"""
Voice Assistant
---------------
A simple desktop voice assistant with real microphone input (speech_recognition),
text-to-speech output, and a handful of useful commands.

"""

import ast
import datetime
import json
import operator
import os
import webbrowser

import pyjokes
import pyttsx3
import speech_recognition as sr
import wikipedia
from Weather import get_weather
from To_do_list import to_do_list
from RPS import RPS
from Password_generator import generate_password

NOTES_FILE = "assistant_notes.json"


class VoiceAssistant:
    def __init__(self, name="A.H", rate=175, volume=1.0, voice_index=None):
        self.name = name
        self.last_response = ""
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.audio_mode = self._init_microphone()

        # Text-to-speech engine (re-initialized per call for stability across platforms)
        self.tts_rate = rate
        self.tts_volume = volume
        self.tts_voice_index = voice_index

    # ---------- Setup ----------

    def _init_microphone(self):
        """Try to set up a microphone. Returns True if audio input is usable."""
        try:
            mic = sr.Microphone()
            with mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.microphone = mic
            return True
        except (OSError, AttributeError, sr.RequestError):
            print("No usable microphone found — falling back to typed input.\n")
            return False

    # ---------- Output ----------

    def speak(self, text):
        print(f"{self.name}: {text}")
        self.last_response = text
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.tts_rate)
            engine.setProperty("volume", self.tts_volume)
            if self.tts_voice_index is not None:
                voices = engine.getProperty("voices")
                if 0 <= self.tts_voice_index < len(voices):
                    engine.setProperty("voice", voices[self.tts_voice_index].id)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception:
            pass  # Speech output not supported on this system; text output already shown.

    # ---------- Input ----------

    def listen(self):
        """Get a command via microphone if available, otherwise via typed input."""
        if not self.audio_mode:
            return input("You (type your command): ").lower().strip()

        with self.microphone as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""

        try:
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            self.speak("Speech service is unavailable right now. Switching to typed input.")
            self.audio_mode = False
            return ""

    # ---------- Greeting ----------

    def wish_user(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good Morning!"
        elif hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        self.speak(greeting)
        self.speak(f"I am {self.name}, your voice assistant. How can I help you today?")

    # ---------- Features ----------

    def handle_password_generator(self):
        self.speak("Generating a secure password for you.")
        x = input(self.speak("Please enter the desired length of the password (minimum 4): "))
        password = generate_password(int(x))
        self.speak(f"Here is your generated password: {password}")


    def handle_rps(self):
        self.speak("Starting Rock, Paper, Scissors game.")
        RPS()

    def handle_to_do_list(self):
        self.speak("Opening your to-do list.")
        to_do_list() 

    def handle_wikipedia(self, query):
        topic = query.replace("wikipedia", "").strip()
        if not topic:
            self.speak("What would you like me to look up?")
            return
        self.speak("Searching Wikipedia...")
        try:
            result = wikipedia.summary(topic, sentences=2)
            self.speak("According to Wikipedia:")
            self.speak(result)
        except wikipedia.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            self.speak(f"That's ambiguous. Did you mean: {options}?")
        except Exception:
            self.speak("Sorry, I couldn't find anything on that.")

    def handle_open_site(self, query):
        sites = {
            "youtube": "https://www.youtube.com/",
            "google": "https://www.google.com/",
            "gmail": "https://mail.google.com/",
            "maps": "https://maps.google.com/",
            "github": "https://github.com/",
        }
        for name, url in sites.items():
            if f"open {name}" in query:
                self.speak(f"Opening {name.capitalize()}...")
                webbrowser.open(url)
                return True
        return False

    def handle_search(self, query):
        term = query.replace("search for", "").replace("search", "").strip()
        if not term:
            self.speak("What should I search for?")
            return
        self.speak(f"Searching the web for {term}...")
        webbrowser.open(f"https://www.google.com/search?q={term}")

    def handle_play_music(self, query):
        song = query.replace("play", "").strip()
        if not song:
            self.speak("What would you like me to play?")
            return
        self.speak(f"Looking for {song} on YouTube...")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    def handle_weather(self, query):
        city = (
            query.replace("what's the weather in", "")
            .replace("what is the weather in", "")
            .replace("weather in", "")
            .replace("weather", "")
            .strip()
        )
        if not city:
            city = input("Which city? ") if not self.audio_mode else None
            if not city:
                self.speak("Which city would you like the weather for?")
                city = self.listen()
        if not city:
            self.speak("I didn't catch a city name.")
            return
        self.speak(f"Checking the weather in {city}...")
        result = get_weather(city)
        self.speak(result)

    def handle_time(self):
        str_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {str_time}")

    def handle_date(self):
        str_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today's date is {str_date}")

    def handle_joke(self):
        self.speak(pyjokes.get_joke())

    def handle_calculate(self, query):
        expression = (
            query.replace("calculate", "")
            .replace("what is", "")
            .replace("what's", "")
            .strip()
        )
        try:
            result = self._safe_eval(expression)
            self.speak(f"{expression} equals {result}")
        except Exception:
            self.speak("Sorry, I couldn't calculate that.")

    @staticmethod
    def _safe_eval(expr):
        """Evaluate a basic arithmetic expression without using eval()."""
        allowed_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
                return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
                return allowed_ops[type(node.op)](_eval(node.operand))
            raise ValueError("Unsupported expression")

        tree = ast.parse(expr, mode="eval")
        return _eval(tree.body)

    def handle_note(self, query):
        content = query.replace("note", "", 1).replace("take a", "").strip()
        if not content:
            self.speak("What should I note down?")
            return
        notes = self._load_notes()
        notes.append({"text": content, "time": datetime.datetime.now().isoformat(timespec="seconds")})
        self._save_notes(notes)
        self.speak("Got it, I've saved that note.")

    def handle_read_notes(self):
        notes = self._load_notes()
        if not notes:
            self.speak("You don't have any notes yet.")
            return
        self.speak(f"You have {len(notes)} note{'s' if len(notes) != 1 else ''}.")
        for i, note in enumerate(notes, 1):
            self.speak(f"Note {i}: {note['text']}")

    @staticmethod
    def _load_notes():
        if not os.path.exists(NOTES_FILE):
            return []
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def _save_notes(notes):
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)

    def handle_repeat(self):
        if self.last_response:
            self.speak(self.last_response)
        else:
            self.speak("I haven't said anything yet.")

    # ---------- Main loop ----------

    def run(self):
        self.wish_user()
        while True:
            query = self.listen()
            if not query:
                continue

            if "wikipedia" in query:
                self.handle_wikipedia(query)
            elif "open " in query and self.handle_open_site(query):
                pass
            elif "search" in query:
                self.handle_search(query)
            elif "play" in query:
                self.handle_play_music(query)
            elif "calculate" in query or "what is" in query or "what's" in query:
                self.handle_calculate(query)
            elif "read notes" in query or "read my notes" in query:
                self.handle_read_notes()
            elif "note" in query:
                self.handle_note(query)
            elif "weather" in query:
                self.handle_weather(query)
            elif "rock paper scissors" in query or "rps" in query:
                self.handle_rps()
            elif "password" in query or "generate password" in query:
                self.handle_password_generator()    
            elif "to-do" in query or "todo" in query or "task" in query:
                self.handle_to_do_list()
            elif "time" in query:
                self.handle_time()
            elif "date" in query:
                self.handle_date()
            elif "joke" in query:
                self.handle_joke()
            elif "repeat" in query:
                self.handle_repeat()
            elif "exit" in query or "bye" in query or "quit" in query:
                self.speak("Goodbye! Have a nice day!")
                break
            else:
                self.speak("Sorry, I didn't understand that. Try again.")


if __name__ == "__main__":
    assistant = VoiceAssistant(name="Assistant")
    assistant.run()