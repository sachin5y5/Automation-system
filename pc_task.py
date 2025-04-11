import screen_brightness_control as sbc
import re
import pygetwindow as gw
# import speech_recognition as sr
# import pyttsx3
# import spacy
# import os
import webbrowser
import pyautogui
# import subprocess
# import json
import time
import sys
def increase_volume(level):
    for _ in range(int(level[0]/2)):
        pyautogui.press("volumeup")
def decrease_volume(level):
    for _ in range(int(level[0]/2)):
        pyautogui.press("volumedown")

def increase_brightness(level=None):
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        if level:
            new_brightness = min(max(level[0], 0), 100)  # Ensure brightness is between 0 and 100
        else:
            new_brightness = min(current_brightness + 10, 100)  # Increase by 10%, max 100%
        sbc.set_brightness(new_brightness, display=0)
        print(f"Brightness increased to {new_brightness}%")
    except Exception as e:
        print(f"Error increasing brightness: {e}")

def decrease_brightness(level=None):
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        if level:
            new_brightness = max(current_brightness - level[0], 0)  # Decrease by specified level, min 0%
        else:
            new_brightness = max(current_brightness - 10, 0)  # Decrease by 10%, min 0%
        sbc.set_brightness(new_brightness, display=0)
        print(f"Brightness decreased to {new_brightness}%")
    except Exception as e:
        print(f"Error decreasing brightness: {e}")

def perform_task(tokens):
    for token in tokens:
       match token:
            case "open":
                tokens.remove("open")
                tokens=" ".join(tokens)
                pyautogui.press("win")  
                time.sleep(1)  
                pyautogui.write(tokens)  
                time.sleep(1)  
                pyautogui.press("enter")  
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
                webbrowser.open(f"https://www.google.com/search?q={tokens}")  
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
            case "brightness":
                tokens.remove("brightness")
                tokens = " ".join(tokens)
                try:
                    level = [int(s) for s in re.findall(r'\d+', tokens)]
                    if "increase" in tokens:
                        increase_brightness(level if level else None)
                    elif "decrease" in tokens:
                        decrease_brightness(level if level else None)
                    elif level:
                        new_brightness = min(max(level[0], 0), 100)  # Ensure brightness is between 0 and 100
                        sbc.set_brightness(new_brightness, display=0)
                        print(f"Brightness set to {new_brightness}%")
                except Exception as e:
                    print(f"Error adjusting brightness: {e}")

if __name__ == "__main__":
    # Get tokens from command-line arguments
    tokens = sys.argv[1:]
    if tokens:
        perform_task(tokens)
    else:
        print("No tokens provided.")