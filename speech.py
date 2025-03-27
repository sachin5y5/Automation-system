# # # import speech_recognition as sr
# # # import pyttsx3 
# # # import spacy
# # # r = sr.Recognizer() 
# # # # def SpeakText(command):
# # #     # Initialize the engine
# # #     # engine = pyttsx3.init()
# # #     # engine.say(command) 
# # #     # engine.runAndWait()
# # # while(1):    
# # #     try:
# # #         with sr.Microphone() as source2:
# # #             r.adjust_for_ambient_noise(source2, duration=0.2)
# # #             print("Listening....")
# # #             audio2 = r.listen(source2, timeout=5, phrase_time_limit=10)
# # #             MyText = r.recognize_google(audio2)
# # #             MyText = MyText.lower()
# # #             print("Recognized speech ", MyText)

# # #             nlp = spacy.load("en_core_web_sm")
# # #             tokens = MyText.split('\n') 
# # #             tokens = [token.lemma_ for token in nlp(MyText) if not token.is_stop]
# # #             print("Tokens:", tokens)
# # #   # Filter out common words (stop words)
 
            
# # #             # with open("recognized_speech.txt", "a") as f:
# # #             #     f.write(MyText + "\n")
# # #             # import os
# # #             # os.system('python test.py')
# # #     except sr.RequestError as e:
# # #         print("Could not request results; {0}".format(e))
# # #     except sr.UnknownValueError:
# # #         print("unknown error occurred")

# # import speech_recognition as sr
# # import pyttsx3 
# # import spacy
# # r = sr.Recognizer() 
# # nlp = spacy.load("en_core_web_sm")
# # pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure","wifi","bluetooth","airplane"]
# # arduino_keywords = ["light", "fan", "sensor", "motor", "control"]
# # entities = []  
# # while True:    
# #     try:
# #         with sr.Microphone() as source2:
# #             r.adjust_for_ambient_noise(source2, duration=0.2)
# #             print("Listening....")            
# #             audio2 = r.listen(source2, timeout=5, phrase_time_limit=10)
# #             MyText = r.recognize_google(audio2)
# #             MyText = MyText.lower()
# #             print("Recognized speech:", MyText)
# #             tokens = MyText.split('\n') 
# #             tokens = [token.text for token in nlp(MyText) if not token.is_stop]
# #             print("Tokens:", tokens)
# #             doc = nlp(MyText)
# #             entities = [(ent.text, ent.label_) for ent in doc.ents]  
# #             print("Entities:", entities)
# #             task_type = "Unknown Task"
# #             if any(keyword in MyText for keyword in arduino_keywords):
# #                 task_type = "Arduino Task"
# #             for token in tokens:
# #                 if token in pc_keywords:
# #                     task_type = "PC Task"
# #                     break
# #             print("Task Type:", task_type)  
# #             if "stop" in MyText:
# #                 print("Exiting...")
# #                 break
# #     except sr.RequestError as e:
# #         print("Could not request results; {0}".format(e))
# #     except sr.UnknownValueError:
# #         print("Unknown error occurred")

# from pc_task import SpeakText
# import speech_recognition as sr
# import pyttsx3 
# import spacy
# import os
# r = sr.Recognizer() 
# nlp = spacy.load("en_core_web_sm")
# pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure"]
# arduino_keywords = ["light", "fan", "sensor", "motor", "control"]
# entities = []  
# while True:    
#     try:
#         with sr.Microphone() as source2:
#             r.adjust_for_ambient_noise(source2, duration=0.2)
#             print("Listening....")            
#             audio2 = r.listen(source2, timeout=10, phrase_time_limit=10)  
#             MyText = r.recognize_google(audio2).strip()  
#             MyText = MyText.lower()
#             print("Recognized speech:", MyText) 
#             doc = nlp(MyText)  
#             tokens = [token.text for token in doc if not token.is_stop]
#             tokens = [token.text for token in nlp(MyText) if not token.is_stop]
#             print("Tokens:", tokens)
#             doc = nlp(MyText)
#             entities = [(ent.text, ent.label_) for ent in doc.ents]  
#             print("Entities:", entities)
#             task_type = "Unknown Task"
#             if any(keyword in MyText for keyword in arduino_keywords):
#                 task_type = "Arduino Task"
#             try:
#                 os.system('python aurdino_task.py')
#             except Exception as e:
#                 print(f"Error executing aurdino_task.py: {e}")
#             for token in tokens:
#                 if token in pc_keywords:
#                     task_type = "PC Task"
#                     SpeakText(MyText)  
#                     try:
#                         os.system('python pc_task.py') 
#                     except Exception as e:
#                         print(f"Error executing pc_task.py: {e}")
#                     print("PC Task executed successfully.")  
#                     print("PC Task executed successfully.")  
#                     break
#             print("Task Type:", task_type)  
#             if task_type == "PC Task":
#                 print("Waiting for PC Task to complete...")  
#             else:
#                 print("Listening for the next command...")  
#             if "stop" in MyText:
#                 print("Exiting...")
#                 break
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#     except sr.UnknownValueError:
#         print("Unknown error occurred, please try speaking again.")
# from pc_task import SpeakText
import speech_recognition as sr
import pyttsx3 
import spacy
import os

r = sr.Recognizer() 
nlp = spacy.load("en_core_web_sm")
pc_keywords = ["install", "update", "run", "open", "close", "search", "download", "volume", "brightness", "settings", "configure"]
arduino_keywords = ["light", "fan", "sensor", "motor", "control"]
entities = []  

while True:    
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening....")            
            audio2 = r.listen(source2, timeout=15, phrase_time_limit=10)  

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
                        exit_code = os.system('python pc_task.py') 
                        if exit_code == 0:
                            print("PC Task executed successfully.")  # Indicate task completion
                        else:
                            print("PC Task execution failed with exit code:", exit_code)
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

