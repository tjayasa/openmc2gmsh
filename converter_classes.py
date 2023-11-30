import numpy as np
from converter_functions import *

id_counter = 0

class surface:
    def __init__(self, surface_type):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the global ID counter

        self.type = surface_type
        self.boundaryType = None
        self.boundingLines = []
        self.boundingLineIDs = []
        self.coeffs = {}

    def __str__(self):
        return f"Surface of Type {self.type} with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"
    
    def setPlaneCoefficients(self, a, b, c, d):
        self.coeffs["a"] = a
        self.coeffs["b"] = b
        self.coeffs["c"] = c
        self.coeffs["d"] = d

    def setCylinderCoefficients(self, x0, y0, z0, r):
        self.coeffs["x0"] = a
        self.coeffs["y0"] = b
        self.coeffs["z0"] = c
        self.coeffs["r"] = d
    
    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id

    def addBoundingLine(self, input_line):
        self.boundingLines.append(input_line)
        self.boundingLineIDs.append(input_line.gmsh_id)



class line:
    def __init__(self, line_type):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the global ID counter

        self.type = line_type
        self.boundingPoints = []
        self.coeffs = {}

    def setCoefficients(self, x0, y0, z0, alpha, beta, epsilon):
        self.coeffs["x0"] = x0
        self.coeffs["y0"] = y0
        self.coeffs["z0"] = z0
        self.coeffs["alpha"] = alpha
        self.coeffs["beta"] = beta
        self.coeffs["epsilon"] = epsilon

    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id

    def addBoundingPoint(self, input_point):
        self.boundingPoints.append(input_point)



class point:
    def __init__(self, x, y, z):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the ID counter

        self.x = x
        self.y = y
        self.z = z

        self.coeffs = {}

    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id