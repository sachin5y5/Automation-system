import screen_brightness_control as sbc
import re
import pygetwindow as gw
import speech_recognition as sr
import pyttsx3
import spacy
import os
import webbrowser
import pyautogui
import subprocess
import json
import time
pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure"]
arduino_keywords = ["light", "fan", "sensor", "motor", "control"]
entities = []  
engine = pyttsx3.init()
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
def increase_volume(level):
    for _ in range(int(level[0]/2)):
        pyautogui.press("volumeup")
def decrease_volume(level):
    for _ in range(int(level[0]/2)):
        pyautogui.press("volumedown")
def perform_task(tokens):
    for token in tokens:
       match token:
            case "open":
                tokens.remove("open")
                tokens=" ".join(tokens)
                pyautogui.press("win")  # Open Start Menu
                time.sleep(1)  # Wait for the menu to open
                pyautogui.write(tokens)  # Type the app name
                time.sleep(1)  # Wait for the app to appear
                pyautogui.press("enter")  # Press Enter to open the app
            case "close":
                tokens.remove("close")
                tokens=" ".join(tokens)
                window=gw.getWindowsWithTitle(tokens)
                if window:
                    window[0].close()
                else:
                    print(f"No window found with title: {tokens}")
            case "search":
                tokens.remove("search")
                tokens=" ".join(tokens)
                webbrowser.open(f"https://www.google.com/search?q={tokens}")  # Open Google search
            case "volume":
                tokens.remove("volume")
                tokens=" ".join(tokens)
                level = [int(s) for s in re.findall(r'\d+', tokens)]
                if "increase" in tokens:
                    increase_volume(level)
                elif "decrease" in tokens:
                    decrease_volume(level)
                elif "mute" in tokens:
                    pyautogui.press("volumemute")
            # case "brightness":
            #     tokens.remove("brightness")
            #     tokens=" ".join(tokens)
            #     if "increase" in tokens:
            #         for _ in range(5):  # Adjust as needed
            #             pyautogui.press("brightnessup")  # Increase brightness by 10%
            #     elif "decrease" in tokens:
            #         sbc.set_brightness('10-', display=0) 
while True:
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2 ,timeout=15, phrase_time_limit=10)
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
                    try: 
                       perform_task(tokens)
                    except Exception as e:
                        print(f"Error y: {e}")
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