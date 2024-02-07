import gmsh
import numpy as np

BOUNDING_VALUE = 10000
LARGE_VALUE = BOUNDING_VALUE * 10
ORIENTATION_OFFSET = 2147483648

class Prims:
    def __init__(self, id, coeffs, albedo, name, type):
        Prims.maxID: int = 0
        self.id: int = id
        self.coeffs: list[float] = coeffs
        self.albedo: float = albedo
        self.name: str = name
        self.boundry_type: str = type
        
class Plane(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float, name: str, type: str):
        super().__init__(id, coeffs, albedo, name, type)
        self.__make_large_box(np.ndarray([coeffs[0], coeffs[1], coeffs[2]]),
                                np.ndarray([0,0,coeffs[3]]))
        
    def __make_large_box(self, normal: np.ndarray, vert_shift: np.ndarray):
        point = np.array([1,0,0]) if normal[0] != 0 else np.array([0,1,0]) # arbitrary point not on normal
        normal = normal / np.linalg.norm(normal)
        proj = np.dot(normal, point)
        point_a = point - proj
        point_a = point_a / np.linalg.norm(point_a)
        point_b = np.cross(normal,point_a)
        point_b = point_b / np.linalg.norm(point_b)
        bot_left = LARGE_VALUE * (-point_a - point_b) + vert_shift
        dir_vec_pos = LARGE_VALUE * (point_a + point_b + normal)
        dir_vec_neg = LARGE_VALUE * (point_a + point_b + normal)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_pos[0],dir_vec_pos[1],dir_vec_pos[2],self.id)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_neg[0],dir_vec_neg[1],dir_vec_neg[2],ORIENTATION_OFFSET + self.id)

class ZCylinder(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float, name: str, type: str):
        super().__init__(id, coeffs, name, type)
    
    def __make_large_z_cylinder(self, x: float, y:float , r:float):
        gmsh.model.occ.add_cylinder(x, y, -LARGE_VALUE, 0, 0, 2 * LARGE_VALUE, r, self.id)
        gmsh.model.occ.add_box(-BOUNDING_VALUE/2,-BOUNDING_VALUE/2,-BOUNDING_VALUE/2,
                               BOUNDING_VALUE,BOUNDING_VALUE,BOUNDING_VALUE,self.id + 1)
        gmsh.model.occ.cut([(3,self.id)],[(3,self.id+1)],ORIENTATION_OFFSET + self.id, False, True)

        
        



