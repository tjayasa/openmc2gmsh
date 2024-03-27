import gmsh
from Converter.Prims import Prims

class InvalidRegionError(Exception):
    pass

class Entity:
    # self.primatives: List[Prims]
    # self.id:
    ID_OFFSET = 200000
    def __init__(self, id: int, region: list[int], material: int, name: str = "", universe: int = 0):
        """Entity will initialize gmsh if not already intialized."""
        self.tags = []
        self.id = id + Entity.ID_OFFSET
        self.region: list = list(map(lambda tag : tag if type(tag) != int else [(3,tag)] if tag > 0 else [(3,Prims.ORIENTATION_OFFSET - tag)],
                         region))

        if not gmsh.is_initialized():
            gmsh.initialize()

    def create_intersection(self):
        """ Calls the Gmsh api to store the intersection in self.mesh """
        # outtag = gmsh.model.occ.copy([(3,self.primIDs[0])])
        if len(self.region) == 1:
            # print(self.primIDs[0])
            # replace save_id with the cheapest 3d mesh to create
            gmsh.model.occ.add_sphere(0,0,0,Prims.BOUNDING_VALUE,self.id)
            # print(self.region[0])
            temp = gmsh.model.occ.copy(self.region[0])
            gmsh.model.occ.remove([(3,self.id)])
            gmsh.model.occ.intersect( temp ,[(3,0)],
                                        tag=self.id,
                                        removeObject=True,
                                        removeTool=False)
            return
        
        # FIXME: creates additional geometry on every subsequent intersection call --> solution: only push copies of Prims
        self.tags = [(3,Prims.BOUNDING_BOX_TAG)]
        operation_stack = []
        operation_stack.append(gmsh.model.occ.copy(self.tags))
        operation_stack.append(gmsh.model.occ.copy(self.region[0]) if type(self.region[0]) == list else self.region[0])
        index = 1
        while(len(operation_stack) > 1):
            # print(operation_stack)
            
            # error cases:
            if operation_stack[0] == '|':
                raise InvalidRegionError("invalid expression sequence: ^|*")

            if (operation_stack[-2] == '(' or operation_stack[-1] == '(') and index >= len(self.region):
                print(operation_stack)
                raise InvalidRegionError("invalid expression sequence: (.$ | .($")
            
            if operation_stack[-2] == '~' and operation_stack[-1] == '|':
                raise InvalidRegionError("invalid expression sequence: ~|")

            if operation_stack[-2] == '|' and operation_stack[-1] == '|':
                raise InvalidRegionError("invalid expression sequence: ||")
            
            if operation_stack[-2] == '|' and operation_stack[-1] == ')':
                raise InvalidRegionError("invalid expression sequence: |)")
            
            if operation_stack[-2] == '(' and operation_stack[-1] == '|':
                raise InvalidRegionError("invalid expression sequence: (|")
            
            if operation_stack[-1] == '|' and index >= len(self.region):
                raise InvalidRegionError("invalid expression sequence: *|$")
            
            if operation_stack[-1] == '~' and index >= len(self.region):
                raise InvalidRegionError("invalid expression sequence: *~$")
            
            # case : )
            if operation_stack[-1] == ')':
                operation_stack.pop()
                while operation_stack[-2] != '(':
                    if type(operation_stack[-1]) == list and type(operation_stack[-2]) == list:
                        output_tags, __ = gmsh.model.occ.intersect(operation_stack[-1], operation_stack[-2])
                        operation_stack.pop()
                        operation_stack.pop()
                        operation_stack.append(output_tags)
                    if operation_stack[-2] == '~':
                        if type(operation_stack[-1]) != list:
                            raise InvalidRegionError()
                        temp_out, __ = gmsh.model.occ.intersect([(3,Prims.BOUNDING_BOX_TAG)], operation_stack[-1], removeObject=False, removeTool=True)
                        output_tags, __ = gmsh.model.occ.cut([(3,Prims.BOUNDING_BOX_TAG)], temp_out, removeObject=False, removeTool=True)
                        operation_stack.pop()
                        operation_stack.pop()
                        operation_stack.append(output_tags)
                    if operation_stack[-2] == '|':
                        if type(operation_stack[-1]) != list or type(operation_stack[-3]) != list:
                            raise InvalidRegionError()
                        output_tags, __ = gmsh.model.occ.fuse(operation_stack[-1], operation_stack[-3])
                        operation_stack.pop()
                        operation_stack.pop()
                        operation_stack.pop()
                        operation_stack.append(output_tags)
                operation_stack.pop(-2)
                    
            # case : ()
            elif operation_stack[-2] == '(' and operation_stack[-1] == ')':
                operation_stack.pop()
                operation_stack.pop()
            
            # case : \d\d
            elif type(operation_stack[-1]) == list and type(operation_stack[-2]) == list:
                output_tags, __ = gmsh.model.occ.intersect(operation_stack[-1], operation_stack[-2])
                operation_stack.pop()
                operation_stack.pop()
                operation_stack.append(output_tags)
            
            # case : ~\d
            elif operation_stack[-2] == '~' and type(operation_stack[-1]) == list:
                temp_out, __ = gmsh.model.occ.intersect([(3,Prims.BOUNDING_BOX_TAG)], operation_stack[-1], removeObject=False, removeTool=True)
                output_tags, __ = gmsh.model.occ.cut([(3,Prims.BOUNDING_BOX_TAG)], temp_out, removeObject=False, removeTool=True)
                operation_stack.pop()
                operation_stack.pop()
                operation_stack.append(output_tags)
                
            if index < len(self.region):
                operation_stack.append(gmsh.model.occ.copy(self.region[index]) if type(self.region[index]) == list else self.region[index])
                # operation_stack.append(self.region[index])
                index += 1
                
            
        self.tags = operation_stack[0]
        print(self.tags)
        
        # for id in self.primIDs:
        #     self.tags, __ = gmsh.model.occ.intersect(self.tags, [(3,id)], removeObject=False, removeTool=False)
        # print(self.tags)

        # write_tag = self.id + Prims.ORIENTATION_OFFSET if len(self.primIDs) % 2 == 0 else self.id
        # gmsh.model.occ.add_sphere(0,0,0,Prims.BOUNDING_VALUE,self.id)
        # temp = gmsh.model.occ.copy([(3,self.primIDs[0])])
        # gmsh.model.occ.remove([(3,self.id)])
        # outtag, __ = gmsh.model.occ.intersect( temp,[(3,self.primIDs[1])],
        #                                       tag=write_tag,
        #                                       removeObject=True,
        #                                       removeTool=False)

        # for id in self.primIDs[2:]:
        #     write_tag = self.id + (Prims.ORIENTATION_OFFSET if write_tag == self.id else 0)
        #     gmsh.model.occ.intersect([(3,self.id + Prims.ORIENTATION_OFFSET 
        #                                     if self.id == write_tag else self.id)],
        #                                 [(3,id)],
        #                                 tag = write_tag,
        #                                 removeObject=True,
        #                                 removeTool=False)
        
        # # intersect with the boudning box (id = 0)
        # gmsh.model.occ.intersect([(3,self.id + Prims.ORIENTATION_OFFSET)],[(3,0)],
        #                                 tag = self.id,
        #                                 removeObject=True,
        #                                 removeTool=False)
        
        #if write_tag == entity_id + Prims.ORIENTATION_OFFSET:
            #rewrite id to not orienttion OFFSET
        
        # gmsh.model.occ.intersect()
        
    
    def write_xml(self):
        """Write entity to the XML"""

    
    
    

