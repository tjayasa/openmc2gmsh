import gmsh

gmsh.initialize()
factory = gmsh.model.occ
factory.add_sphere(-1,0,0,1,0)
factory.add_sphere(1,0,0,1,1)
factory.add_sphere(0,-1,0,1,2)


# print(factory.fuse([(3,0)],[(3,1)], removeObject = False, removeTool = False))
# print(factory.intersect([(3,0)],[(3,1),(3,2)], removeObject = False, removeTool = False))
factory.synchronize()
gmsh.model.addPhysicalGroup(3,[0,1], 3, "0 + 1")
gmsh.model.addPhysicalGroup(3,[0,1,2],3, "everything")

# factory.intersect([(3,2)],[(3,3)])
factory.synchronize()

gmsh.fltk.run()
gmsh.finalize()