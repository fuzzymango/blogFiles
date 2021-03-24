# --------------------------------------------------------------
#  customTracker_IS.py
#  Version: 1.0.3
#  Last Updated: June 18th, 2019
# --------------------------------------------------------------

import nuke

def customTrackerIS():

	code = '''
# get a list of all transform/cornerpin nodes before the tracker creates a new one
allTransformsBefore = nuke.allNodes("Transform", recurseGroups=True)
allCornerPinsBefore = nuke.allNodes("CornerPin2D", recurseGroups=True)

# --------------------------------------------------------------
# DEFAULT SCRIPT FROM TRACKER NODE
# --------------------------------------------------------------
tracker = nuke.thisNode()
cornerPinOption = tracker.knob("cornerPinOptions").getValue()
if cornerPinOption == 0:
    tracker.knob("createPinUseCurrentFrame").execute()
elif cornerPinOption == 1:
    tracker.knob("createPinUseReferenceFrame").execute()
elif cornerPinOption == 2:
    tracker.knob("createPinUseCurrentFrameBaked").execute()
elif cornerPinOption == 3:
    tracker.knob("createPinUseReferenceFrameBaked").execute()
elif cornerPinOption == 4:
    tracker.knob("createTransformStabilize").execute()
elif cornerPinOption == 5:
    tracker.knob("createTransformMatchMove").execute()
elif cornerPinOption == 6:
    tracker.knob("createTransformStabilizeBaked").execute()
elif cornerPinOption == 7:
    tracker.knob("createTransformMatchMoveBaked").execute()
# --------------------------------------------------------------
# --------------------------------------------------------------

# get a list of all transform/cornerpin nodes after the tracker has created a new one
allTransformsAfter = nuke.allNodes("Transform", recurseGroups=True)
allCornerPinsAfter = nuke.allNodes("CornerPin2D", recurseGroups=True)

# get the value of the reference frame from the tracker
refFrame = int(nuke.thisNode()['reference_frame'].value())
trackerName = str(nuke.thisNode().name())




try:
    # add the reference frame to the label
    [node for node in allTransformsAfter if node not in allTransformsBefore][0].knob("label").setValue('<center><b>Ref Frame: ' + str(refFrame))

    # set filter to mitchell
    [node for node in allTransformsAfter if node not in allTransformsBefore][0].knob("filter").setValue('Mitchell')

    # set shutter offset to centered
    [node for node in allTransformsAfter if node not in allTransformsBefore][0].knob("shutteroffset").setValue('centered')

    # keep track of previous transforms and name newly created transforms incrementally
    transformProposedName = trackerName + '_matchmove'
    index = 1
    while True:
        if not nuke.exists(transformProposedName + str(index)):
            transformActualName = transformProposedName + str(index)
            break
        index += 1

    # set the name of the created transform
    [node for node in allTransformsAfter if node not in allTransformsBefore][0].knob("name").setValue(transformActualName)

except:
    # add reference frame to the label
    [node for node in nuke.allNodes("CornerPin2D", recurseGroups=True) if node not in allCornerPinsBefore][0].knob("label").setValue('<center><b>Ref Frame: ' + str(refFrame))

    # add reference frame to the label
    [node for node in nuke.allNodes("CornerPin2D", recurseGroups=True) if node not in allCornerPinsBefore][0].knob("filter").setValue('Mitchell')

    # set shutter offset to centered
    [node for node in nuke.allNodes("CornerPin2D", recurseGroups=True) if node not in allCornerPinsBefore][0].knob("shutteroffset").setValue('centered')

    # keep track of previous cornerPins and name newly created cornerPins incrementally
    cornerPinProposedName = trackerName + '_cornerPin'
    index = 1
    while True:
        if not nuke.exists(cornerPinProposedName + str(index)):
            cornerPinActualName = cornerPinProposedName + str(index)
            break
        index += 1

    # set the name of the created cornerPin
    [node for node in allCornerPinsAfter if node not in allCornerPinsBefore][0].knob("name").setValue(cornerPinActualName)
	'''

	nuke.thisNode().knob('createCornerPin').setValue(code)
