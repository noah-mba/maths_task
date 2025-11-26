##--------------------------------------------
## Importing modules
##--------------------------------------------
from psychopy import core, visual, event, data, gui
import numpy as np
import os

## ----------------------
## Setup global variables
## ----------------------
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

expName = 'MathsDistractorTask'
psychopyVersion = '2025.1.1'

# Global quit keys
for key in ['escape']:
    event.globalKeys.add(key, func=core.quit) # this ensure that the experiment quits when we press escape

# Information about this experiment
expInfo = {
    'Participant': '',
    'Session': '001',
    'date': data.getDateStr(),
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}

##-------------------------------------------------
## GUI for participants info
##-------------------------------------------------
# Use this dict to create the dlg
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, sortKeys=False)
if not dlg.OK:
    core.quit()

##--------------------------------------------
## Creating a window
##--------------------------------------------
win = visual.Window(size=(1024, 768), 
                    fullscr=True, # Set to True for actual experiment
                    screen=0, 
                    units='pix',
                    allowGUI=False, 
                    color=[0.0, 0.0, 0.0], # Black background
                    colorSpace='rgb')

win.mouseVisible = False

##--------------------------------------------
## Creating stimuli
##--------------------------------------------

# 1. Instructions
instr_text = "¡Bienvenido!\n\nVerás una serie de operaciones matemáticas.\nEscribe la respuesta usando las teclas numéricas.\nPulsa INTRO para confirmar tu respuesta.\n\nResponde de forma precisa.\n\nPulsa ESPACIO para comenzar."
instructions = visual.TextStim(win, text=instr_text, color='white', height=30, wrapWidth=800)

# 2. Problem Text (The Question)
problem_stim = visual.TextStim(win, text='PlaceHolder', pos=(0, 100), height=50, color='white')

# 3. Answer Text (What the user is typing)
answer_stim = visual.TextStim(win, text='', pos=(0, -50), height=50, color='lime')

# 4. Prompt Text
prompt_stim = visual.TextStim(win, text='Escribe la respuesta y pulsa INTRO', pos=(0, -150), height=20, color='gray')

##-------------------------------------------------
## Data Handling
##-------------------------------------------------

# Define output filename
filename = _thisDir + os.sep + 'data/%s_%s_%s' % (expInfo['Participant'], expName, expInfo['date'])

# Load conditions
# Ensure 'math_problems.csv' exists in the same folder!
try:
    conditions = data.importConditions('math_problems.csv')
except Exception as e:
    print(f"Error loading csv: {e}")
    core.quit()

# Create Trial Handler
# Method is 'sequential' because your PDF said "Resuelve estas operaciones por orden" (Solve in order)
trials = data.TrialHandler(nReps=1, method='sequential', 
                           trialList=conditions, extraInfo=expInfo, name='trials')

# Create Experiment Handler (saves the data)
thisExp = data.ExperimentHandler(name=expName, version='1.0',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)

thisExp.addLoop(trials)

##-------------------------------------------------
## Run Experiment
##-------------------------------------------------

# --- Show Instructions ---
instructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# --- Start Global Timer (5 Minutes) ---
experiment_timer = core.Clock()
TIME_LIMIT = 300.0 # 5 minutes in seconds

# --- Trial Loop ---
for trial in trials:
    
    # 1. Check Global Time Limit
    if experiment_timer.getTime() > TIME_LIMIT:
        print("Time limit reached! Ending experiment.")
        break
        
    # 2. Setup Trial Stimuli
    problem_stim.text = trial['operation_text']
    correct_answer = int(trial['correct_answer'])
    
    # Variables for the typing loop
    user_input = ""
    trial_clock = core.Clock() # Reset reaction time clock
    event.clearEvents()
    
    # 3. Typing Loop (Wait for Enter)
    trial_finished = False
    
    while not trial_finished:
        
        # Check global timer continuously (optional: immediate stop)
        if experiment_timer.getTime() > TIME_LIMIT:
            break
            
        # Draw stimuli
        problem_stim.draw()
        answer_stim.text = user_input # Update what they see
        answer_stim.draw()
        prompt_stim.draw()
        win.flip()
        
        # Check keys
        keys = event.getKeys()
        
        for key in keys:
            # A. If Enter is pressed -> Submit
            if key == 'return' or key == 'enter':
                if len(user_input) > 0: # Ensure they typed something
                    response_time = trial_clock.getTime()
                    trial_finished = True
            
            # B. If Backspace -> Delete last character
            elif key == 'backspace':
                user_input = user_input[:-1]
                
            # C. If Number -> Add to string
            # We allow 'num_0' through 'num_9' (numpad) and '0' through '9' (top row)
            elif key.replace('num_', '').isdigit():
                digit = key.replace('num_', '')
                user_input += digit
            
            # D. Escape -> Quit
            elif key == 'escape':
                core.quit()

    # 4. Save Data (Only if time didn't run out mid-trial)
    if experiment_timer.getTime() <= TIME_LIMIT:
        
        # Calculate Accuracy
        try:
            participant_int = int(user_input)
            is_correct = 1 if participant_int == correct_answer else 0
        except ValueError:
            participant_int = -999
            is_correct = 0

        print(f"Problem: {trial['operation_text']} | User: {user_input} | Correct: {is_correct}")

        trials.addData('user_response', user_input)
        trials.addData('accuracy', is_correct)
        trials.addData('rt', response_time)
        
        thisExp.nextEntry() # Save row to CSV

# --- End Experiment ---
end_text = visual.TextStim(win, text="¡Se ha acabado el tiempo!\n\nGracias por participar.", color='white')
end_text.draw()
win.flip()
core.wait(3)

win.close()
core.quit()