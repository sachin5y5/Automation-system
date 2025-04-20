import screen_brightness_control as sbc
import subprocess
import re # impored for manipulation of string
import pygetwindow as gw # imported for controling window applications 
import speech_recognition as sr # imported for converting speech to text
import pyttsx3 #imported for text to speech
import spacy #impoerted for performing nlp fast
import os
import webbrowser
import pyautogui # imported for automate the pressing keywords
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
from ui_page import run_ui

pc_keywords = ["install", "update", "open", "close", "search", "download", "volume", "brightness"]
arduino_keywords = ["light", "fan"]
entities = []  
engine = pyttsx3.init()
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
ui_running = True  # Use a global variable to signal the UI thread

def backend_logic():
    global ui_running
    while ui_running:  # Keep listening while the UI is running
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("Listening...")
                audio2 = r.listen(source2, timeout=15, phrase_time_limit=10)
                MyText = r.recognize_google(audio2).strip()
                MyText = MyText.lower()
                print("Recognized speech:", MyText)
                
                # Process only if speech starts with "era"
                if not MyText.startswith("era"):
                    print("Speech does not start with 'era'. Ignoring...")
                    continue
                
                doc = nlp(MyText)
                tokens = list(dict.fromkeys([token.text for token in doc if not token.is_stop and token.text != "era"]))
                print("Tokens:", tokens)
                entities = [(ent.text, ent.label_) for ent in doc.ents]
                print("Entities:", entities)
                task_type = "Unknown Task"
                if any(keyword in MyText for keyword in arduino_keywords):
                    task_type = "Arduino Task"
                for token in tokens:
                    if token in pc_keywords:
                        task_type = "PC Task"
                        print("Detected PC Task. Executing pc_task.py...")
                        try:
                            # Pass tokens as arguments to pc_task.py
                            result = subprocess.run(['python', 'pc_task.py', *tokens], capture_output=True, text=True)
                            print("Response from pc_task.py:", result.stdout)
                        except Exception as e:
                            print(f"Error while running pc_task.py: {e}")
                        break
                print("Task Type:", task_type)
                if "stop" in MyText:
                    print("Exiting...")
                    ui_running = False  # Signal the UI thread to stop
                    break
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Listening timed out; please try again.")
        except sr.UnknownValueError:
            print(" ")

def run_ui_with_control():
    global ui_running
    ui_running_flag = [ui_running]  # Use a list to pass by reference
    run_ui(ui_running_flag)  # Pass the flag to the UI

if __name__ == "__main__":
    # Run the backend logic in a separate thread
    backend_thread = threading.Thread(target=backend_logic)
    backend_thread.start()

    # Run the Tkinter UI in the main thread
    run_ui_with_control()  # This should display the UI

    # Wait for the backend thread to finish
    backend_thread.join()