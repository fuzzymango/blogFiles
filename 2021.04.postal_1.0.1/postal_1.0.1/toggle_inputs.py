import nuke
import nukescripts
import postal_main

def toggle_inputs(n):
	n = nuke.thisNode()
	n['hideInputTracker'].setValue(not n['hideInputTracker'].value())

	listOfChildren = postal_main.get_child_list(n)

	for child in listOfChildren:
		childNode = nuke.toNode(child)
		if not childNode is None: childNode['hide_input'].setValue(not childNode['hide_input'].value())

	postal_main.set_child_list(n, listOfChildren, False)