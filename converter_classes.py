import numpy as np
from converter_functions import *

id_counter = 1 #id = 0 is reserved for the void volume/surface

class volume:
    """Base Class for 3-dimensional objects (i.e. cells in OpenMC)"""

    def __init__(self, volume_type):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the global ID counter

        #The ID of the object constructed after all of the boolean operations have been carried out:
        self.final_id = None

        self.type = volume_type
        self.material= None
        self.name = None
        self.universe = None
        self.boundingSurfaces = [None] # Using None in place of the void volume may be a bad idea, but we'll see if it has any consequences later
        self.boundingSurfaceOMCIDs = [None]
        self.boundingSurfaceGmshIDs = [0]
        self.boundingSurfaceRelationships = [-1]
        self.coeffs = {}

    def __str__(self):
        return f"Volume {self.name} of Type {self.type} with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"
    
    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id

    def setFinalID(self, id):
        self.final_id = id

    def addBoundingSurface(self, input_line):
        self.boundingLines.append(input_line)
        self.boundingLineIDs.append(input_line.gmsh_id)

    def findAllBoundingSurfaces(self,list_of_surfaces):

        # This double for loop is almost certainly incredibly inefficient, but is the simplest
        # implementation and will do for the time being.
        for OMCID in self.boundingSurfaceOMCIDs:
            if OMCID is None:
                    continue

            for current_surface in list_of_surfaces:
                if current_surface.OMC_id is None:
                    break
                
                if int(current_surface.OMC_id) == int(OMCID):
                    #print("Match Found")
                    self.boundingSurfaces.append(current_surface)
                    self.boundingSurfaceGmshIDs.append(current_surface.gmsh_id)

        #print(f"Bounding Surfaces for Cell {self.OMC_id}:", self.boundingSurfaceGmshIDs)

    def write_gmsh_representation(self, dimensionality):

        global id_counter

        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        current_id = 0

        if dimensionality == 3:

            #output_string = output_string + circle_1.write_gmsh_representation(dimensionality)
            #print(len(self.boundingSurfaces))
            hasPrintedBoundaryIntersection = False
            for index in range(1,len(self.boundingSurfaces)):

                if ("boundary" in self.boundingSurfaces[index].type): # if the bounding surface is a boundary
                    if not hasPrintedBoundaryIntersection: # if the boundary intersection has yet to be printed

                        if index == 1:
                            current_id = 0
                        else:
                            output_string = output_string + f"BooleanIntersection({id_counter})" +  " = {Volume{" + f"{current_id}" + "};}{Volume{0};};\n"

                            current_id = id_counter
                            id_counter = id_counter + 1 #increment id counter

                        hasPrintedBoundaryIntersection = True

                elif self.boundingSurfaceRelationships[index] == -1:
                    
                    if index == 1:
                        current_id = self.boundingSurfaces[1].gmsh_id
                    else:
                        output_string = output_string + f"BooleanIntersection({id_counter})" +  " = {Volume{" + f"{current_id}" + "};}{" + f"Volume{'{'}{self.boundingSurfaceGmshIDs[index]}" + "};};\n"

                        current_id = id_counter
                        id_counter = id_counter + 1 #increment id counter

                elif self.boundingSurfaceRelationships[index] == 1:

                    output_string = output_string + f"BooleanDifference({id_counter})" +  " = {Volume{" + f"{current_id}" + "};}{" + f"Volume{'{'}{self.boundingSurfaceGmshIDs[index]}" + "};};\n"

                    current_id = id_counter
                    id_counter = id_counter + 1 #increment id counter

                else:
                    raise ValueError("Invalid Bounding Surface Relationship Encountered")


            output_string = output_string + "Physical Volume" + f'("{self.name}")' + f"= {'{'}{current_id}{'}'};\n"
            id_counter = id_counter + 1

            self.setFinalID(current_id)

        elif dimensionality == 2:

            #print(len(self.boundingSurfaces))
            hasPrintedBoundaryIntersection = False
            for index in range(1,len(self.boundingSurfaces)):

                if ("boundary" in self.boundingSurfaces[index].type): # if the bounding surface is a boundary
                    if not hasPrintedBoundaryIntersection: # if the boundary intersection has yet to be printed

                        if index == 1:
                            current_id = 0
                        else:
                            output_string = output_string + f"BooleanIntersection({id_counter})" +  " = {Surface{" + f"{current_id}" + "};}{Surface{0};};\n"

                            current_id = id_counter
                            id_counter = id_counter + 1 #increment id counter

                        hasPrintedBoundaryIntersection = True

                elif self.boundingSurfaceRelationships[index] == -1:
                    
                    if index == 1:
                        current_id = self.boundingSurfaces[1].gmsh_id
                    else:
                        output_string = output_string + f"BooleanIntersection({id_counter})" +  " = {Surface{" + f"{current_id}" + "};}{" + f"Surface{'{'}{self.boundingSurfaceGmshIDs[index]}" + "};};\n"

                        current_id = id_counter
                        id_counter = id_counter + 1 #increment id counter

                elif self.boundingSurfaceRelationships[index] == 1:

                    output_string = output_string + f"BooleanDifference({id_counter})" +  " = {Surface{" + f"{current_id}" + "};}{" + f"Surface{'{'}{self.boundingSurfaceGmshIDs[index]}" + "};};\n"

                    current_id = id_counter
                    id_counter = id_counter + 1 #increment id counter

                else:
                    raise ValueError("Invalid Bounding Surface Relationship Encountered")

            output_string = output_string + "Physical Surface" + f'("{self.name}")' + f"= {'{'}{current_id}{'}'};\n"
            id_counter = id_counter + 1

            self.setFinalID(current_id)

        return(output_string)

