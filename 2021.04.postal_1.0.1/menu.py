# Add this to your menu.py file located in the .nuke folder. 
# The default keyboard shortcut to create a new parent is F9,
# change this value to whatever keyboard shortcut you would like.
import postal_main
utilitiesMenu.addCommand('Postal Parent', 'postal_main.createParent()', 'F9', shortcutContext=2)