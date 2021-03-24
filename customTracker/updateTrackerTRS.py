# --------------------------------------------------------------
#  updateTrackerTRS.py
#  Version: 1.0.1
#  Last Updated: September 5th, 2019
# --------------------------------------------------------------
# --------------------------------------------------------------
# ADD TO MENU.PY
# utilitiesMenu = nuke.menu('Nuke').addMenu('IsaacUtilities')
# # add tracker TRS checkbox toggling to the toolbar
# from updateTrackerTRS import *
# utilitiesMenu.addCommand('Toggle Tracker TRS/Toggle Tracker Translate', 'update_tracker_TRS(True,  False, False)', 'shift+t', icon='Tracker4.png', shortcutContext=2)
# utilitiesMenu.addCommand('Toggle Tracker TRS/Toggle Tracker Rotate', 'update_tracker_TRS(False, True,  False)', 'shift+r', icon='Tracker4.png', shortcutContext=2)
# utilitiesMenu.addCommand('Toggle Tracker TRS/Toggle Tracker Scale', 'update_tracker_TRS(False, False, True)', 'shift+e', icon='Tracker4.png', shortcutContext=2)
# --------------------------------------------------------------

import nuke
import re
import nukescripts

def update_tracker_TRS(trans, rot, scale):

	# get the current node context
	node = nuke.selectedNode()

	if node.Class() == 'Tracker4':
		# set a variable for the 'Tracks' knob
		track_list = node['tracks']

		# filter Tracks knob to find the number of tracks
		items = re.findall('{ [0-9, ]*}', track_list.toScript())[0]
		num_tracks = int(items.split(' ')[-2])

		# validate the user input SHIFT + T
		if (trans == True and rot == False and scale == False):
			for i in range(0, num_tracks):
				# check to see if T is checked or not
				if track_list.getValue(31*i+6) == 0:
					# set T to True
					track_list.setValue(trans, 31*i+6)
				else: 
					# set T to False
					trans = 0
					track_list.setValue(trans, 31*i+6)
		
		# validate user input SHIFT + R
		elif (trans == False and rot == True and scale == False):
			for i in range(0, num_tracks):
				# check to see if R is checked or not
				if track_list.getValue(31*i+7) == 0:
					# set R to True
					track_list.setValue(rot, 31*i+7)
				else: 
					# set R to False
					rot = 0
					track_list.setValue(rot, 31*i+7)

		# validate user input SHIFT + S
		elif (trans == False and rot == False and scale == True):
			for i in range(0, num_tracks):
				# check to see if S is checked or not
				if track_list.getValue(31*i+8) == 0:
					# set S to True
					track_list.setValue(scale, 31*i+8)
				else: 
					# set S to False
					scale = 0
					track_list.setValue(scale, 31*i+8)

		else:
			pass

	else:
		nuke.message('Wrong node class slected. Use Tracker4')