class surface:
    """Base Class for 2-dimensional objects (i.e. surfaces in OpenMC)"""

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
        #self.positiveHalfSpace = None
        #self.negativeHalfSpace = None

    def __str__(self):
        return f"Surface of Type {self.type} with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"
    
    def setPlaneCoefficients(self, a, b, c, d):
        self.coeffs["a"] = a
        self.coeffs["b"] = b
        self.coeffs["c"] = c
        self.coeffs["d"] = d
    
    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id

    def addBoundingLine(self, input_line):
        self.boundingLines.append(input_line)
        self.boundingLineIDs.append(input_line.gmsh_id)


class cylinder(surface):
    """Child Class for Cylindrical Surfaces"""

    def __str__(self):
        return f"Cylinder Surface with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setCoefficients(self, x0, y0, z0, alpha, beta, epsilon, r, h=None):
        self.coeffs["x0"] = x0
        self.coeffs["y0"] = y0
        self.coeffs["z0"] = z0
        self.coeffs["alpha"] = alpha
        self.coeffs["beta"] = beta
        self.coeffs["epsilon"] = epsilon
        self.coeffs["r"] = r
        self.coeffs["h"] = h

    def setBaseAndHeight(self, bounding_dimensions):
        xmin = bounding_dimensions[0][0]
        xmax = bounding_dimensions[1][0]
        ymin = bounding_dimensions[2][0]
        ymax = bounding_dimensions[3][0]
        zmin = bounding_dimensions[4][0]
        zmax = bounding_dimensions[5][0]

        if self.coeffs["h"] is None:
            match self.type:
                case "x-cylinder":
                    self.coeffs["h"] = xmax-xmin
                case "y-cylinder":
                    self.coeffs["h"] = ymax-ymin
                case "z-cylinder":
                    self.coeffs["h"] = zmax-zmin
                case _:
                    raise ValueError("Invalid Cylinder Type Specified")

        match self.type:
            case "x-cylinder":
                self.coeffs["x0"] = xmin
            case "y-cylinder":
                self.coeffs["y0"] = ymin
            case "z-cylinder":
                self.coeffs["z0"] = zmin
            case _:
                raise ValueError("Invalid Cylinder Type Specified")

        return

    def write_gmsh_representation(self, dimensionality):

        global id_counter

        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        if dimensionality == 3:
            
            output_string = output_string + f"Cylinder({self.gmsh_id}) = " + "{" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}, {self.coeffs['alpha']*self.coeffs['h']}, {self.coeffs['beta']*self.coeffs['h']}, {self.coeffs['epsilon']*self.coeffs['h']}, {self.coeffs['r']}" + "};\n"
                

        elif dimensionality == 2:

            circle_1 = circle("circle")
            circle_1.setOpenMCID(self.OMC_id)
            circle_1.setgmshID(self.gmsh_id)
            circle_1.setCoefficients(self.coeffs["x0"], self.coeffs["y0"], self.coeffs["z0"], 0, 0, 1, self.coeffs["r"])

            output_string = output_string + circle_1.write_gmsh_representation(dimensionality)

        return(output_string)

