import gmsh
gmsh.initialize()
factory = gmsh.model.occ

factory.add_disk(-1,0,0,1.5,1.5)
factory.add_disk(0,1,0,1.5,1.5)
factory.add_disk(1,0,0,1.5,1.5)
factory.add_disk(10,0,0,1.5,1.5)

id = 100
temp = factory.intersect([(2,1)], [(2,2)],
                         tag=id,
                         removeObject=False, removeTool=False)
print('tags = ', temp[0])
print('map = ', temp[1])

temp = factory.intersect([(2,id)], [(2,3)],
                         tag=id+1,
                         removeObject=True, removeTool=False)
print('tags = ', temp[0])
print('map = ', temp[1])
factory.synchronize()
gmsh.fltk.run()
gmsh.finalize()