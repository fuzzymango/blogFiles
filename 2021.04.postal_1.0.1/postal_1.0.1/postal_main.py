###########################
#  POSTAL MAIN SCRIPT
#  version 1.0.1
#  21 April 2021
#  isaacspiegel.com 
###########################

import random 
import nuke
import nukescripts

### CONSTANTS
ERROR_MESSAGE = 'ERROR: {}'

### GETS NAME OF PARENT FROM TEXT INPUT
### RETURNS THE STRING VALUE OF INPUT
def parentLabelFromUser(parentUpstreamNode):
	txt = nuke.getInput('Parent name', parentUpstreamNode['name'].value())
	if not txt:
		nuke.message(ERROR_MESSAGE.format('failed to get label'))
		return False
	else:
		return txt

### GETS THE LIST OF ALL CHILDREN FROM A GIVEN PARENT NODE
### RETURNS A LIST OF ALL CHILDREN
def get_child_list(parent_node):
	items = parent_node['childList'].value()
	items.splitlines()

	word = ''
	wordList = []
	for i in items:
		if not i == '\n':
			word+=i
		else:
			wordList.append(word)
			word = ''
	return wordList

### UPDATES THE LIST OF CHILDREN FOR A GIVEN PARENT NODE
### REMOVES ANY 'NONE' CHILDREN
def set_child_list(parent_node, wordList, setSelected):
	newList = ''
	for name in wordList:
		tn = nuke.toNode(name)
		if tn is not None:
			if setSelected: tn.setSelected(True)
			newList += name + '\n'

	parent_node['childList'].setValue(newList)


### MAIN SCRIPT THAT STARTS THE PROGRAM AND CREATES THE FIRST PARENT NODE
def createParent():
	sns = nuke.selectedNodes()
	if len(sns) > 1 or len(sns) == 0:
		nuke.message(ERROR_MESSAGE.format('select only 1 node'))
		return

	### CREATE PARENT FROM ANCHOR
	anchor = nuke.selectedNode()
	parentLabel = parentLabelFromUser(anchor)
	if not parentLabel: return

	parent = nuke.createNode('NoOp')
	parent['tile_color'].setValue(10485759)
	parent['note_font_size'].setValue(20.0)
	parent['note_font'].setValue('Verdana Bold Bold Bold')
	parent['name'].setValue(anchor['name'].value() + '_' + str(random.randint(0,1000000)))
	parent['label'].setValue(parentLabel)

	### PARENT TAB KNOBS AND BUTTONS
	parentTabKnob = nuke.Tab_Knob('postalParent', 'Postal parent')
	parent.addKnob(parentTabKnob)
	parentLabelStringKnob = nuke.String_Knob('parentLabel', 'parent label', parentLabel)
	parent.addKnob(parentLabelStringKnob)

	UPDATE_LABEL_PYSCRIPT = """
import update_label
update_label.update_label(nuke.thisNode())
	"""
	UPDATE_LABEL_TOOLTIP = """
Changes the names of all the child nodes to match the parent label
	"""
	parentUpdateLabelButton = nuke.PyScript_Knob('updateLabel', 'update label', UPDATE_LABEL_PYSCRIPT)
	parentUpdateLabelButton.setTooltip(UPDATE_LABEL_TOOLTIP)
	parent.addKnob(parentUpdateLabelButton)

	CREATE_CHILD_PYSCRIPT = """
import create_child
create_child.create_child(nuke.thisNode())
	"""
	CREATE_CHILD_TOOLTIP = """
Creates a new child node linked to this parent node
	"""
	parentCreateChildButton = nuke.PyScript_Knob('createChild', 'create child', CREATE_CHILD_PYSCRIPT)
	parentCreateChildButton.setFlag(0x0000000000001000)
	parentCreateChildButton.setTooltip(CREATE_CHILD_TOOLTIP)
	parent.addKnob(parentCreateChildButton)

	SELECT_CHILDREN_PYSCRIPT = """
import select_children
select_children.select_children()
	"""
	SELECT_CHILDREN_TOOLTIP = """
Selects all the children of this parent node
	"""
	parentSelectChildrenButton = nuke.PyScript_Knob('selectChildren', 'select children', SELECT_CHILDREN_PYSCRIPT)
	parentSelectChildrenButton.setTooltip(SELECT_CHILDREN_TOOLTIP)
	parent.addKnob(parentSelectChildrenButton)

	TOGGLE_INPUTS_PYSCRIPT = """
import toggle_inputs
toggle_inputs.toggle_inputs(nuke.thisNode())
"""
	TOGGLE_INPUTS_TOOLTIP = """
Toggles on/off the hidden inputs of all children linked to this parent node
	"""
	toggleInputsButton = nuke.PyScript_Knob('toggleInputs', 'toggle inputs', TOGGLE_INPUTS_PYSCRIPT)
	parent.addKnob(toggleInputsButton)

	### SET AUTOLABEL
	anchor.setSelected(False)
	parent.setSelected(True)
	parent['autolabel'].setValue("nuke.thisNode().knob('label').value()")

	## PARENT NODE CHILDREN TAB
	listChildrenTabKnob = nuke.Tab_Knob('children', 'children')
	parent.addKnob(listChildrenTabKnob)

	## LIST OF CHILDREN TWIRL DOWN MENU
	childListTwirlTab = nuke.Tab_Knob('list of children', None, nuke.TABBEGINCLOSEDGROUP)
	parent.addKnob(childListTwirlTab)

	LIST_CHILDREN_KNOB_TOOLTIP = """
This is the current list of the names of the nodes (not labels!!) of all the children connected to this parent node. You can manually add/remove children by editing this list. Make sure to press the 'Update' button to apply any changes.

WARNING: Toying with this list improperly may break connections to other children, use with caution. 
	"""
	listChildrenKnob = nuke.Multiline_Eval_String_Knob('childList', 'child nodes', '')
	listChildrenKnob.setTooltip(LIST_CHILDREN_KNOB_TOOLTIP)
	parent.addKnob(listChildrenKnob)
	UPDATE_CHILD_LIST_PYSCRIPT = """
import postal_main
listOfChildren = postal_main.get_child_list(nuke.thisNode())
postal_main.set_child_list(nuke.thisNode(), listOfChildren, False)
	"""
	UPDATE_CHILD_LIST_TOOLTIP = """
Refreshes the list of children that are linked to this parent node
	"""
	updateChildListButton = nuke.PyScript_Knob('updateList', 'update', UPDATE_CHILD_LIST_PYSCRIPT)
	updateChildListButton.setFlag(0x0000000000001000)
	updateChildListButton.setTooltip(UPDATE_CHILD_LIST_TOOLTIP)
	parent.addKnob(updateChildListButton)
	childListTwirlTab = nuke.Tab_Knob('list of children', None, -1)
	parent.addKnob(childListTwirlTab)


	
	hideInputCheckbox = nuke.Boolean_Knob('hideInputTracker', 'hideInputTracker')
	hideInputCheckbox.setFlag(0x0000000000000400)
	hideInputCheckbox.setTooltip(TOGGLE_INPUTS_TOOLTIP)
	parent.addKnob(hideInputCheckbox)
	parent['hideInputTracker'].setValue(True)


	### AUTO-CREATE FIRST CHILD
	parent['createChild'].execute()