class sphere(surface):
    """Child Class for Spherical Surfaces"""

    def __str__(self):
        return f"Sphere Surface with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setCoefficients(self, x0, y0, z0, r):
        self.coeffs["x0"] = x0
        self.coeffs["y0"] = y0
        self.coeffs["z0"] = z0
        self.coeffs["r"] = r

    def write_gmsh_representation(self, dimensionality):

        global id_counter

        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        if dimensionality == 3:
            
            output_string = output_string + f"Sphere({self.gmsh_id}) = " + "{" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}, {self.coeffs['r']}" + "};\n"
                

        elif dimensionality == 2:

            print("2D Printing of Sphere is not yet implemented")

        return(output_string)

class torus(surface):
    """Child Class for Toroidal Surfaces"""

    def __str__(self):
        return f"Torus Surface with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setCoefficients(self, x0, y0, z0, alpha, beta, epsilon, major_r, minor_r):
        self.coeffs["x0"] = x0
        self.coeffs["y0"] = y0
        self.coeffs["z0"] = z0
        self.coeffs["alpha"] = alpha
        self.coeffs["beta"] = beta
        self.coeffs["epsilon"] = epsilon
        self.coeffs["major_r"] = major_r
        self.coeffs["minor_r"] = minor_r

    def write_gmsh_representation(self, dimensionality):

        global id_counter

        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        if dimensionality == 3:
            
            output_string = output_string + f"Torus({self.gmsh_id}) = " + "{" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}, {self.coeffs['major_r']}, {self.coeffs['minor_r']}" + "};\n"


            if self.type == "x-torus":
                output_string = output_string + "Rotate{{0,1,0}, {" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}" + "}, Pi/2} {Volume{" + f"{self.gmsh_id}" + "};}\n"
            elif self.type == "y-torus":
                output_string = output_string + "Rotate{{1,0,0}, {" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}" + "}, Pi/2} {Volume{" + f"{self.gmsh_id}" + "};}\n"


        elif dimensionality == 2:

            print("2D Printing of Torus is not yet implemented")

        return(output_string)



