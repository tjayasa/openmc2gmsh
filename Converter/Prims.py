import gmsh
import numpy as np

class Prims:
    BOUNDING_VALUE = 100
    LARGE_VALUE = BOUNDING_VALUE * 10
    # ORIENTATION_OFFSET = 1073741824
    ORIENTATION_OFFSET = 100000
    maxID: int = 1 #index 0 = bounding box
    idMap: dict = {}
    def __init__(self, id: int, coeffs, albedo, name, boundry_type):
        Prims.maxID += 1
        self.id: int = id
        self.coeffs: list[float] = coeffs
        self.albedo: float = albedo
        self.name: str = name
        self.boundry_type: str = boundry_type
        
        if not gmsh.is_initialized():
            gmsh.initialize()
        
class Plane(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float = 0.0, name: str = "", boundry_type: str = ""):
        super().__init__(id, coeffs, albedo, name, boundry_type)
        self.__make_large_box()
        # self.__make_large_box(np.ndarray(self.coeffs[:3]),
        #                         np.ndarray([0,0,self.coeffs[3]]))
        
    def __make_large_box(self):

        point_arb = None  # pick an arbitrary point not on the normal
        if self.coeffs[0] == 0:
            point_arb = np.array([1,0,0])
        elif self.coeffs[1] == 0:
            point_arb = np.array([0,1,0])
        elif self.coeffs[2] == 0:
            point_arb = np.array([0,0,1])

        # define normal vector of the plane
        normal = np.array(self.coeffs[0:3])
        normal = normal / np.linalg.norm(normal)
        
        # find two vectors that live on the plane (dx,dy)
        proj = np.dot(normal, point_arb) * normal
        dx = point_arb - proj
        dx = dx / np.linalg.norm(dx)
        dy = np.cross(normal,dx)
        dy = dy / np.linalg.norm(dy)
        print("dx = ", dx)
        print("dy = ", dy)
        print("norm = ", normal)

        # find an arbitrary point on the plane
        point = None
        if normal[2] != 0:
            point = np.array([0.0,0.0,self.coeffs[3]/self.coeffs[2]])
        elif normal[1] != 0:
            point = np.array([0.0,self.coeffs[3]/self.coeffs[1],0.0])
        elif normal[0] != 0:
            point = np.array([self.coeffs[3]/self.coeffs[0],0.0,0.0])

        bot_left = Prims.LARGE_VALUE * (-dx - dy) + point
        dir_vec_pos = 2 * Prims.LARGE_VALUE * (dx + dy + normal)
        dir_vec_neg = 2 * Prims.LARGE_VALUE * (dx + dy - normal)
        print("bot_left = ",bot_left)
        print("dxyz = ", dir_vec_neg)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_pos[0],dir_vec_pos[1],dir_vec_pos[2],self.id)
        gmsh.model.occ.add_box(bot_left[0],bot_left[1],bot_left[2],dir_vec_neg[0],dir_vec_neg[1],dir_vec_neg[2],Prims.ORIENTATION_OFFSET + self.id)

class ZCylinder(Prims):
    def __init__(self, id: int, coeffs: list[float], albedo: float = 0.0, name: str = "", boundry_type: str = ""):
        super().__init__(id, coeffs, albedo, name, boundry_type)
        self.__make_large_z_cylinder(coeffs[0],coeffs[1],coeffs[2])
    
    def __make_large_z_cylinder(self, x: float, y:float , r:float):
        factory = gmsh.model.occ
        factory.add_cylinder(x, y, -Prims.LARGE_VALUE, 0, 0, 2 * Prims.LARGE_VALUE, r, self.id)
        factory.add_box(-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,
                               Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,self.id + 1)
        gmsh.model.occ.cut([(3,self.id + 1)],[(3,self.id)], Prims.ORIENTATION_OFFSET + self.id, True, False)
        # factory.synchronize()
        # gmsh.fltk.run()