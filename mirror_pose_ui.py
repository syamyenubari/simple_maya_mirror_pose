import maya.cmds as cmds

def mirrorPoseUI():
    if cmds.window("mirrorPoseWin", exists=True):
        cmds.deleteUI("mirrorPoseWin")

    cmds.window("mirrorPoseWin", title="Mirror Pose Plugin", widthHeight=(300, 380))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.button(label="Mirror Pose", command=mirrorPose, height=35)
    cmds.button(label="Mirror Pose (Suits IK)", command=mirrorPoseSuitsIK, height=35)
    cmds.button(label="Mirror (Unflipped) Pose", command=mirrorUnflippedPose, height=35)
    cmds.button(label="Copy Pose", command=copyPose, height=35)
    cmds.button(label="Paste Pose", command=pastePose, height=35)
    cmds.button(label="Paste Mirror (This Side)", command=pasteMirrorThisSide, height=35)
    cmds.button(label="Paste Mirror Pose", command=pasteMirrorPose, height=35)
    cmds.button(label="Paste Mirror (Unflipped) Pose", command=pasteMirrorUnflippedPose, height=35)
    cmds.showWindow("mirrorPoseWin")

pose_data = {}

def mirrorPose(*args):
    selected = cmds.ls(selection=True)
    for ctrl in selected:
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = None  # Center controller, no suffix
        
        key_attrs = cmds.listAttr(ctrl, keyable=True)
        for attr in key_attrs:
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

def mirrorUnflippedPose(*args):
    selected = cmds.ls(selection=True)
    for ctrl in selected:
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = None  # Center controller, no suffix
        
        key_attrs = cmds.listAttr(ctrl, keyable=True)
        for attr in key_attrs:
            if attr.startswith("translate") or attr.startswith("rotate"):
                try:
                    value = cmds.getAttr(f"{ctrl}.{attr}")
                    if opposite_ctrl and cmds.objExists(opposite_ctrl):
                        cmds.setAttr(f"{opposite_ctrl}.{attr}", value)
                    else:
                        cmds.setAttr(f"{ctrl}.{attr}", value)
                except:
                    cmds.warning(f"Failed to mirror attribute {attr} for controller {ctrl}.")

def copyPose(*args):
    global pose_data
    selected = cmds.ls(selection=True)
    pose_data = {}
    for ctrl in selected:
        key_attrs = cmds.listAttr(ctrl, keyable=True)
        pose_data[ctrl] = {attr: cmds.getAttr(f"{ctrl}.{attr}") for attr in key_attrs if attr.startswith("translate") or attr.startswith("rotate")}

def pastePose(*args):
    global pose_data
    for ctrl, attrs in pose_data.items():
        for attr, value in attrs.items():
            try:
                cmds.setAttr(f"{ctrl}.{attr}", value)
            except:
                cmds.warning(f"Failed to paste attribute {attr} for controller {ctrl}.")

def pasteMirrorThisSide(*args):
    global pose_data
    for ctrl, attrs in pose_data.items():
        for attr, value in attrs.items():
            try:
                flipped_value = -value if isinstance(value, (int, float)) else value
                cmds.setAttr(f"{ctrl}.{attr}", flipped_value)
            except:
                cmds.warning(f"Failed to paste mirror attribute {attr} for controller {ctrl}.")

def pasteMirrorPose(*args):
    global pose_data
    for ctrl, attrs in pose_data.items():
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = ctrl  # Center controller, no suffix
        
        for attr, value in attrs.items():
            try:
                flipped_value = -value if isinstance(value, (int, float)) else value
                if opposite_ctrl and cmds.objExists(opposite_ctrl):
                    cmds.setAttr(f"{opposite_ctrl}.{attr}", flipped_value)
                else:
                    cmds.setAttr(f"{ctrl}.{attr}", flipped_value)
            except:
                cmds.warning(f"Failed to paste mirror attribute {attr} for controller {ctrl}.")

def pasteMirrorUnflippedPose(*args):
    global pose_data
    for ctrl, attrs in pose_data.items():
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = ctrl  # Center controller, no suffix
        
        for attr, value in attrs.items():
            try:
                if opposite_ctrl and cmds.objExists(opposite_ctrl):
                    cmds.setAttr(f"{opposite_ctrl}.{attr}", value)
                else:
                    cmds.setAttr(f"{ctrl}.{attr}", value)
            except:
                cmds.warning(f"Failed to paste mirror attribute {attr} for controller {ctrl}.")

def mirrorPoseSuitsIK(*args):
    selected = cmds.ls(selection=True)
    for ctrl in selected:
        if ctrl.endswith('L') or ctrl.endswith('l'):
            opposite_ctrl = ctrl[:-1] + 'R'
        elif ctrl.endswith('R') or ctrl.endswith('r'):
            opposite_ctrl = ctrl[:-1] + 'L'
        else:
            opposite_ctrl = None  # Center controller, no suffix
        
        key_attrs = cmds.listAttr(ctrl, keyable=True)
        for attr in key_attrs:
            if attr.startswith("translate") or attr.startswith("rotate"):
                try:
                    value = cmds.getAttr(f"{ctrl}.{attr}")
                    if attr == 'translateY':
                        flipped_value = value  # Keep Y translation the same
                    else:
                        flipped_value = -value if isinstance(value, (int, float)) else value
                    if opposite_ctrl and cmds.objExists(opposite_ctrl):
                        cmds.setAttr(f"{opposite_ctrl}.{attr}", flipped_value)
                    else:
                        cmds.setAttr(f"{ctrl}.{attr}", flipped_value)
                except:
                    cmds.warning(f"Failed to mirror attribute {attr} for controller {ctrl}.")

mirrorPoseUI()
