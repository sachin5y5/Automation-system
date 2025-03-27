from test import tokens
import pyttsx3
from pyspark.sql import SparkSession  

def SpeakText(command):  
    try:
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")

SpeakText(" ".join(tokens))
