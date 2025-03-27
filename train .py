import pyautogui
import time
import webbrowser

# Uncommented code for pyautogui automation
# pyautogui.press("win")  # Open Start Menu
# time.sleep(1)  # Wait for the menu to open
# pyautogui.write("notepad")  # Type the app name
# time.sleep(1)  # Wait for results

# pyautogui.press("enter")  # Open the app
# time.sleep(1)  # Wait for the app to open
# pyautogui.write("Hello, this is a test.")  # Type some text

tokens = "today weather"  # Define the tokens variable
webbrowser.open(f"https://www.google.com/search?q={tokens}")  # Open Google search
