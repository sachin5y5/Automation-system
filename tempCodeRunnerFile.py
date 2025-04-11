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
            # case "brightness":
            #     tokens.remove("brightness")
            #     tokens=" ".join(tokens)
            #     if "increase" in tokens:
            #         for _ in range(5):  # Adjust as needed
            #             pyautogui.press("brightnessup")  # Increase brightness by 10%
            #     elif "decrease" in tokens:
            #         sbc.set_brightness('10-', display=0) 