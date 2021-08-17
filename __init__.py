bl_info = {
    "name": "Multipaste",
    "blender": (2,80,0),
    "version": (0,1),
    "category":"Import-Export"
}
import bpy,pathlib

def _(a=None,b=[]):
    if a:
        b += [a]
        return a
    else:
        return b

@_
class MultiPastePrefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    def draw(self,context):
        self.layout.operator("multipaste.install_module")
@_
class MULTIPASTE_OT_install_module(bpy.types.Operator):
    bl_idname = "multipaste.install_module"
    bl_label = "install modules"
    module_name: bpy.props.StringProperty(default="pywin32")
    def execute(self,context):
        import subprocess
        import ensurepip
        import sys
        ensurepip.bootstrap()
        python_binary = sys.executable
        t = subprocess.check_call([python_binary,"-m","pip","install",self.module_name])
        print("t:",t)
        return {"FINISHED"}

@_
class MULTIPASTE_OT_multipaste(bpy.types.Operator):
    bl_idname = "multipaste.multipaste"
    bl_label = "multi paste operator"
    def execute(self,context):
        import win32clipboard
        win32clipboard.OpenClipboard()
        t = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        win32clipboard.CloseClipboard()
        for f in t:
            if f.endswith(".svg"):
                bpy.ops.import_curve.svg(filepath=f)
                print("f:",f)
            elif f.endswith(".obj"):
                bpy.ops.import_scene.obj(filepath=f)
            elif f.endswith(".dae"):
                bpy.ops.wm.collada_import(filepath=f)
            elif f.endswith(".ply"):
                bpy.ops.import_mesh.ply(filepath=f)

        print("ok")
        return {"FINISHED"}


def disp(self,context):
    self.layout.operator("multipaste.multipaste")

def register():
    list(map(bpy.utils.register_class,_()))
    bpy.types.VIEW3D_MT_object.append(disp)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(disp)
    list(map(bpy.utils.unregister_class,_()))

