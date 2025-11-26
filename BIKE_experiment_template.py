"""
Proposal for a BIKE experiment template using PsychoPy
Initially conceived in October'25 by Carlos and ...

Re-using materiales from many others (notably Silvia Formica <3)

REQUIREMENTS:
    - Download and install PsychoPy standalone: https://www.psychopy.org/download.html
    - Open this script from PsychoPy Coder
(Note: this was created in PsychoPy v2025.1.1. Unsure about backwards compatibility)
"""

##--------------------------------------------
## Importing modules
# To begin with, we import the functions we are going to use throughout the 
# experiment. Some are collections of functions in python (e.g., numpy),
# some are specific features of psychopy. You can always google them
# to check the online documentation.
##--------------------------------------------
from psychopy import core, visual, event, data, gui
import numpy as np
import pandas as pd
import random
import os
import csv

## ----------------------
## Setup global variables
## ----------------------
for key in ['q', 'escape']:
    event.globalKeys.add(key, func=core.quit) # this ensure that the experiment quits when we press q or escape
_thisDir = os.path.dirname(os.path.abspath(__file__)) # ensure that relative paths start from the same directory as this script
psychopyVersion = '2025.1.1'
expName = 'BIKE_exp_template'

# information about this experiment
expInfo = {
    'Participant': '',
    'Age':'',
    'Gender':['Female', 'Male', 'Other', 'I prefer not to say'],
    'Handedness':['Right', 'Left', 'Both'],
    'date': data.getDateStr(),
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}

##-------------------------------------------------
## GUI for participants info
##-------------------------------------------------
# Use this dict to create the dlg
infoDlg = gui.DlgFromDict(dictionary=expInfo, 
    title=expName,sortKeys=False)
# Script will now wait for the dlg to close...

if infoDlg.OK:  # This will be True if user hit OK...
    print(expInfo)
else: # ...or False, if they hit Cancel
    print('User Cancelled')
    core.quit()  # user pressed cancel


##--------------------------------------------
## Creating a window

# To present visual stimuli in our experiment, we need to create a canvas
# on which we can draw them.
# Many parameters can be modified (https://psychopy.org/api/visual/window.html)
# but a few are crucial: size (in pixels - you can find the resolution of your
# screen under the properties tab if you want to have the window fullscreen),
# color (can be a string or the RGB values)
# and units (we will go for pixels, the choice depends on the characteristics 
# of your experiment and on the stimuli you need to present).
##--------------------------------------------

win = visual.Window(size=(800,600), # Size of the window in whatever unit we expecify below
                    fullscr=False, # make window fullscreen (better timing)
                    screen=0, # Specifies the physical screen that stimuli will appear on (in case there's more than one)
                    units='pix', # note that units are in pixels!
                    allowGUI=False, # If False, window will be drawn with no frame and no buttons to close etc
                    color=[0.5, 0.5, 0.5], # set the color of the window to GRAY
                    colorSpace='rgb')

# Other useful parameters:
# win.mouseVisible = False
# win.fullscr=True

##--------------------------------------------
## Creating stimuli

#Now that we have a canvas, we want to create stimuli to draw on it.
#Psychopy is quite flexible, and offers already a large variety of objects that 
#can be drawn (https://www.psychopy.org/api/visual/).

#Some crucial elements that we are going to use for our experiments are 
#Text strings and Images.

# TIP: initialize as many stimuli as you will need for the whole task
##--------------------------------------------

# For instance, we can create the instructions for our experiment

# --- Instructions Text ---
textStim = visual.TextStim(win,
                            color = 'black',
                            text='Welcome!\n\n\nWhenever you are ready, press the spacebear to continue.')
textStim.draw()
win.flip()
core.wait(0.1)
press=event.waitKeys(1000000000, keyList=(['space', 'q'])) # this will make the instruction stay on screen until the spacebar is pressed

# --- We can also create as many stimuli as you will need for the whole task --- 
fixation = visual.TextStim(win, text='+', color = 'white')
target = visual.TextStim(win, text='word', color = 'white')

##-------------------------------------------------
## Design Matrix: load or create list of trials
##-------------------------------------------------

## OPTION 1: loading a csv file (this will be almost always the to-go option
# you can use this option is you have create a design matrix in advance
design = data.importConditions('design.csv' )

## OPTION 2: create from scratch the design using Psychopy functions
#design = data.createFactorialTrialList(
#    {'groupBehav':['approach', 'avoid'],
#    'stimValence': ['happy', 'angry']})
#design = design * 3 # increase the number of trials by 3

##-------------------------------------------------
## Experiment and TrialHandler
# Once we've loaded our trials, we can make use of
# PsychoPy tools to handle trials and store data
##-------------------------------------------------

## creating output file
output_filename = f"{expName}_sub{int(expInfo['Participant']):02d}"

## Setting an ExperimentHandler for data saving
thisExp = data.ExperimentHandler(name='expName',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=output_filename)
    
## Setting the trial list using TrialHandler
trials = data.TrialHandler(nReps=1,
    method='random', # be careful! if you're loading an already randomized file, then set to 'sequential'
    originPath=-1, 
    trialList=design,
    seed=None, name='trials')

## Adding the trial loop to the experiment
thisExp.addLoop(trials)

for trial in trials:
    print('start trial' + str(trial))
    
    ## now we need to define the sequence of events that will repeat over trials
    
    # --- FIXATION ---
    # we draw the fixation 
    fixation.draw()
    # we flip the window to make the fixation appear
    win.flip()
    # we wait for 2 seconds with the fixation on the window
    core.wait(2)
    
    # --- TARGET ---
    target.text = trial['target'] # we update the content of the target based on the design file column ('target')
    target.draw()
    win.flip()
    
    # cleaning key presses that might be saved in memory from earlier
    event.clearEvents()

    # we specify which keys can be used to respond
    allowed_keys = ['a', 'l', 'space']
    # ..and how much time
    max_time = 2.0  # (in seconds)
    
    ## Simplest option: waits for one single response up to a maximum time deadline
    # This option 'blocks' everything until the button is pressed, or until
    # max_time is reached. Nothing else can be done during this time.
    # Good and efficient for a single button press

    clock = core.Clock()
    key_press = event.waitKeys(max_time, allowed_keys, timeStamped = clock)
    thisExp.addData('response', key_press)  # Log response
    print('Response collected:')
    print(key_press)
    
     # the last line informs the experiment that we are moving on to the 
    # next trial and saves all the info to our output file
    thisExp.nextEntry()

