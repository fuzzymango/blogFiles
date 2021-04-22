import nukescripts
import nuke
import postal_main

def select_children():
	n = nuke.thisNode()
	listOfChildren = postal_main.get_child_list(n)

	nukescripts.clear_selection_recursive()

	postal_main.set_child_list(n, listOfChildren, True)