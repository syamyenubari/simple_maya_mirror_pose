import bpy
from bpy.props import StringProperty, CollectionProperty
import mathutils
import json

def get_opposite_suffix(name):
    suffixes = {
        'L': 'R', 'l': 'r', 'R': 'L', 'r': 'l',
        '_L': '_R', '_l': '_r', '_R': '_L', '_r': '_l',
        '.L': '.R', '.l': '.r', '.R': '.L', '.r': '.l'
    }
    for suffix, opposite in suffixes.items():
        if name.endswith(suffix):
            return name[:-len(suffix)] + opposite
    return None

def flip_value(value):
    return [-v for v in value]

def mirror_pose(context, flip_values=True, copy_mode=False, paste_mode=False, ik_mode=False):
    pose_bones = context.active_object.pose.bones if context.active_object and context.active_object.type == 'ARMATURE' else None

    if not pose_bones:
        return {'CANCELLED'}

    if copy_mode:
        context.scene.mirrored_pose_data.clear()

    for bone in pose_bones:
        if bone.bone.select:
            if copy_mode:
                data = context.scene.mirrored_pose_data.add()
                data.name = bone.name
                data.data = json.dumps({
                    'location': list(bone.location),
                    'rotation_quaternion': list(bone.rotation_quaternion),
                    'rotation_euler': list(bone.rotation_euler)
                })
            elif paste_mode:
                opposite_name = get_opposite_suffix(bone.name)
                if opposite_name:
                    data_item = next((item for item in context.scene.mirrored_pose_data if item.name == bone.name), None)
                    if data_item:
                        data = json.loads(data_item.data)
                        loc = mathutils.Vector(data['location'])
                        rot_quat = mathutils.Quaternion(data['rotation_quaternion'])
                        rot_euler = mathutils.Euler(data['rotation_euler'])

                        if flip_values:
                            loc = flip_value(loc)
                            rot_quat.conjugate()
                            rot_euler = flip_value(rot_euler)

                        if ik_mode:
                            loc[2] = data['location'][2]  # Keep Z location unflipped for IK mode

                        opposite_bone = pose_bones.get(opposite_name)
                        if opposite_bone:
                            opposite_bone.location = loc
                            opposite_bone.rotation_quaternion = rot_quat
                            opposite_bone.rotation_euler = rot_euler
            else:
                opposite_name = get_opposite_suffix(bone.name)
                if opposite_name:
                    opposite_bone = pose_bones.get(opposite_name)
                    if opposite_bone:
                        loc = bone.location.copy()
                        rot_quat = bone.rotation_quaternion.copy()
                        rot_euler = bone.rotation_euler.copy()

                        if flip_values:
                            loc = flip_value(loc)
                            rot_quat.conjugate()
                            rot_euler = flip_value(rot_euler)

                        if ik_mode:
                            loc[2] = bone.location[2]  # Keep Z location unflipped for IK mode

                        opposite_bone.location = loc
                        opposite_bone.rotation_quaternion = rot_quat
                        opposite_bone.rotation_euler = rot_euler
                elif not opposite_name and flip_values:
                    # Center bone (no suffix)
                    bone.location = flip_value(bone.location)
                    bone.rotation_quaternion.conjugate()
                    bone.rotation_euler = flip_value(bone.rotation_euler)

    return {'FINISHED'}

class MirroredPoseDataItem(bpy.types.PropertyGroup):
    name: StringProperty()
    data: StringProperty()

class POSE_OT_MirrorPose(bpy.types.Operator):
    bl_idname = "pose.mirror_pose"
    bl_label = "Mirror Pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context)

class POSE_OT_MirrorPoseIK(bpy.types.Operator):
    bl_idname = "pose.mirror_pose_ik"
    bl_label = "Mirror Pose (Suits IK)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context, ik_mode=True)

class POSE_OT_MirrorPoseUnflipped(bpy.types.Operator):
    bl_idname = "pose.mirror_pose_unflipped"
    bl_label = "Mirror Pose (Unflipped)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context, flip_values=False)

class POSE_OT_CopyPose(bpy.types.Operator):
    bl_idname = "pose.copy_pose"
    bl_label = "Copy Pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context, copy_mode=True)

class POSE_OT_PasteMirrorPose(bpy.types.Operator):
    bl_idname = "pose.paste_mirror_pose"
    bl_label = "Paste Mirror Pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context, paste_mode=True)

class POSE_OT_PasteMirrorPoseUnflipped(bpy.types.Operator):
    bl_idname = "pose.paste_mirror_pose_unflipped"
    bl_label = "Paste Mirror Pose (Unflipped)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return mirror_pose(context, flip_values=False, paste_mode=True)

class VIEW3D_PT_MirrorPosePanel(bpy.types.Panel):
    bl_label = "Mirror Pose Tools"
    bl_idname = "VIEW3D_PT_mirror_pose_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("pose.mirror_pose")
        layout.operator("pose.mirror_pose_ik")
        layout.operator("pose.mirror_pose_unflipped")
        layout.operator("pose.copy_pose")
        layout.operator("pose.paste_mirror_pose")
        layout.operator("pose.paste_mirror_pose_unflipped")

classes = (
    MirroredPoseDataItem,
    POSE_OT_MirrorPose,
    POSE_OT_MirrorPoseIK,
    POSE_OT_MirrorPoseUnflipped,
    POSE_OT_CopyPose,
    POSE_OT_PasteMirrorPose,
    POSE_OT_PasteMirrorPoseUnflipped,
    VIEW3D_PT_MirrorPosePanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mirrored_pose_data = CollectionProperty(type=MirroredPoseDataItem)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mirrored_pose_data

if __name__ == "__main__":
    register()