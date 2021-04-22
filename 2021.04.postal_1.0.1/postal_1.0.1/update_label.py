import nuke 
import nukescripts
import postal_main

def update_label(parent_node):
	parent_node['autolabel'].setValue("nuke.thisNode().knob('parentLabel').getValue()")
	newParentLabel = parent_node['parentLabel'].getValue()

	listOfChildren = postal_main.get_child_list(parent_node)

	for child in listOfChildren:
		childNode = nuke.toNode(child)
		if childNode is None: 
			continue
		childNode['parentLabel'].setValue(newParentLabel)
		childNode.knob('autolabel').setValue("nuke.thisNode().knob('parentLabel').getValue()")

	postal_main.set_child_list(parent_node, listOfChildren, False)