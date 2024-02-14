from Converter.Prims import ZCylinder
import gmsh

def test_display_prim():
    a = ZCylinder(3, [0.0, 0.0, 0.39])

def main():
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    gmsh.option.setNumber("Mesh.MeshSizeMin", 0.4)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 0.4)


    test_display_prim()

    gmsh.model.occ.synchronize()
    gmsh.fltk.run()
    gmsh.finalize()