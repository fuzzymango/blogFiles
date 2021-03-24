# --------------------------------------------------------------
#  KEYFRAME RETIMER
#  Version: 1.0.4
#  Last Updated: 21 February 2021
# --------------------------------------------------------------
#  This script assigns a retime expression based off a Kronos, 
#  OFlow, timewarp, or framehold node to all other selected
#  nodes. Very useful for retiming cameras or transforms.
# --------------------------------------------------------------
import nuke
import nukescripts

# list of valid knobs to be retimed
VALID_KNOBS = [
	"int_knob",
	"multiInt_knob",
	"double_knob",
	"float_knob",
	"multifloat_knob",
	"array_knob",
	"xy_knob",
	"xyz_knob",
	"wh_knob",
	"bbox_knob",
	"color_knob",
	"acolor_knob",
	"axis_knob",
	"uv_knob",
	"box3_knob",
	"range_knob",
	"keyer_knob",
	"scale_knob",
	"positionvector_knob",
	"iarray_knob"]

# list of nodes that are able to retime
VALID_RETIME_NODES = [
	"Kronos",
	"OFlow2",
	"FrameHold",
	"TimeOffset",
	"TimeWarp"]

ERROR_FORMAT = 'ERROR: {}'

def getRetimeExpression(retimeNode):
	inputOutputSpeedFormat = 'curve(((frame-{0}.input.first)*{0}.{1})+{0}.input.first)'

	timingTypes = {
		'Output Speed' : inputOutputSpeedFormat.format(retimeNode['name'].value(),'timingOutputSpeed'),
		'Input Speed'  : inputOutputSpeedFormat.format(retimeNode['name'].value(),'timingInputSpeed'),
		'Frame'        : 'curve(' + retimeNode['name'].value() + '.timingFrame2)',
		'FrameHold'    : 'curve(' + retimeNode['name'].value() + '.knob.first_frame)',
		'TimeOffset'   : '(frame + ' + retimeNode['name'].value() + '.time_offset)',
		'TimeWarp'     : 'curve(' + retimeNode['name'].value() + '.lookup)'
	}

	retimeNodeClass = retimeNode.Class()
	if retimeNodeClass   == 'Kronos' or retimeNode == 'OFlow2': return timingTypes[retimeNode['timing2'].value()]
	elif retimeNodeClass == 'FrameHold' : return timingTypes['FrameHold']
	elif retimeNodeClass == 'TimeOffset': return timingTypes['TimeOffset']
	elif retimeNodeClass == 'TimeWarp'  : return timingTypes['TimeWarp']
	else: return None

def getAnimatedNodes(selection, retimeNode):
	animatedNodes = []
	animatedNode = False
	for n in selection:
		if n is retimeNode: continue
		for k in n.knobs():
			if str.lower(n[k].Class()) in VALID_KNOBS and n[k].isAnimated():
				animatedNode = True
		if animatedNode: animatedNodes.append(n)

	return animatedNodes

def setRetimeExpression(node_n, retimeNode):
	for k in node_n.knobs():
		if not node_n[k].isAnimated(): continue
		for subKnob in node_n[k].animations():
			subKnob.setExpression(getRetimeExpression(retimeNode))

def retimeKeyframes():
	# variable to store the kronos node used for retiming
	retimeNode = None

	# the user selection of nodes
	selection = nuke.selectedNodes()

	if not (selection):
		nuke.message(ERROR_FORMAT.format('selection is empty'))
		return

	if not selection[-1].Class() in VALID_RETIME_NODES:
		nuke.message(ERROR_FORMAT.format('must select the node doing the retiming first'))
		return
	retimeNode = selection[len(selection)-1]


	animatedNodeList = getAnimatedNodes(selection, retimeNode)
	for n in animatedNodeList:
		setRetimeExpression(n, retimeNode)
