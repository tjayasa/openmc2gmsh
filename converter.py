import xml.etree.ElementTree as ET
import numpy as np
from converter_functions import *
from converter_classes import *

def parse_openmc_surface(surface):
    """Parse OpenMC surface and return salient information in the form of a dict (Gmsh points and lines)."""
    surface_id = str(surface.get('id'))
    surface_type = str(surface.get('type'))
    boundary_type = str(surface.get('boundary'))
    coeffs = [float(c) for c in surface.get('coeffs').split()]
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
            return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r":r}
        #Cones:
        case "x-cone":
            x0, y0, z0, r2 = coeffs
            return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
        case "y-cone":
            x0, y0, z0, r2 = coeffs
            return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
        case "z-cone":
            x0, y0, z0, r2 = coeffs
            return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "z0":z0, "r2":r2}
        #Cylinders:
        case "x-cylinder":
            y0, z0, r = coeffs
            return {"type":surface_type, "id":surface_id, "y0":y0, "z0":z0, "r":r}
        case "y-cylinder":
            x0, z0, r = coeffs
            return {"type":surface_type, "id":surface_id, "x0":x0, "z0":z0, "r":r}
        case "z-cylinder":
            x0, y0, r = coeffs
            return {"type":surface_type, "id":surface_id, "x0":x0, "y0":y0, "r":r}
        
        #Tori
        case "x-torus":
            x0, y0, z0, B, C = coeffs
            A = np.sqrt(C + B**2)
            return {"type": "x-torus", "center": [x0, y0, z0], "major_radius": A, "minor_radius": B}
        case "y-torus":
            x0, y0, z0, B, C = coeffs
            A = np.sqrt(C + B**2)
            return {"type": "y-torus", "center": [x0, y0, z0], "major_radius": A, "minor_radius": B}
        case "z-torus":
            x0, y0, z0, B, C = coeffs
            A = np.sqrt(C + B**2)
            return {"type": "z-torus", "center": [x0, y0, z0], "major_radius": A, "minor_radius": B}
        
        #Quadrics
        case "quadric":
            # Extract the coefficients for the general quadric equation
            # coefficients D, E, and F are unused so replaced with _
            A, B, C, _, _, _, G, H, J, K = coeffs
            # Convert the general quadric coefficients to ellipsoid parameters
            # Assuming the ellipsoid is centered at (x0, y0, z0) and has semi-axes lengths a, b, c
            x0 = -G / (2 * A)
            y0 = -H / (2 * B)
            z0 = -J / (2 * C)
            a = np.sqrt(-K / A + x0**2)
            b = np.sqrt(-K / B + y0**2)
            c = np.sqrt(-K / C + z0**2)
            return {"type": "ellipsoid", "center": [x0, y0, z0], "semi_axes": [a, b, c]}
        
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

        for surface in surfaces:
            try:
                surface_obj = parse_openmc_surface(surface)
                #line = []
                match surface_dict["type"]:
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
                        f.write(f"Sphere({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, {surface_dict['z0']}, {surface_dict['r']};\n")
                    case "x-cylinder":
                        print ("XCylinder Encountered!")
                        f.write(f"Cylinder({surface_dict['id']}) = 0, {surface_dict['y0']}, {surface_dict['z0']}, 1, 0, 0, {surface_dict['r']};\n")
                    case "y-cylinder":
                        print ("YCylinder Encountered!")
                        f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, 0, {surface_dict['z0']}, 0, 1, 0, {surface_dict['r']};\n")
                    case "z-cylinder":
                        print ("ZCylinder Encountered!")
                        if dimensionality == 2:
                            f.write(f"Circle({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, 0,  {surface_dict['r']};\n")
                        if dimensionality == 3:
                            f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, 0, 0, 0, 1, {surface_dict['r']};\n")
                    #case "x-cone":
                    #    print ("XCone Encountered!")
                    #    f.write(f"Cylinder({surface_dict['id']}) = {surface_dict['x0']}, {surface_dict['y0']}, {surface_dict['z0']}, 1, 0, 0, {surface_dict['r']};\n")
                    
                    case "x-torus":
                        torus_data = surface_obj
                        # Gmsh doesn't directly support x-torus; it supports z-torus. 
                        # So, rotate the torus about the Y-axis by 90 degrees to align the Z-torus along the X-axis.
                        f.write(f"Translate {{0, 0, {torus_data['center'][0]}}} {{\n")
                        f.write(f"  Rotate {{0, 90, 0}} {{\n")
                        f.write(f"    Torus({{0, 0, 0}}, {torus_data['major_radius']}, {torus_data['minor_radius']});\n")
                        f.write(f"  }}\n")
                        f.write(f"}}\n")
                    case "y-torus":
                        torus_data = surface_obj
                        # Rotate the torus about the X-axis by 90 degrees to align the Z-torus along the Y-axis.
                        f.write(f"Translate {{0, 0, {torus_data['center'][1]}}} {{\n")
                        f.write(f"  Rotate {{90, 0, 0}} {{\n")
                        f.write(f"    Torus({{0, 0, 0}}, {torus_data['major_radius']}, {torus_data['minor_radius']});\n")
                        f.write(f"  }}\n")
                        f.write(f"}}\n")
                    case "z-torus":
                        torus_data = surface_obj
                        # Z-torus is directly supported in Gmsh.
                        f.write(f"Torus({torus_data['center'][0]}, {torus_data['center'][1]}, {torus_data['center'][2]}, {torus_data['major_radius']}, {torus_data['minor_radius']});\n")

                    case "quadric":
                        ellipsoid_data = surface_obj
                        if ellipsoid_data["type"] == "ellipsoid":
                            center = ellipsoid_data["center"]
                            semi_axes = ellipsoid_data["semi_axes"]
                            f.write(f"Ellipsoid({center[0]}, {center[1]}, {center[2]}, {semi_axes[0]}, {semi_axes[1]}, {semi_axes[2]});\n")

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

