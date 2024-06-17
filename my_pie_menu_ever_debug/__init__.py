bl_info = {
    "name": "MyBestPieMenuEVER_debug",
    "author": "emptybraces",
    "version": (1, 0),
    "blender": (3, 6, 1),
    "location": "3D View",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}
import bpy
import sys

class OT_ReinstallAddon(bpy.types.Operator):
    bl_idname = "mpmei.reinstall_addon"
    bl_label = "Reinstall Addon"
    def execute(self, context):
        exist_module = False
        # 検索
        addon_name = "my_pie_menu_ever"
        for i in bpy.context.preferences.addons.keys():
            if "pie_menu_ever" in i:
                addon_anme = i
                break
        if is_addon_enabled(addon_name):
            #if 'my_pie_menu_ever._AddonPreferences' in sys.modules:
            from my_pie_menu_ever import _AddonPreferences
            if _AddonPreferences:
                ref = _AddonPreferences.Accessor.get_ref()
                if ref:
                    exist_module = True
                    self.dict = ref.dict()
        bpy.ops.preferences.addon_remove(module=addon_name)
        bpy.ops.preferences.addon_refresh()
        bpy.ops.preferences.addon_install(filepath="D:/googledrive/blender/plugin/MyBestPieMenuEver/my_pie_menu_ever-1.3.1.zip")
        # 再度検索
        for i in bpy.context.preferences.addons.keys():
            if "pie_menu_ever" in i:
                addon_anme = i
                break
        bpy.ops.preferences.addon_enable(module=addon_name)
        if exist_module:
            _AddonPreferences.Accessor.get_ref().dict_apply(self.dict)
            self.dict = None
        def draw(self, context):
            self.layout.label(text="reinstalled!")
        context.window_manager.popup_menu(draw)
        return {'FINISHED'}

def is_addon_enabled(addon_name):
    # 現在有効になっているアドオンのリストを取得
    enabled_addons = bpy.context.preferences.addons.keys()
    return addon_name in enabled_addons

classes = (
    OT_ReinstallAddon,
)
addon_keymaps = []
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('mpmei.reinstall_addon', 'W', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
if __name__ == "__main__":
    register()