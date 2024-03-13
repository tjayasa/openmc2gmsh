import gmsh
from Converter.Prims import Prims
    
class Entity:
    # self.primatives: List[Prims]
    # self.id:
    bounding_box = None
    ID_OFFSET = 20000
    def __init__(self, id: int, region: list[int], material: int, name: str = "", universe: int = 0):
        """Entity will initialize gmsh if not already intialized."""
        self.id = id + 200000
        self.primIDs: list[int] = list(map(lambda tag : tag if tag > 0 else Prims.ORIENTATION_OFFSET - tag,
                         region))
        
        if not gmsh.is_initialized():
            gmsh.initialize()

        if Entity.bounding_box is None:
            Entity.bounding_box = gmsh.model.occ.add_box(-Prims.BOUNDING_VALUE/2,  # corner.x
                                                -Prims.BOUNDING_VALUE/2,           # corner.y
                                                -Prims.BOUNDING_VALUE/2,           # corner.z
                                                Prims.BOUNDING_VALUE,              # dx
                                                Prims.BOUNDING_VALUE,              # dy
                                                Prims.BOUNDING_VALUE,              # dz
                                                0)                                 # tag = 0

    def create_intersection(self):
        """ Calls the Gmsh api to store the intersection in self.mesh """
        if len(self.primIDs) < 2:
            # map value to itself
            return
        print(self.id)
        print(self.primIDs)
        # primIDs.append(0)
        # read_xml("OpenMC_Examples/pincellGeometry.xml")
        # tags = gmsh.model.occ.intersect([(3,primIDs[0])], [(3,i) for i in primIDs[1:]],   # intersect tags
        #                          tag = entity_id,                       # tag
        #                          removeObject=False,
        #                          removeTool=False)
        
        # tags = gmsh.model.occ.intersect([(3,primIDs[0])], [(3,i) for i in primIDs[1:]],   # intersect tags
        #                          removeObject=False,
        #                          removeTool=False)
        write_tag = self.id + Prims.ORIENTATION_OFFSET
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
        
        #if write_tag == entity_id + Prims.ORIENTATION_OFFSET:
            #rewrite id to not orienttion OFFSET
        
        # gmsh.model.occ.intersect()
        
    
    def write_xml(self):
        """Write entity to the XML"""

    
    
    