plane1 = surface("plane")
plane1.setCoefficients(1, 2, 3, 3)

plane2 = surface("plane")
plane2.setCoefficients(1, 0, 0, 9)

#plane_dict2 = {"a":1 , "b":0 , "c":0 , "d":9}

line1 = line("straight")
line1.setCoefficients(0, 1, 0, 1, 2, 3)

#line_dict1 = {"x0": 0, "y0": 1, "z0": 0, "alpha": 1, "beta": 2, "epsilon": 3}

#xline = {"x0": 1, "y0": 0, "z0": 0, "alpha": 0, "beta": 1, "epsilon": 2}
#yline = {"x0": 0, "y0": 1, "z0": 0, "alpha": 1, "beta": 0, "epsilon": 1}

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

#bottom_boundary = {"a":0 , "b":0 , "c":1 , "d":zmin}

#top_boundary = {"a":0 , "b":0 , "c":1 , "d":zmax}
#bottom_boundary = {"a":0 , "b":0 , "c":1 , "d":zmin}

#front_boundary = {"a":0 , "b":1 , "c":0 , "d":ymax}
#back_boundary = {"a":0 , "b":1 , "c":0 , "d":ymin}

#right_boundary = {"a":1 , "b":0 , "c":0 , "d":xmax}
#left_boundary = {"a":1 , "b":0 , "c":0 , "d":xmin}

#intersection_line = find_intersection_line(plane_dict1, plane_dict2)
#find_plane_line_intersection_point(plane_dict1, line_dict1)

#print (f"Do the lines intersect? {do_lines_intersect(xline, yline)}")
#if do_lines_intersect(xline, yline):
#    find_line_line_intersection_point(xline, yline)

#Find the six intersection lines with the boundaries:
#top_intersect = find_intersection_line(plane1, top_boundary)
#bottom_intersect = find_intersection_line(plane1, bottom_boundary)

#front_intersect = find_intersection_line(plane1, front_boundary)
#back_intersect = find_intersection_line(plane1, back_boundary)

#left_intersect = find_intersection_line(plane1, left_boundary)
#right_intersect = find_intersection_line(plane1, right_boundary)

list_of_boundaries = [top_boundary, bottom_boundary, front_boundary, back_boundary, left_boundary, right_boundary]

#list_of_possible_intersects = [top_intersect, bottom_intersect, front_intersect, back_intersect, left_intersect, right_intersect]

list_of_intersects = []
bounding_points = []

for i in range(0,6):
    intersect =  find_intersection_line(plane1, list_of_boundaries[i])
    if intersect is not None:
        list_of_intersects.append(intersect)

i = 0
print(len(list_of_intersects))

for index1 in range(0,len(list_of_intersects)):
    for index2 in range(index1+1,len(list_of_intersects)):
        #print(i)
        #print (f"Do the lines {index1} and {index2} intersect? {do_lines_intersect(list_of_intersects[index1], list_of_intersects[index2])}")
        if do_lines_intersect(list_of_intersects[index1], list_of_intersects[index2]):

            point = find_line_line_intersection_point(list_of_intersects[index1], list_of_intersects[index2])
            print (f"Lines {index1} and {index2} intersect.")

            if is_point_within_bounds(point, xmin, xmax, ymin, ymax, zmin, zmax):

                print (f"Lines {index1} and {index2} intersect in bounds.")
                print(f"Intersection Point ({point.x}, {point.y}, {point.z}) is within bounds")
                bounding_points.append(point)

                plane1.addBoundingLine(list_of_intersects[index1])

                list_of_intersects[index1].addBoundingPoint(point)
                list_of_intersects[index2].addBoundingPoint(point)
        #i = i+1



for point in bounding_points:
    print(f"Point(0) = {'{'} {round(float(point.x), 5)}, {round(float(point.y), 5)}, {round(float(point.z), 5)}{'}'};")
    
    #id_counter = id_counter+1

print(len(plane1.boundingLines))

# Running the function
#convert_to_gmsh('./pincellGeometry.xml', './convertedPincellGeometry.geo', 2)
#convert_to_gmsh('./simpleGeometry.xml', './convertedGeometry.geo', 3)
