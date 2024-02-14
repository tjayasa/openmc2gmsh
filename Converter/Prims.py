import gmsh
import numpy as np

class Prims:
    BOUNDING_VALUE = 10
    LARGE_VALUE = BOUNDING_VALUE * 10
    ORIENTATION_OFFSET = 1073741824
    maxID: int = 1 #index 0 = bounding box
    def __init__(self, coeffs, albedo, name, boundry_type):
        self.id: int = Prims.maxID
        Prims.maxID += 1
        self.coeffs: list[float] = coeffs
        self.albedo: float = albedo
        self.name: str = name
        self.boundry_type: str = boundry_type
        
        if not gmsh.is_initialized():
            gmsh.initialize()
        
class Plane(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float = 0.0, name: str = "", boundry_type: str = ""):
        super().__init__(id, coeffs, albedo, name, type)
        self.__make_large_box(np.ndarray([self.coeffs[0], self.coeffs[1], self.coeffs[2]]),
                                np.ndarray([0,0,self.coeffs[3]]))
        
    def __make_large_box(self, normal: np.ndarray, vert_shift: np.ndarray):
        point = np.array([1,0,0]) if normal[0] != 0 else np.array([0,1,0]) # arbitrary point not on normal
        normal = normal / np.linalg.norm(normal)
        proj = np.dot(normal, point)
        point_a = point - proj
        point_a = point_a / np.linalg.norm(point_a)
        point_b = np.cross(normal,point_a)
        point_b = point_b / np.linalg.norm(point_b)
        bot_left = Prims.LARGE_VALUE * (-point_a - point_b) + vert_shift
        dir_vec_pos = Prims.LARGE_VALUE * (point_a + point_b + normal)
        dir_vec_neg = Prims.LARGE_VALUE * (point_a + point_b + normal)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_pos[0],dir_vec_pos[1],dir_vec_pos[2],self.id)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_neg[0],dir_vec_neg[1],dir_vec_neg[2],Prims.ORIENTATION_OFFSET + self.id)

class ZCylinder(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float = 0.0, name: str = "", boundry_type: str = ""):
        super().__init__(id, coeffs, name, boundry_type)
        self.__make_large_z_cylinder(coeffs[0],coeffs[1],coeffs[2])
    
    def __make_large_z_cylinder(self, x: float, y:float , r:float):
        factory = gmsh.model.occ
        factory.add_cylinder(x, y, -Prims.LARGE_VALUE, 0, 0, 2 * Prims.LARGE_VALUE, r, self.id)
        # factory.synchronize()
        # gmsh.fltk.run()
        factory.add_box(-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,
                               Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,Prims.ORIENTATION_OFFSET + self.id)
        # factory.synchronize()
        # gmsh.fltk.run()
        gmsh.model.occ.cut([(3,Prims.ORIENTATION_OFFSET + self.id)],[(3,self.id)], self.id + 1, True, False)
        # factory.synchronize()
        # gmsh.fltk.run()
        
        # gmsh.model.occ.synchronize()
        
        print(gmsh.model.getEntities(3))