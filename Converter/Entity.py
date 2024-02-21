import gmsh
from Converter.Prims import Prims
    
class Entity:
    # self.primatives: List[Prims]
    # self.id:
    count: int = 0
    bounding_box = None

    def __init__(self, prims: list[Prims]):
        """Entity will initialize gmsh if not already intialized."""
        self.primatives: list[Prims] = prims
        self.id = Entity.count
        self.mesh = None
        
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

    def create_intersection(self, primIDs: list[int], entity_id: int):
        """Calls the Gmsh api to store the intersection in self.mesh"""
        #TODO: call Gmsh api to set self.mesh = GmshObject
        gmsh.model.occ.intersect([(3,i) for i in primIDs], [(3, 0)], removeObject=False, removeTool=False)
        # gmsh.model.occ.intersect()
        
    
    def write_xml(self):
        """Write entity to the XML"""

    
    
    

