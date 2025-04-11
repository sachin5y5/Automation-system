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
pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure"]
arduino_keywords = ["light", "fan"]
entities = []  
engine = pyttsx3.init()
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")

while True:
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2 ,timeout=15, phrase_time_limit=10)
            MyText = r.recognize_google(audio2).strip()  
            # if not MyText.lower().startswith("era"):
            #     print("Command not recognized. Please start with 'era'.")
            #     continue
            MyText = MyText.lower()  
            print("Recognized speech:", MyText) 
            doc = nlp(MyText)  
            tokens = list(dict.fromkeys([token.text for token in doc if not token.is_stop and token.text != "era"]))
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
                    print("Detected PC Task. Executing testing.py...")
                    try:
                        # Pass tokens as arguments to testing.py
                        result = subprocess.run(['python', 'testing.py', *tokens], capture_output=True, text=True)
                        print("Response from testing.py:", result.stdout)
                        # Continue with further processing if needed
                    except Exception as e:
                        print(f"Error while running testing.py: {e}")
                    break
            print("Task Type:", task_type) 
            # if task_type == "PC Task" or task_type == "Arduino Task":
            #     print("Waiting for the next command...")  
            # else:
            #     print("Waiting for the next command...") 
            if "stop" in MyText:
                print("Exiting...")
                break
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.WaitTimeoutError:
        print("Listening timed out; please try again.")
    except sr.UnknownValueError:
        print(" ")