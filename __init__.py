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
        try:
            import win32clipboard
        except ImportError:
            print("is pywin32 installed? (try doing that)")
        _list = []
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData()
            _list += [text]

        except TypeError:
            _list = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        finally:
            win32clipboard.CloseClipboard()
        for text in _list:
            try:
                exists = pathlib.Path(text).exists()
            except OSError:
                print("The following clipboard content does not appear to be a list of files:")
                print("-------->")
                print(text)
                print("<--------")
            if text.endswith(".svg"):
                bpy.ops.import_curve.svg(filepath=text)
            elif text.endswith(".obj"):
                bpy.ops.import_scene.obj(filepath=text)
            elif text.endswith(".dae"):
                bpy.ops.wm.collada_import(filepath=text)
            elif text.endswith(".ply"):
                bpy.ops.import_mesh.ply(filepath=text)
            elif text.endswith(".stl"):
                bpy.ops.import_mesh.stl(filepath=text)
            else:
                print("recieved a file whose extension has no handler:")
                print(text)


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

