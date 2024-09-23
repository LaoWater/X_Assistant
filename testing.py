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

################################
Auto Lvler AI Agent Version 1 ##
################################

Default Probabilities for Char movement: 
f{'left': 0.126193724420191, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.126193724420191, 
'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281})

R-L 
scale 25:
{'left': 0.4, 'up_left': 0.03649635036496351, 'up_right': 0.03649635036496351, 'right': 0.4, 'up': 0.027007299270072994, 'down': 0.027007299270072994, 'down_left': 0.03649635036496351, 'down_right': 0.03649635036496351}

scale 5:
Adjusted Probabilities distribution based on predominant pattern R-L and scale 1
{'left': 0.4, 'up_left': 0.03649635036496351, 'up_right': 0.03649635036496351, 'right': 0.4, 'up': 0.027007299270072994, 'down': 0.027007299270072994, 'down_left': 0.03649635036496351, 'down_right': 0.03649635036496351}


##########################
New Version - Scale 15: ##
##########################

Default Probabilities for Char movement: f{'left': 0.126193724420191, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.126193724420191, 'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281})

Step 1: Adjusting probabilities for predominant pattern R-L directions with scale 0.01
Adjusted probabilities: {'left': 0.12993178717598908, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.12993178717598908, 'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281}
Total Increase for Predominant Directions: 0.0074761255115961545
Step 2: Redistributing the increase (0.0074761255115961545) among non-predominant directions...
Total Probability for Non-Predominant Directions: 0.747612551159618
Step 2 Completed: Adjusted probabilities redistributed: {'left': 0.12993178717598908, 'up_left': 0.12894952251023195, 'up_right': 0.12894952251023195, 'right': 0.12993178717598908, 'up': 0.09347885402455665, 'down': 0.09347885402455665, 'down_left': 0.12894952251023195, 'down_right': 0.12894952251023195}
Step 3: Ensuring total probability sums to 1...
Total Adjusted Probability before residual adjustment: 0.9626193724420192, Residual: 0.03738062755798077
Final Adjusted Probabilities: {'left': 0.13497732426303852, 'up_left': 0.13395691609977325, 'up_right': 0.13395691609977325, 'right': 0.13497732426303852, 
'up': 0.09710884353741499, 'down': 0.09710884353741499, 'down_left': 0.13395691609977325, 'down_right': 0.13395691609977325}

##########################
New Version - Scale 25: ##
##########################

Step 1: Adjusting probabilities for predominant pattern R-L directions with scale 0.25
Adjusted probabilities: {'left': 0.21964529331514326, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.21964529331514326, 
'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281}
Total Increase for Predominant Directions: 0.18690313778990453
Step 2: Redistributing the increase (0.18690313778990453) among non-predominant directions...
Total Probability for Non-Predominant Directions: 0.747612551159618
Step 2 Completed: Adjusted probabilities redistributed: {'left': 0.21964529331514326, 'up_left': 0.06821282401091405, 'up_right': 0.06821282401091405, 'right': 0.21964529331514326, 'up': 0.0504774897680764, 'down': 0.0504774897680764, 'down_left': 0.06821282401091405, 'down_right': 0.06821282401091405}
Step 3: Ensuring total probability sums to 1...
Total Adjusted Probability before residual adjustment: 0.8130968622100956, Residual: 0.18690313778990442

Final Adjusted Probabilities: {'left': 0.27013422818791943, 'up_left': 0.08389261744966442, 'up_right': 0.08389261744966442, 'right': 0.27013422818791943, 
'up': 0.06208053691275167, 'down': 0.06208053691275167, 'down_left': 0.08389261744966442, 'down_right': 0.08389261744966442}

##########################
New Version - Scale 55: ##
##########################

Step 1: Adjusting probabilities for predominant pattern R-L directions with scale 0.55
Adjusted probabilities: {'left': 0.33178717598908597, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.33178717598908597, 'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281}
Total Increase for Predominant Directions: 0.41118690313778994
Step 2: Redistributing the increase (0.41118690313778994) among non-predominant directions...
Total Probability for Non-Predominant Directions: 0.747612551159618
Step 2 Completed: Adjusted probabilities redistributed: {'left': 0.33178717598908597, 'up_left': 0.06821282401091405, 'up_right': 0.06821282401091405, 'right': 0.33178717598908597, 'up': 0.0504774897680764, 'down': 0.0504774897680764, 'down_left': 0.06821282401091405, 'down_right': 0.06821282401091405}
Step 3: Ensuring total probability sums to 1...
Total Adjusted Probability before residual adjustment: 1.0373806275579809, Residual: -0.03738062755798088

Final Adjusted Probabilities: {'left': 0.31983166754339826, 'up_left': 0.06575486586007365, 'up_right': 0.06575486586007365, 'right': 0.31983166754339826, 
'up': 0.048658600736454505, 'down': 0.048658600736454505, 'down_left': 0.06575486586007365, 'down_right': 0.06575486586007365}

##########################
New Version - Scale 55: ##
##########################

Step 1: Adjusting probabilities for predominant pattern R-L directions with scale 0.8
Adjusted probabilities: {'left': 0.42523874488403823, 'up_left': 0.1364256480218281, 'up_right': 0.1364256480218281, 'right': 0.42523874488403823, 'up': 0.1009549795361528, 'down': 0.1009549795361528, 'down_left': 0.1364256480218281, 'down_right': 0.1364256480218281}
Total Increase for Predominant Directions: 0.5980900409276945
Step 2: Redistributing the increase (0.5980900409276945) among non-predominant directions...
Total Probability for Non-Predominant Directions: 0.747612551159618
Step 2 Completed: Adjusted probabilities redistributed: {'left': 0.42523874488403823, 'up_left': 0.06821282401091405, 'up_right': 0.06821282401091405, 'right': 0.42523874488403823, 'up': 0.0504774897680764, 'down': 0.0504774897680764, 'down_left': 0.06821282401091405, 'down_right': 0.06821282401091405}
Step 3: Ensuring total probability sums to 1...
Total Adjusted Probability before residual adjustment: 1.2242837653478855, Residual: -0.22428376534788552

Final Adjusted Probabilities: {'left': 0.34733675061288166, 'up_left': 0.05571651437486071, 'up_right': 0.05571651437486071, 'right': 0.34733675061288166, 
'up': 0.041230220637396925, 'down': 0.041230220637396925, 'down_left': 0.05571651437486071, 'down_right': 0.05571651437486071}


---------------------------------

Latest Version Distribution:
Scale: 0, Probability Distribution: 'left' = 12.6%, 'up_left' = 13.6%, 'up_right' = 13.6%, 'right' = 12.6%, 'up' = 10.1%, 'down' = 10.1%, 'down_left' = 13.6%, 'down_right' = 13.6%
Scale: 2, Probability Distribution: 'left' = 14.4%, 'up_left' = 13.1%, 'up_right' = 13.1%, 'right' = 14.4%, 'up' = 9.3%, 'down' = 9.3%, 'down_left' = 13.1%, 'down_right' = 13.1%
Scale: 4, Probability Distribution: 'left' = 16.6%, 'up_left' = 12.5%, 'up_right' = 12.5%, 'right' = 16.6%, 'up' = 8.4%, 'down' = 8.4%, 'down_left' = 12.5%, 'down_right' = 12.5%
Scale: 6, Probability Distribution: 'left' = 19.2%, 'up_left' = 11.8%, 'up_right' = 11.8%, 'right' = 19.2%, 'up' = 7.2%, 'down' = 7.2%, 'down_left' = 11.8%, 'down_right' = 11.8%
Scale: 8, Probability Distribution: 'left' = 21.7%, 'up_left' = 10.6%, 'up_right' = 10.6%, 'right' = 21.7%, 'up' = 7.0%, 'down' = 7.0%, 'down_left' = 10.6%, 'down_right' = 10.6%
Scale: 10, Probability Distribution: 'left' = 23.3%, 'up_left' = 9.7%, 'up_right' = 9.7%, 'right' = 23.3%, 'up' = 7.2%, 'down' = 7.2%, 'down_left' = 9.7%, 'down_right' = 9.7%
Scale: 12, Probability Distribution: 'left' = 23.9%, 'up_left' = 9.5%, 'up_right' = 9.5%, 'right' = 23.9%, 'up' = 7.1%, 'down' = 7.1%, 'down_left' = 9.5%, 'down_right' = 9.5%
Scale: 14, Probability Distribution: 'left' = 24.4%, 'up_left' = 9.3%, 'up_right' = 9.3%, 'right' = 24.4%, 'up' = 6.9%, 'down' = 6.9%, 'down_left' = 9.3%, 'down_right' = 9.3%
Scale: 16, Probability Distribution: 'left' = 24.9%, 'up_left' = 9.1%, 'up_right' = 9.1%, 'right' = 24.9%, 'up' = 6.8%, 'down' = 6.8%, 'down_left' = 9.1%, 'down_right' = 9.1%
Scale: 18, Probability Distribution: 'left' = 25.4%, 'up_left' = 9.0%, 'up_right' = 9.0%, 'right' = 25.4%, 'up' = 6.6%, 'down' = 6.6%, 'down_left' = 9.0%, 'down_right' = 9.0%
Scale: 20, Probability Distribution: 'left' = 25.9%, 'up_left' = 8.8%, 'up_right' = 8.8%, 'right' = 25.9%, 'up' = 6.5%, 'down' = 6.5%, 'down_left' = 8.8%, 'down_right' = 8.8%
Scale: 22, Probability Distribution: 'left' = 26.4%, 'up_left' = 8.6%, 'up_right' = 8.6%, 'right' = 26.4%, 'up' = 6.4%, 'down' = 6.4%, 'down_left' = 8.6%, 'down_right' = 8.6%
Scale: 24, Probability Distribution: 'left' = 26.8%, 'up_left' = 8.5%, 'up_right' = 8.5%, 'right' = 26.8%, 'up' = 6.3%, 'down' = 6.3%, 'down_left' = 8.5%, 'down_right' = 8.5%
Scale: 26, Probability Distribution: 'left' = 27.2%, 'up_left' = 8.3%, 'up_right' = 8.3%, 'right' = 27.2%, 'up' = 6.2%, 'down' = 6.2%, 'down_left' = 8.3%, 'down_right' = 8.3%
Scale: 28, Probability Distribution: 'left' = 27.6%, 'up_left' = 8.2%, 'up_right' = 8.2%, 'right' = 27.6%, 'up' = 6.0%, 'down' = 6.0%, 'down_left' = 8.2%, 'down_right' = 8.2%
Scale: 30, Probability Distribution: 'left' = 28.0%, 'up_left' = 8.0%, 'up_right' = 8.0%, 'right' = 28.0%, 'up' = 5.9%, 'down' = 5.9%, 'down_left' = 8.0%, 'down_right' = 8.0%
Scale: 32, Probability Distribution: 'left' = 28.4%, 'up_left' = 7.9%, 'up_right' = 7.9%, 'right' = 28.4%, 'up' = 5.8%, 'down' = 5.8%, 'down_left' = 7.9%, 'down_right' = 7.9%
Scale: 34, Probability Distribution: 'left' = 28.8%, 'up_left' = 7.7%, 'up_right' = 7.7%, 'right' = 28.8%, 'up' = 5.7%, 'down' = 5.7%, 'down_left' = 7.7%, 'down_right' = 7.7%
Scale: 36, Probability Distribution: 'left' = 29.1%, 'up_left' = 7.6%, 'up_right' = 7.6%, 'right' = 29.1%, 'up' = 5.6%, 'down' = 5.6%, 'down_left' = 7.6%, 'down_right' = 7.6%
Scale: 38, Probability Distribution: 'left' = 29.5%, 'up_left' = 7.5%, 'up_right' = 7.5%, 'right' = 29.5%, 'up' = 5.5%, 'down' = 5.5%, 'down_left' = 7.5%, 'down_right' = 7.5%
Scale: 40, Probability Distribution: 'left' = 29.8%, 'up_left' = 7.4%, 'up_right' = 7.4%, 'right' = 29.8%, 'up' = 5.5%, 'down' = 5.5%, 'down_left' = 7.4%, 'down_right' = 7.4%
Scale: 42, Probability Distribution: 'left' = 30.1%, 'up_left' = 7.3%, 'up_right' = 7.3%, 'right' = 30.1%, 'up' = 5.4%, 'down' = 5.4%, 'down_left' = 7.3%, 'down_right' = 7.3%
Scale: 44, Probability Distribution: 'left' = 30.4%, 'up_left' = 7.1%, 'up_right' = 7.1%, 'right' = 30.4%, 'up' = 5.3%, 'down' = 5.3%, 'down_left' = 7.1%, 'down_right' = 7.1%
Scale: 46, Probability Distribution: 'left' = 30.7%, 'up_left' = 7.0%, 'up_right' = 7.0%, 'right' = 30.7%, 'up' = 5.2%, 'down' = 5.2%, 'down_left' = 7.0%, 'down_right' = 7.0%
Scale: 48, Probability Distribution: 'left' = 31.0%, 'up_left' = 6.9%, 'up_right' = 6.9%, 'right' = 31.0%, 'up' = 5.1%, 'down' = 5.1%, 'down_left' = 6.9%, 'down_right' = 6.9%
Scale: 50, Probability Distribution: 'left' = 31.3%, 'up_left' = 6.8%, 'up_right' = 6.8%, 'right' = 31.3%, 'up' = 5.0%, 'down' = 5.0%, 'down_left' = 6.8%, 'down_right' = 6.8%
Scale: 52, Probability Distribution: 'left' = 31.6%, 'up_left' = 6.7%, 'up_right' = 6.7%, 'right' = 31.6%, 'up' = 5.0%, 'down' = 5.0%, 'down_left' = 6.7%, 'down_right' = 6.7%
Scale: 54, Probability Distribution: 'left' = 31.9%, 'up_left' = 6.6%, 'up_right' = 6.6%, 'right' = 31.9%, 'up' = 4.9%, 'down' = 4.9%, 'down_left' = 6.6%, 'down_right' = 6.6%
Scale: 56, Probability Distribution: 'left' = 32.1%, 'up_left' = 6.5%, 'up_right' = 6.5%, 'right' = 32.1%, 'up' = 4.8%, 'down' = 4.8%, 'down_left' = 6.5%, 'down_right' = 6.5%
Scale: 58, Probability Distribution: 'left' = 32.4%, 'up_left' = 6.4%, 'up_right' = 6.4%, 'right' = 32.4%, 'up' = 4.8%, 'down' = 4.8%, 'down_left' = 6.4%, 'down_right' = 6.4%
Scale: 60, Probability Distribution: 'left' = 32.6%, 'up_left' = 6.3%, 'up_right' = 6.3%, 'right' = 32.6%, 'up' = 4.7%, 'down' = 4.7%, 'down_left' = 6.3%, 'down_right' = 6.3%
Scale: 62, Probability Distribution: 'left' = 32.8%, 'up_left' = 6.3%, 'up_right' = 6.3%, 'right' = 32.8%, 'up' = 4.6%, 'down' = 4.6%, 'down_left' = 6.3%, 'down_right' = 6.3%
Scale: 64, Probability Distribution: 'left' = 33.1%, 'up_left' = 6.2%, 'up_right' = 6.2%, 'right' = 33.1%, 'up' = 4.6%, 'down' = 4.6%, 'down_left' = 6.2%, 'down_right' = 6.2%
Scale: 66, Probability Distribution: 'left' = 33.3%, 'up_left' = 6.1%, 'up_right' = 6.1%, 'right' = 33.3%, 'up' = 4.5%, 'down' = 4.5%, 'down_left' = 6.1%, 'down_right' = 6.1%
Scale: 68, Probability Distribution: 'left' = 33.5%, 'up_left' = 6.0%, 'up_right' = 6.0%, 'right' = 33.5%, 'up' = 4.4%, 'down' = 4.4%, 'down_left' = 6.0%, 'down_right' = 6.0%
Scale: 70, Probability Distribution: 'left' = 33.7%, 'up_left' = 5.9%, 'up_right' = 5.9%, 'right' = 33.7%, 'up' = 4.4%, 'down' = 4.4%, 'down_left' = 5.9%, 'down_right' = 5.9%
Scale: 72, Probability Distribution: 'left' = 33.9%, 'up_left' = 5.9%, 'up_right' = 5.9%, 'right' = 33.9%, 'up' = 4.3%, 'down' = 4.3%, 'down_left' = 5.9%, 'down_right' = 5.9%
Scale: 74, Probability Distribution: 'left' = 34.2%, 'up_left' = 5.8%, 'up_right' = 5.8%, 'right' = 34.2%, 'up' = 4.3%, 'down' = 4.3%, 'down_left' = 5.8%, 'down_right' = 5.8%
Scale: 76, Probability Distribution: 'left' = 34.4%, 'up_left' = 5.7%, 'up_right' = 5.7%, 'right' = 34.4%, 'up' = 4.2%, 'down' = 4.2%, 'down_left' = 5.7%, 'down_right' = 5.7%
Scale: 78, Probability Distribution: 'left' = 34.5%, 'up_left' = 5.6%, 'up_right' = 5.6%, 'right' = 34.5%, 'up' = 4.2%, 'down' = 4.2%, 'down_left' = 5.6%, 'down_right' = 5.6%
Scale: 80, Probability Distribution: 'left' = 34.7%, 'up_left' = 5.6%, 'up_right' = 5.6%, 'right' = 34.7%, 'up' = 4.1%, 'down' = 4.1%, 'down_left' = 5.6%, 'down_right' = 5.6%
Scale: 82, Probability Distribution: 'left' = 34.9%, 'up_left' = 5.5%, 'up_right' = 5.5%, 'right' = 34.9%, 'up' = 4.1%, 'down' = 4.1%, 'down_left' = 5.5%, 'down_right' = 5.5%
Scale: 84, Probability Distribution: 'left' = 35.1%, 'up_left' = 5.4%, 'up_right' = 5.4%, 'right' = 35.1%, 'up' = 4.0%, 'down' = 4.0%, 'down_left' = 5.4%, 'down_right' = 5.4%
Scale: 86, Probability Distribution: 'left' = 35.3%, 'up_left' = 5.4%, 'up_right' = 5.4%, 'right' = 35.3%, 'up' = 4.0%, 'down' = 4.0%, 'down_left' = 5.4%, 'down_right' = 5.4%
Scale: 88, Probability Distribution: 'left' = 35.4%, 'up_left' = 5.3%, 'up_right' = 5.3%, 'right' = 35.4%, 'up' = 3.9%, 'down' = 3.9%, 'down_left' = 5.3%, 'down_right' = 5.3%
Scale: 90, Probability Distribution: 'left' = 35.6%, 'up_left' = 5.3%, 'up_right' = 5.3%, 'right' = 35.6%, 'up' = 3.9%, 'down' = 3.9%, 'down_left' = 5.3%, 'down_right' = 5.3%
Scale: 92, Probability Distribution: 'left' = 35.8%, 'up_left' = 5.2%, 'up_right' = 5.2%, 'right' = 35.8%, 'up' = 3.8%, 'down' = 3.8%, 'down_left' = 5.2%, 'down_right' = 5.2%
Scale: 94, Probability Distribution: 'left' = 35.9%, 'up_left' = 5.1%, 'up_right' = 5.1%, 'right' = 35.9%, 'up' = 3.8%, 'down' = 3.8%, 'down_left' = 5.1%, 'down_right' = 5.1%
Scale: 96, Probability Distribution: 'left' = 36.1%, 'up_left' = 5.1%, 'up_right' = 5.1%, 'right' = 36.1%, 'up' = 3.8%, 'down' = 3.8%, 'down_left' = 5.1%, 'down_right' = 5.1%
Scale: 98, Probability Distribution: 'left' = 36.2%, 'up_left' = 5.0%, 'up_right' = 5.0%, 'right' = 36.2%, 'up' = 3.7%, 'down' = 3.7%, 'down_left' = 5.0%, 'down_right' = 5.0%
Scale: 100, Probability Distribution: 'left' = 36.4%, 'up_left' = 5.0%, 'up_right' = 5.0%, 'right' = 36.4%, 'up' = 3.7%, 'down' = 3.7%, 'down_left' = 5.0%, 'down_right' = 5.0%


"""