class boundary(surface):
    """Child Class for Planar Boundary Surfaces"""

    def __str__(self):
        return f"Boundary Surface of Type {self.type} with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setBoundaryType(self, boundaryType):
        self.boundaryType = boundaryType

    def write_gmsh_representation(self, bounding_dimensions, dimensionality):

        [xmin, xmax, ymin, ymax, zmin, zmax] = bounding_dimensions
        xmin = xmin[0]
        xmax = xmax[0]
        ymin = ymin[0]
        ymax = ymax[0]

        if dimensionality == 3:
            if zmin == 0 and zmax == 0: #default values 
                zmin = 0
                zmax = 1
            else:
                zmin = zmin[0]
                zmax = zmax[0]
        else:
            zmin = 0
            zmax = 0
        #print(zmin)

        output_string = ""
        output_string = output_string + f"\n// {self}\n"

        if dimensionality == 3:

            line_1 = line("straight")
            line_2 = line("straight")
            line_3 = line("straight")
            line_4 = line("straight")

            if self.type == "x-plane-boundary":
            #print(self.coeffs["d"])
                if self.coeffs["d"][0] == xmin: #if left boundary
                    point_1 = point(xmin, ymin, zmin)
                    point_2 = point(xmin, ymax, zmin)
                    point_3 = point(xmin, ymax, zmax)
                    point_4 = point(xmin, ymin, zmax)
                elif self.coeffs["d"][0] == xmax: #if right boundary
                    point_1 = point(xmax, ymin, zmin)
                    point_2 = point(xmax, ymax, zmin)
                    point_3 = point(xmax, ymax, zmax)
                    point_4 = point(xmax, ymin, zmax)
                else:
                    raise ValueError("Invalid Boundary Coordinate Provided")

                line_1.setCoefficients(point_1.x, point_1.y, point_1.z, 0, 1, 0)
                line_2.setCoefficients(point_2.x, point_2.y, point_2.z, 0, 0, 1)
                line_3.setCoefficients(point_3.x, point_3.y, point_3.z, 0, -1, 0)
                line_4.setCoefficients(point_4.x, point_4.y, point_4.z, 0, 0, -1)

            elif self.type == "y-plane-boundary":
                if self.coeffs["d"][0] == ymin: #if back boundary
                    point_1 = point(xmin, ymin, zmin)
                    point_2 = point(xmin, ymin, zmax)
                    point_3 = point(xmax, ymin, zmax)
                    point_4 = point(xmax, ymin, zmin)
                elif self.coeffs["d"][0] == ymax: #if front boundary
                    point_1 = point(xmin, ymax, zmin)
                    point_2 = point(xmin, ymax, zmax)
                    point_3 = point(xmax, ymax, zmax)
                    point_4 = point(xmax, ymax, zmin)
                else:
                    raise ValueError("Invalid Boundary Coordinate Provided")

                line_1.setCoefficients(point_1.x, point_1.y, point_1.z, 0, 0, 1)
                line_2.setCoefficients(point_2.x, point_2.y, point_2.z, 1, 0, 0)
                line_3.setCoefficients(point_3.x, point_3.y, point_3.z, 0, 0, -1)
                line_4.setCoefficients(point_4.x, point_4.y, point_4.z, -1, 0, 0)

            elif self.type == "z-plane-boundary":
                if self.coeffs["d"][0] == zmin: #if bottom boundary
                    point_1 = point(xmin, ymin, zmin)
                    point_2 = point(xmax, ymin, zmin)
                    point_3 = point(xmax, ymax, zmin)
                    point_4 = point(xmin, ymax, zmin)
                elif self.coeffs["d"][0] == zmax: #if top boundary
                    point_1 = point(xmin, ymin, zmax)
                    point_2 = point(xmax, ymin, zmax)
                    point_3 = point(xmax, ymax, zmax)
                    point_4 = point(xmin, ymax, zmax)
                else:
                    raise ValueError("Invalid Boundary Coordinate Provided")

                line_1.setCoefficients(point_1.x, point_1.y, point_1.z, 1, 0, 0)
                line_2.setCoefficients(point_2.x, point_2.y, point_2.z, 0, 1, 0)
                line_3.setCoefficients(point_3.x, point_3.y, point_3.z, -1, 0, 0)
                line_4.setCoefficients(point_4.x, point_4.y, point_4.z, 0, -1, 0)

            else:
                raise ValueError("Unknown boundary type provided, cannot write to gmsh")


            line_1.addBoundingPoint(point_1)
            line_1.addBoundingPoint(point_2)

            line_2.addBoundingPoint(point_2)
            line_2.addBoundingPoint(point_3)

            line_3.addBoundingPoint(point_3)
            line_3.addBoundingPoint(point_4)

            line_4.addBoundingPoint(point_4)
            line_4.addBoundingPoint(point_1)

            output_string = output_string + line_1.write_gmsh_representation(dimensionality)
            output_string = output_string + line_2.write_gmsh_representation(dimensionality)
            output_string = output_string + line_3.write_gmsh_representation(dimensionality)
            output_string = output_string + line_4.write_gmsh_representation(dimensionality)

            output_string = output_string + f"Line Loop({self.gmsh_id}) = " + "{" + f"{line_1.gmsh_id}, {line_2.gmsh_id}, {line_3.gmsh_id}, {line_4.gmsh_id}" + "};\n"

            output_string = output_string + f"Plane Surface({self.gmsh_id}) = " + "{" + f"{self.gmsh_id}" + "};\n"
            #output_string = output_string + f'Physical Surface("{self.boundaryType}_surface") = ' + "{" + f"{self.gmsh_id}" + "};\n"

        elif dimensionality == 2:

            line_1 = line("straight")
            line_1.setgmshID(self.gmsh_id) #override the line's gmsh ID to prevent ID conflicts

            if self.type == "x-plane-boundary":
            #print(self.coeffs["d"])
                if self.coeffs["d"][0] == xmin: #if left boundary
                    point_1 = point(xmin, ymin, 0)
                    point_2 = point(xmin, ymax, 0)
                elif self.coeffs["d"][0] == xmax: #if right boundary
                    point_1 = point(xmax, ymin, 0)
                    point_2 = point(xmax, ymax, 0)
                else:
                    raise ValueError("Invalid Boundary Coordinate Provided")

                line_1.setCoefficients(point_1.x, point_1.y, point_1.z, 0, 1, 0)


            elif self.type == "y-plane-boundary":
                if self.coeffs["d"][0] == ymin: #if back boundary
                    point_1 = point(xmin, ymin, 0)
                    point_2 = point(xmax, ymin, 0)
                elif self.coeffs["d"][0] == ymax: #if front boundary
                    point_1 = point(xmin, ymax, 0)
                    point_2 = point(xmax, ymax, 0)
                else:
                    raise ValueError("Invalid Boundary Coordinate Provided")

                line_1.setCoefficients(point_1.x, point_1.y, point_1.z, 1, 0, 0)


            elif self.type == "z-plane-boundary": # if one of the top or bottom boundaries
                print("ZBoundary Encountered in 2D Model, Skipping Boundary")

            else:
                raise ValueError("Unknown boundary type provided, cannot write to gmsh")

            line_1.addBoundingPoint(point_1)
            line_1.addBoundingPoint(point_2)

            output_string = output_string + line_1.write_gmsh_representation(dimensionality)
            
        return(output_string)

