import bpy
from bpy.types import Panel, Menu, Operator
from . import _Util
from . import _MenuPose
# --------------------------------------------------------------------------------
# オブジェクトモードメニュー
# --------------------------------------------------------------------------------
def MenuPrimary(pie, context):
    box = pie.split().box()
    box.label(text = 'Object')
    _Util.layout_operator(box, _MenuPose.OT_ClearTransform.bl_idname, label="Clear Pose Transform", isActive=_Util.is_armature_in_selected())
    _Util.layout_operator(box, "wiggle.reset", label="Wiggle2: ResetPhysics") # if imported

# --------------------------------------------------------------------------------
def MenuSecondary(pie, context):
    root = pie.split().row()
    box = root.split(factor=1.0).box()
    box.label(text = 'File')
    box.operator("import_scene.fbx")
    box.operator("screen.userpref_show")
    box.operator(OT_ReinstallAddon.bl_idname)
    # box = root.split(factor=1.0).box()

# --------------------------------------------------------------------------------
class OT_ReinstallAddon(bpy.types.Operator):
    bl_idname = "op.reinstall_addon"
    bl_label = "Reinstall Addon"
    def execute(self, context):
        prefs = _Util.get_prefs()
        path_addon = prefs.pass_addon
        if not path_addon:
            _Util.show_msgbox("required setup addon path in preferences")
            return {'FINISHED'}
        addon_name = "my_pie_menu_ever"
        bpy.ops.preferences.addon_remove(module=addon_name)
        bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_install(filepath=path_addon)
        bpy.ops.preferences.addon_enable(module=addon_name)
        _Util.get_prefs().pass_addon = path_addon
        _Util.show_msgbox("Reinstalled!")
        return {'FINISHED'}
# --------------------------------------------------------------------------------
classes = (
    OT_ReinstallAddon,
)
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
