import xml.etree.ElementTree as ET
import numpy as np
from converter_functions import *
from converter_classes import *

def parse_openmc_surface(xml_surface):
    """Parse OpenMC surface and return salient information in the form of a dict (Gmsh points and lines)."""
    surface_id = str(xml_surface.get('id'))
    surface_type = str(xml_surface.get('type'))
    boundary_type = str(xml_surface.get('boundary'))
    coeffs = [float(c) for c in xml_surface.get('coeffs').split()]
    #print (f"type: {surface_type}")

    match surface_type:
        #Planes:
        case "x-plane":
            x0 = coeffs
            new_surface = surface("plane")
            new_surface.setCoefficients(1, 0, 0, x0)
            return new_surface
        case "y-plane":
            y0 = coeffs
            new_surface = surface("plane")
            new_surface.setCoefficients(0, 1, 0, y0)
            return new_surface
        case "z-plane":
            z0 = coeffs
            new_surface = surface("plane")
            new_surface.setCoefficients(0, 0, 1, z0)
            return new_surface
        case "plane":
            a, b, c, d = coeffs
            new_surface = surface("plane")
            new_surface.setCoefficients(a, b, c, d)
            return new_surface
            # Assuming only planar surfaces for simplicity (will definitely have to be more complex)
            #if a == 0 and b == 0:
                # Vertical line
                #return [(d/c, -10), (d/c, 10)]
            #elif a == 0 and c == 0:
                # Horizontal line
                #return [(-10, d/b), (10, d/b)]
            #else:
                #raise ValueError("Unsupported surface type")
        #Spheres:
        case "sphere":
            x0, y0, z0, r = coeffs
            new_surface = surface("sphere")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r":r}
            return new_surface
        #Cones:
        case "x-cone":
            x0, y0, z0, r2 = coeffs
            new_surface = surface("x-cone")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
            return new_surface
        case "y-cone":
            x0, y0, z0, r2 = coeffs
            new_surface = surface("y-cone")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
            return new_surface
        case "z-cone":
            x0, y0, z0, r2 = coeffs
            new_surface = surface("z-cone")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
            return new_surface
        #Cylinders:
        case "x-cylinder":
            y0, z0, r = coeffs
            new_surface = surface("x-cylinder")
            #return {"type":surface_type, "id":surface_id, "y0":y0, "z0":z0, "r":r}
            return new_surface
        case "y-cylinder":
            x0, z0, r = coeffs
            new_surface = surface("y-cylinder")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "z0":z0, "r":r}
            return new_surface
        case "z-cylinder":
            x0, y0, r = coeffs
            new_surface = surface("z-cylinder")
            #return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "r":r}
            return new_surface
        #Default (Error) Case:
        case _:
            raise ValueError("Unsupported surface type (new)")

def convert_to_gmsh(openmc_file, gmsh_file, dimensionality):
    """Convert OpenMC geometry to Gmsh format."""

    #Setting up variables:
    is_3d = (dimensionality == 3)

    try:
        tree = ET.parse(openmc_file)
        root = tree.getroot()
        # print(tree)

        # for child in root:
        #     print (child.tag, child.attrib)

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return
    root = tree.getroot()

    geometry = root
    if geometry is None:
        print("No <geometry> element found in the XML file.")
        return

    surfaces = geometry.findall('surface')
    if not surfaces:
        print("No <surface> elements found within <geometry>.")
        return

    points = {}
    lines = []
    id_counter = 0


    # Process each surface in the OpenMC file
    with open(gmsh_file, 'w') as f:

        for current_surface in surfaces:
            try:
                surface_obj = parse_openmc_surface(current_surface)
                #line = []
                match surface_obj.type:
                    case "x-plane":
                        print ("XPlane Encountered!")
                        #if dimensionality == 2:
                            #f.write(f"Sphere({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, {surface_dict['z0']}, {surface_dict['r']};\n")
                    case "y-plane":
                        print ("YPlane Encountered!")
                    case "z-plane":
                        print ("ZPlane Encountered!")
                    case "plane":
                        print ("Plane Encountered!")

                    case "sphere":
                        print ("Sphere Encountered!")
                        #f.write(f"Sphere({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, {surface_dict['z0']}, {surface_dict['r']};\n")
                    case "x-cylinder":
                        print ("XCylinder Encountered!")
                        #f.write(f"Cylinder({surface_dict['id']}) = 0, {surface_dict['y0']}, {surface_dict['z0']}, 1, 0, 0, {surface_dict['r']};\n")
                    case "y-cylinder":
                        print ("YCylinder Encountered!")
                        #f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, 0, {surface_dict['z0']}, 0, 1, 0, {surface_dict['r']};\n")
                    case "z-cylinder":
                        print ("ZCylinder Encountered!")
                        #if dimensionality == 2:
                            #f.write(f"Circle({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, 0,  {surface_dict['r']};\n")
                        #if dimensionality == 3:
                            #f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, 0, 0, 0, 1, {surface_dict['r']};\n")
                    #case "x-cone":
                    #    print ("XCone Encountered!")
                    #    f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, {surface_dict['z0']}, 1, 0, 0, {surface_dict['r']};\n")
                    case _:
                        print("Unimplemented Surface Encountered!")
                #for point in line_points:
                #    if point not in points:
                #        points[point] = len(points) + 1
                #    line.append(points[point])
                #lines.append(tuple(line))
            except ValueError as e:
                print(f"Skipping surface due to error: {e}")

        # Write to Gmsh file
    #with open(gmsh_file, 'w') as f:
    #    for point, idx in points.items():
    #        f.write(f"Point({idx}) = {{{point[0]}, {point[1]}, 0, 1.0}};\n")
    #    for i, line in enumerate(lines, 1):
    #        f.write(f"Line({i}) = {{{line[0]}, {line[1]}}};\n")

#plane_dict1 = {"a":1 , "b":2 , "c":1 , "d":3}

example_plane = surface("plane")
example_plane.setCoefficients(1, 1, 1, 3)

#plane2 = surface("plane")
#plane2.setCoefficients(1, 0, 0, 9)

line1 = line("straight")
line1.setCoefficients(0, 1, 0, 1, 2, 3)

# Set up  bounding box:
xmin = -10
xmax = 10
ymin = -10
ymax = 5
zmin = 0
zmax = 10

top_boundary = surface("plane")
top_boundary.setCoefficients(0, 0, 1, zmax)

bottom_boundary = surface("plane")
bottom_boundary.setCoefficients(0, 0, 1, zmin)

front_boundary = surface("plane")
front_boundary.setCoefficients(0, 1, 0, ymax)

back_boundary = surface("plane")
back_boundary.setCoefficients(0, 1, 0, ymin)

right_boundary = surface("plane")
right_boundary.setCoefficients(1, 0, 0, xmax)

left_boundary = surface("plane")
left_boundary.setCoefficients(1, 0, 0, xmin)

find_plane_bounding_points(example_plane, top_boundary, bottom_boundary, front_boundary, back_boundary, right_boundary, left_boundary)

# Running the function
convert_to_gmsh('./pincellGeometry.xml', './convertedPincellGeometry.geo', 2)
#convert_to_gmsh('./simpleGeometry.xml', './convertedGeometry.geo', 3)
