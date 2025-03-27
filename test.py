import speech_recognition as sr
import pyttsx3
import spacy
import os
import webbrowser
import pyautogui
import subprocess
import json
pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure"]
arduino_keywords = ["light", "fan", "sensor", "motor", "control"]
entities = []  

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load or initialize dynamic command mapping
COMMAND_FILE = "commands.json"

def load_commands():
    """Load user-defined commands from a JSON file."""
    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, "r") as file:
            return json.load(file)
    return {}

def save_command(command, action):
    """Save new command-action pairs to the JSON file."""
    commands = load_commands()
    commands[command] = action
    with open(COMMAND_FILE, "w") as file:
        json.dump(commands, file, indent=4)

def execute_command(action):
    """Execute the given system command or function."""
    if action.startswith("http"):
        webbrowser.open(action)  # Open URL
    elif "open" in action:
        os.system(action)  # Open file or application
    elif "pkill" in action or "taskkill" in action:
        os.system(action)  # Close applications
    else:
        subprocess.run(action, shell=True)  # Run general commands

# Default task actions (expandable)
DEFAULT_TASKS = {
    "open browser": "open https://www.google.com",
    "close browser": "pkill -f firefox",
    "search": "open https://www.google.com/search?q=",
    "play music": "open /path/to/music.mp3",
    "increase volume": lambda: pyautogui.press("volumeup"),
    "decrease volume": lambda: pyautogui.press("volumedown"),
    "mute": lambda: pyautogui.press("volumemute"),
    "shutdown": "shutdown now" if os.name != "nt" else "shutdown /s /t 0",
    "restart": "reboot" if os.name != "nt" else "shutdown /r /t 0",
}

def perform_task(command):
    """Dynamically execute a command based on user input."""
    commands = load_commands()
    
    # Check if command is predefined
    if command in DEFAULT_TASKS:
        action = DEFAULT_TASKS[command]
        print(f"Executing: {action}")
        speak(f"Executing {command}")
        execute_command(action if isinstance(action, str) else action())

    # Check user-defined commands
    elif command in commands:
        action = commands[command]
        print(f"Executing: {action}")
        speak(f"Executing {command}")
        execute_command(action)

    else:
        print(f"Unknown command: {command}")
        speak(f"I don't know how to {command}. Would you like to teach me?")
        teach_new_command(command)

def teach_new_command(command):
    """Teach the assistant a new command."""
    speak("Please tell me the action for this command.")
    action = input(f"Enter the system command for '{command}': ").strip()

    if action:
        save_command(command, action)
        speak(f"Got it! Now I can execute {command} using {action}")
        print(f"Saved: {command} -> {action}")
    else:
        speak("Command not saved.")

# Speech Recognition Loop
r = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2 ,timeout=15, phrase_time_limit=10)

            # Recognize Speech
            MyText = r.recognize_google(audio2).strip()  
            if not MyText.lower().startswith("gauri"):
                print("Command not recognized. Please start with 'gauri'.")
                continue
            MyText = MyText.lower()  
            print("Recognized speech:", MyText) 
            doc = nlp(MyText)  
            tokens = [token.text for token in doc if not token.is_stop and token.text != "gauri"]

            print("Tokens:", tokens)
            entities = [(ent.text, ent.label_) for ent in doc.ents]  
            print("Entities:", entities)
            task_type = "Unknown Task"
            
            if any(keyword in MyText for keyword in arduino_keywords): 
                # Execute Arduino Task if detected
                task_type = "Arduino Task"
                # try:
                #     os.system('python aurdino_task.py')
                #     print("Arduino Task executed successfully.")  # Indicate task completion
                # except Exception as e:
                #     print(f"Error executing aurdino_task.py: {e}")
            
            for token in tokens:
                if token in pc_keywords:
                    task_type = "PC Task"
                    print("Detected PC Task. Executing...")
                    # Execute PC Task if detected
                    try: 
                       perform_task(tokens)
                    except Exception as e:
                        print(f"Error executing pc_task.py: {e}")
                    break
            
            print("Task Type:", task_type)  
            if task_type == "PC Task" or task_type == "Arduino Task":
                print("Waiting for the next command...")  # Indicate readiness to listen
            else:
                print("Waiting for the next command...")  # Indicate readiness to listen

            if "stop" in MyText:
                print("Exiting...")
                break
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.WaitTimeoutError:
        print("Listening timed out; please try again.")
    except sr.UnknownValueError:
        print(" ")
