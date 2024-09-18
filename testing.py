import keyboard
import time


def run_autofly_script():
    print("Auto-Fly started. Press Ctrl+S to stop.")
    time.sleep(2)
    start_time = time.time()

    while True:
        for i in range(9):
            keyboard.press_and_release('F10')
            time.sleep(0.07)
        time.sleep(7)

        if keyboard.is_pressed('ctrl+s'):
            print("Script stopped by Ctrl+S.")
            break


if __name__ == "__main__":
    run_autofly_script()



"""

Default Probabilities for Char movement: 
f{'left': 0.126193724420191, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.126193724420191, 
'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281})

R-L 
scale 25:
{'left': 0.4, 'up_left': 0.03649635036496351, 'up_right': 0.03649635036496351, 'right': 0.4, 'up': 0.027007299270072994, 'down': 0.027007299270072994, 'down_left': 0.03649635036496351, 'down_right': 0.03649635036496351}

scale 5:
Adjusted Probabilities distribution based on predominant pattern R-L and scale 1
{'left': 0.4, 'up_left': 0.03649635036496351, 'up_right': 0.03649635036496351, 'right': 0.4, 'up': 0.027007299270072994, 'down': 0.027007299270072994, 'down_left': 0.03649635036496351, 'down_right': 0.03649635036496351}

"""