class plane(surface):
    """Child Class for Planar Surfaces"""

    def __str__(self):
        return f"Plane Surface with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setCoefficients(self, a, b, c, d):
        self.coeffs["a"] = a
        self.coeffs["b"] = b
        self.coeffs["c"] = c
        self.coeffs["d"] = d

    def write_gmsh_representation(self, dimensionality):
        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        if dimensionality == 3:
            print("3D Printing of Non-Boundary Planes is not yet implemented")
            #output_string = output_string + f"Cylinder({self.gmsh_id}) = " + "{" + f"{self.coeffs['x0']}, {self.coeffs['y0']}, {self.coeffs['z0']}, {self.coeffs['alpha']}, {self.coeffs['beta']}, {self.coeffs['epsilon']}, {self.coeffs['r']}" + "};\n"
        elif dimensionality == 2:
            #circle_1 = circle("circle")
            #circle_1.setOpenMCID(self.OMC_id)
            #circle_1.setCoefficients(self.coeffs["x0"], self.coeffs["y0"], self.coeffs["z0"], 0, 0, 1, self.coeffs["r"])

            #output_string = output_string + circle_1.write_gmsh_representation(dimensionality)

            print("2D Printing of Non-Boundary Planes is not yet implemented")

        return(output_string) 


class line:
    """Base Class for 1-Dimensional Objects"""

    def __init__(self, line_type):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the global ID counter

        self.type = line_type
        self.boundingPoints = []
        self.coeffs = {}

    def __str__(self):
        return f"Line of Type {self.type} with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

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

    
    def write_gmsh_representation(self, dimensionality, isPhysical=False):
        output_string = ""

        for bound_point in self.boundingPoints:
            output_string = output_string + bound_point.write_gmsh_representation()

        output_string = output_string + f"Line({self.gmsh_id}) = " + "{" + f"{self.boundingPoints[0].gmsh_id}, {self.boundingPoints[1].gmsh_id}" + "};\n"

        if isPhysical:
            output_string = output_string + f"Physical Line({self.gmsh_id}) = " + "{" + f"{self.gmsh_id}" + "};\n"




        return(output_string)

