import maya.cmds as cmds

def mirrorPoseUI():
    if cmds.window("mirrorPoseWin", exists=True):
        cmds.deleteUI("mirrorPoseWin")

    cmds.window("mirrorPoseWin", title="Mirror Pose", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Mirror Pose", command=mirrorPose)
    cmds.showWindow("mirrorPoseWin")

def mirrorPose(*args):
    selected = cmds.ls(selection=True)
    for ctrl in selected:
        # Determine the opposite controller or if it is a center controller
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = None  # Center controller, no suffix
        
        key_attrs = cmds.listAttr(ctrl, keyable=True)
        for attr in key_attrs:
            # Only process translation and rotation attributes
            if attr.startswith("translate") or attr.startswith("rotate"):
                try:
                    value = cmds.getAttr(f"{ctrl}.{attr}")
                    flipped_value = -value if isinstance(value, (int, float)) else value

                    if opposite_ctrl and cmds.objExists(opposite_ctrl):
                        cmds.setAttr(f"{opposite_ctrl}.{attr}", flipped_value)
                    else:
                        cmds.setAttr(f"{ctrl}.{attr}", flipped_value)
                except:
                    cmds.warning(f"Failed to mirror attribute {attr} for controller {ctrl}.")

mirrorPoseUI()
