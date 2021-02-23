# create a menu called IsaacUtilities at the top toolbar
utilitiesMenu = nuke.menu('Nuke').addMenu('IsaacUtilities')

import retimeKeyframes_IS
utilitiesMenu.addCommand('Retime Keyframes', 'retimeKeyframes_IS.retimeKeyframes()', shortcutContext=2)
