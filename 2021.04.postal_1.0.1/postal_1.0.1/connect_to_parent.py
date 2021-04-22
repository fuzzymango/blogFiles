import nuke
import nukescripts
import postal_main

def connect_to_parent(thisNode):
	parentName = thisNode['parentID'].value()

	parentNode = nuke.toNode(parentName)
	if parentNode is None:
		nuke.message('ERROR: unable to locate parent. Has the parent been deleted?')
		return

	thisNode.setInput(0, parentNode)
	thisNode['hide_input'].setValue(parentNode['hideInputTracker'].value())
	thisNode['parentLabel'].setValue(parentNode['parentLabel'].value())


	listOfChildren = postal_main.get_child_list(parentNode)


	childName = thisNode['name'].value()
	if childName not in listOfChildren:
		listOfChildren.append(childName)

	postal_main.set_child_list(parentNode, listOfChildren, False)