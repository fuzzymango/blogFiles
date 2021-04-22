import random
import nukescripts
import nuke

def create_child(parent_node):

	parentName = parent_node.knob('name').value()
	parentLabel = parent_node.knob('parentLabel').value()
	parentXpos = parent_node.knob('xpos').value()
	parentYpos = parent_node.knob('ypos').value()

	childName = parentLabel + '_' + str(random.randint(0,1000000))
	prevChildList = parent_node.knob('childList').value()
	newChildList = prevChildList + childName + '\n'
	parent_node.knob('childList').setValue(newChildList)

	nukescripts.clear_selection_recursive()
	child = nuke.createNode('NoOp', inpanel=False)
	child.setInput(0, nuke.toNode(parentName))
	nuke.toNode(child['name'].value()).setSelected(True)

	child['hide_input'].setValue(nuke.toNode(parentName).knob('hideInputTracker').value())
	child['note_font_size'].setValue(20.0)
	child['tile_color'].setValue(3511807)
	child['note_font'].setValue('Verdana Bold Bold Bold')
	child['xpos'].setValue(parentXpos)
	child['ypos'].setValue(parentYpos + 50)
	child['name'].setValue(childName)

	childTabKnob = nuke.Tab_Knob('postalChild', 'postal child')
	child.addKnob(childTabKnob)

	parentIDKnob = nuke.String_Knob('parentID', 'parent ID', parentName)
	child.addKnob(parentIDKnob)

	parentLabelKnob = nuke.String_Knob('parentLabel', 'parent label', parentLabel)
	child.addKnob(parentLabelKnob)

	CONNECT_TO_PARENT = """
import connect_to_parent
connect_to_parent.connect_to_parent(nuke.thisNode())
"""
	CONNECT_TO_PARENT_TOOLTIP = """
Reconnects this node to its parentID. This button must be pressed to add this child to parent's list of children
	"""
	connectToParentButton = nuke.PyScript_Knob('connectToParent', 'connect to parent', CONNECT_TO_PARENT)
	connectToParentButton.setFlag(0x0000000000001000)
	connectToParentButton.setTooltip(CONNECT_TO_PARENT_TOOLTIP)
	child.addKnob(connectToParentButton)

	nukescripts.clear_selection_recursive()
	nuke.toNode(child['name'].value()).setSelected(True)
	child['autolabel'].setValue("nuke.thisNode().knob('parentLabel').value()")