class circle(line):
    """Child Class for Circular Lines"""

    def __str__(self):
        return f"Circle Line with OMC ID {self.OMC_id} and gmsh ID {self.gmsh_id}"

    def setCoefficients(self, x0, y0, z0, alpha, beta, epsilon, r):
        self.coeffs["x0"] = x0
        self.coeffs["y0"] = y0
        self.coeffs["z0"] = z0
        self.coeffs["alpha"] = alpha
        self.coeffs["beta"] = beta
        self.coeffs["epsilon"] = epsilon
        self.coeffs["r"] = r

        #Define the Bounding Points of the Cirlce (centerpoint and 4 orthogonal points on the circumference):
        
        centerpoint = point(x0, y0, z0)
        self.boundingPoints.append(centerpoint)

        normal_vector = np.array([alpha, beta, epsilon])

        #Find 2 vectors orthogonal to the normal vector:
        orthogonal_vector_1 = np.array([1, 1, ((-1*alpha) + (-1*beta))/epsilon])
        orthogonal_vector_2 = np.cross(normal_vector, orthogonal_vector_1)

        #Normalize the orthogonal vectors:
        orthogonal_vector_1 = orthogonal_vector_1/np.linalg.norm(orthogonal_vector_1)
        orthogonal_vector_2 = orthogonal_vector_2/np.linalg.norm(orthogonal_vector_2)

        #Use the orthogonal vectors to orthogonal points along the circumference of the circle:
        orthogonal_point_1 = point(x0 + r*orthogonal_vector_1[0], y0 + r*orthogonal_vector_1[1], z0 + r*orthogonal_vector_1[2])
        orthogonal_point_2 = point(x0 + r*orthogonal_vector_2[0], y0 + r*orthogonal_vector_2[1], z0 + r*orthogonal_vector_2[2])

        orthogonal_point_3 = point(x0 - r*orthogonal_vector_1[0], y0 - r*orthogonal_vector_1[1], z0 - r*orthogonal_vector_1[2])
        orthogonal_point_4 = point(x0 - r*orthogonal_vector_2[0], y0 - r*orthogonal_vector_2[1], z0 - r*orthogonal_vector_2[2])
        
        #Add the orthogonal points to the list of bounding points:
        self.boundingPoints.append(orthogonal_point_1)
        self.boundingPoints.append(orthogonal_point_2)
        self.boundingPoints.append(orthogonal_point_3)
        self.boundingPoints.append(orthogonal_point_4)

    def write_gmsh_representation(self, dimensionality):
        output_string = ""

        output_string = output_string + f"\n// {self}\n"

        for bound_point in self.boundingPoints:
            output_string = output_string + bound_point.write_gmsh_representation()

        line_1 = line("circle arc")
        line_2 = line("circle arc")
        line_3 = line("circle arc")
        line_4 = line("circle arc")

        output_string = output_string + f"Circle({line_1.gmsh_id}) = " + "{" + f"{self.boundingPoints[1].gmsh_id}, {self.boundingPoints[0].gmsh_id}, {self.boundingPoints[2].gmsh_id}" + "};\n"

        output_string = output_string + f"Circle({line_2.gmsh_id}) = " + "{" + f"{self.boundingPoints[2].gmsh_id}, {self.boundingPoints[0].gmsh_id}, {self.boundingPoints[3].gmsh_id}" + "};\n"

        output_string = output_string + f"Circle({line_3.gmsh_id}) = " + "{" + f"{self.boundingPoints[3].gmsh_id}, {self.boundingPoints[0].gmsh_id}, {self.boundingPoints[4].gmsh_id}" + "};\n"

        output_string = output_string + f"Circle({line_4.gmsh_id}) = " + "{" + f"{self.boundingPoints[4].gmsh_id}, {self.boundingPoints[0].gmsh_id}, {self.boundingPoints[1].gmsh_id}" + "};\n"

        output_string = output_string + f"Line Loop({self.gmsh_id}) = " + "{" + f"{line_1.gmsh_id}, {line_2.gmsh_id}, {line_3.gmsh_id}, {line_4.gmsh_id}" + "};\n"

        output_string = output_string + f"Plane Surface({self.gmsh_id}) = " + "{" + f"{self.gmsh_id}" + "};\n"



        return(output_string)



class point:
    """Base Class for 0-Dimensional Objects"""

    def __init__(self, x, y, z):

        global id_counter

        self.OMC_id = None
        self.gmsh_id = id_counter
        id_counter = id_counter + 1 #increment the ID counter

        self.x = x
        self.y = y
        self.z = z

        self.coeffs = {}
        self.hasBeenPrinted = False

    def __str__(self):
        return f"Point at location ({self.x}, {self.y}, {self.z}) with gmsh ID {self.gmsh_id}"

    def setOpenMCID(self, id):
        self.OMC_id = id

    def setgmshID(self, id):
        self.gmsh_id = id

    def write_gmsh_representation(self, isPhysical=False):
        output_string = ""

        if not self.hasBeenPrinted:
            output_string = output_string + f"Point({self.gmsh_id}) = " + "{" + f"{self.x}, {self.y}, {self.z}" + "};\n"
            self.hasBeenPrinted = True

        return(output_string)