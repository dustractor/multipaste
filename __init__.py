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
class MULTIPASTE_OT_multipaste(bpy.types.Operator):
    bl_idname = "multipaste.multipaste"
    bl_label = "multi paste operator"
    def execute(self,context):
        paths = []
        for f in context.window_manager.clipboard.splitlines():
            if f.startswith("file://"):
                f = f[7:]
                if pathlib.Path(f).is_file():
                    paths.append(f)
        print("multipaste paths found:",paths)
        for path in paths:
            if path.endswith(".svg"):
                bpy.ops.import_curve.svg(filepath=path)
            elif path.endswith(".obj"):
                bpy.ops.import_scene.obj(filepath=path)
            elif path.endswith(".dae"):
                bpy.ops.wm.collada_import(filepath=path)
            elif path.endswith(".ply"):
                bpy.ops.import_mesh.ply(filepath=path)
            elif path.endswith(".stl"):
                bpy.ops.import_mesh.stl(filepath=path)
            else:
                print("recieved a file whose extension has no handler:")
                print("path:",path)
        print("multipaste ok")
        return {"FINISHED"}


def disp(self,context):
    self.layout.operator("multipaste.multipaste")

def register():
    list(map(bpy.utils.register_class,_()))
    bpy.types.VIEW3D_MT_object.append(disp)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(disp)
    list(map(bpy.utils.unregister_class,_()))

