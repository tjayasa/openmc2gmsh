import gmsh
from Converter.Prims import Prims
    
class Entity:
    # self.primatives: List[Prims]
    # self.id:
    ID_OFFSET = 200000
    def __init__(self, id: int, region: list[int], material: int, name: str = "", universe: int = 0):
        """Entity will initialize gmsh if not already intialized."""
        self.id = id + Entity.ID_OFFSET
        self.primIDs: list[int] = list(map(lambda tag : tag if tag > 0 else Prims.ORIENTATION_OFFSET - tag,
                         region))
        
        if not gmsh.is_initialized():
            gmsh.initialize()
            
    def create_intersection(self):
        """ Calls the Gmsh api to store the intersection in self.mesh """
        # outtag = gmsh.model.occ.copy([(3,self.primIDs[0])])
        if len(self.primIDs) == 1:
            # print(self.primIDs[0])
            # replace save_id with the cheapest 3d mesh to create
            gmsh.model.occ.add_sphere(0,0,0,Prims.BOUNDING_VALUE,self.id)
            temp = gmsh.model.occ.copy([(3,self.primIDs[0])])
            gmsh.model.occ.remove([(3,self.id)])
            gmsh.model.occ.intersect( temp ,[(3,0)],
                                        tag=self.id,
                                        removeObject=True,
                                        removeTool=False)
            return
        write_tag = self.id + Prims.ORIENTATION_OFFSET if len(self.primIDs) % 2 == 0 else self.id
        outtag, __ = gmsh.model.occ.intersect( [(3,self.primIDs[0])],[(3,self.primIDs[1])],
                                              tag=write_tag,
                                              removeObject=False,
                                              removeTool=False)

        for id in self.primIDs[2:]:
            write_tag = self.id + (Prims.ORIENTATION_OFFSET if write_tag == self.id else 0)
            gmsh.model.occ.intersect([(3,self.id + Prims.ORIENTATION_OFFSET 
                                            if self.id == write_tag else self.id)],
                                        [(3,id)],
                                        tag = write_tag,
                                        removeObject=True,
                                        removeTool=False)
        
        # intersect with the boudning box (id = 0)
        gmsh.model.occ.intersect([(3,self.id + Prims.ORIENTATION_OFFSET)],[(3,0)],
                                        tag = self.id,
                                        removeObject=True,
                                        removeTool=False)
        
        #if write_tag == entity_id + Prims.ORIENTATION_OFFSET:
            #rewrite id to not orienttion OFFSET
        
        # gmsh.model.occ.intersect()
        
    
    def write_xml(self):
        """Write entity to the XML"""

    
    
    

