# Python Projects

A collection of small Python projects, from simple command-line games to a voice assistant that ties several of them together.

## Requirements

- Python 3.8 or newer
- Install dependencies:

```bash
pip install -r requirements.txt
```

`PyAudio` is only needed for microphone input in the voice assistant. If it fails to install on your system, the assistant still works and falls back to typed commands. The other projects only need the standard library or `requests`.

## Projects

### Voice Assistant (`Voice_assistant.py`)

The main project. A class-based desktop assistant with speech recognition, text-to-speech, and a set of commands.

```bash
python Voice_assistant.py
```

Things it can do: look things up on Wikipedia, open common sites, search the web, play music on YouTube, do basic calculations, save and read notes, check the weather, tell the time and date, tell jokes, and launch the to-do list, Rock Paper Scissors, and password generator.

If no microphone is found, it switches to typed input automatically. Notes are saved locally to `assistant_notes.json`.

It imports `Weather.py`, `To_do_list.py`, `RPS.py`, and `Password_generator.py`, so keep those files in the same folder.

### Weather (`Weather.py`)

Fetches current weather for a city using the [OpenWeatherMap](https://openweathermap.org/api) API. You need a free API key, set as an environment variable:

```bash
# macOS / Linux
export OPENWEATHER_API_KEY="your_key_here"

# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_key_here"
```

```bash
python Weather.py
```

### To-Do List (`To_do_list.py`)

A command-line task manager that saves tasks to `to_do_list.txt`. Type a command at the prompt: `add`, `remove`, `mark` (or `complete`), or `exit`.

```bash
python To_do_list.py
```

### Password Generator (`Password_generator.py`)

Generates a random password of a chosen length (minimum 4) using the `secrets` module. Every password includes at least one lowercase letter, uppercase letter, digit, and special character.

```bash
python Password_generator.py
```

### Rock Paper Scissors (`RPS.py`)

Play against the computer. Type `rock`, `paper`, or `scissors`, or `exit` to quit.

```bash
python RPS.py
```

### Guessing Game (`Guessing_game.py`)

Guess a number between 1 and 100, with "too high" and "too low" hints.

```bash
python Guessing_game.py
```

### Calculator (`Calculator.py`)

A basic calculator that takes two numbers and an operator (`+`, `-`, `*`, `/`).

```bash
python Calculator.py
```

## Notes

Generated files (`assistant_notes.json`, `to_do_list.txt`) are created in the folder where you run the programs.