import xml.etree.ElementTree as ET
import numpy as np
from converter_functions import *
from converter_classes import *

def convert_to_gmsh(openmc_file, gmsh_file, dimensionality, extrudedLength=None):
    """Convert OpenMC geometry to Gmsh format."""

    print(f"Beginning {dimensionality}D Conversion of {openmc_file}:")

    global id_counter

    try:
        tree = ET.parse(openmc_file)
        root = tree.getroot()

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return
    root = tree.getroot()

    geometry = root
    if geometry is None:
        print("No <geometry> element found in the XML file.")
        return

    xml_surfaces = geometry.findall('surface')
    if not xml_surfaces:
        print("No <surface> elements found within <geometry>.")
        return

    xml_cells = geometry.findall('cell')
    if not xml_cells:
        print("No <cell> elements found within <geometry>.")
        return

    points = {}
    lines = []
    list_of_surface_objects = []
    list_of_cell_objects = []
    list_of_boundaries = []
    boundary_IDS = []

    for current_surface in xml_surfaces:
        try:
            surface_obj = parse_openmc_surface(current_surface, dimensionality, extrudedLength=extrudedLength)
            list_of_surface_objects.append(surface_obj)
            if "boundary" in surface_obj.type:
                list_of_boundaries.append(surface_obj)
        except ValueError as e:
                print(f"Skipping surface due to error: {e}")

    for current_cell in xml_cells:
        try:
            cell_obj = parse_openmc_cell(current_cell, dimensionality)
            cell_obj.findAllBoundingSurfaces(list_of_surface_objects)
            list_of_cell_objects.append(cell_obj)
        except ValueError as e:
                print(f"Skipping surface due to error: {e}")

    #Determine the bounding lines/planes:
    xmin, xmax, ymin, ymax, zmin, zmax = determine_bounding_box(list_of_boundaries, extrudedLength)
    bounding_dimensions = [xmin, xmax, ymin, ymax, zmin, zmax]
    #print(f"zmax: {zmax}")
    
    #Fixing my list buffonery:
    #xmin = xmin[0]
    #xmax = xmax[0]
    #ymin = ymin[0]
    #ymax = ymax[0]
    #zmin = zmin[0]
    #zmax = zmax[0]



    # Process each surface in the OpenMC file
    with open(gmsh_file, 'w') as f:

        #Write the OpenCASCADE Header:
        f.write('SetFactory("OpenCASCADE");\n\n')

        #Write the bounding lines/planes:
        for boundary_obj in list_of_boundaries:
            #print(boundary_obj)
            f.write(boundary_obj.write_gmsh_representation(bounding_dimensions, dimensionality))

            if (dimensionality == 3) or (boundary_obj.type != "z-boundary-plane"): #add all boundary planes for 3D conversion, but only add x and y boundary planes for 2D conversion
                boundary_IDS.append(boundary_obj.gmsh_id)

        
        #Write the boundary physical groups:
        f.write(constructBoundaryPhysicalGroups(list_of_boundaries, dimensionality))

        #Write the surface entries:
        for surface_obj in list_of_surface_objects:
            try:
                #surface_obj = parse_openmc_surface(current_surface, dimensionality)
                #line = []
                match surface_obj.type:
                    case "x-plane":
                        print ("XPlane Encountered!")
                    case "y-plane":
                        print ("YPlane Encountered!")
                    case "z-plane":
                        print ("ZPlane Encountered!")
                    case "x-plane-boundary":
                        print ("XPlane Boundary Encountered!")
                    case "y-plane-boundary":
                        print ("YPlane BoundaryEncountered!")
                    case "z-plane-boundary":
                        print ("ZPlane Boundary Encountered!")
                    case "plane":
                        print ("Plane Encountered!")
                    case "sphere":
                        print ("Sphere Encountered!")
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "x-cylinder":
                        print ("XCylinder Encountered!")
                        surface_obj.setBaseAndHeight(bounding_dimensions)
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "y-cylinder":
                        print ("YCylinder Encountered!")
                        surface_obj.setBaseAndHeight(bounding_dimensions)
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "z-cylinder":
                        print ("ZCylinder Encountered!")
                        surface_obj.setBaseAndHeight(bounding_dimensions)
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "x-torus":
                        print ("XTorus Encountered!")
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "y-torus":
                        print ("YTorus Encountered!")
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case "z-torus":
                        print ("ZTorus Encountered!")
                        f.write(surface_obj.write_gmsh_representation(dimensionality))
                    case _:
                        print("Unimplemented Surface Encountered!")
                        print(f"Type: {surface_obj.type}")

            except ValueError as e:
                print(f"Skipping surface due to error: {e}")


        #Write the Void Volume/Surface:
        boundary_id_string = ""
        for bound_id in boundary_IDS:
            boundary_id_string = boundary_id_string + str(bound_id) + ", "
        boundary_id_string = boundary_id_string[:-2] # remove the final comma and space

        if dimensionality == 3: #void volume
            f.write("\n// Void Volume with gmsh ID 0 (Necessary for Cell Construction)\n")
            f.write("Box(0) = {" + f"{xmin[0]}, {ymin[0]}, {zmin[0]}, {xmax[0]-xmin[0]}, {ymax[0]-ymin[0]}, {zmax[0]-zmin[0]}" + "};\n")
        elif dimensionality == 2: # void surface
            f.write("\n// Void Surface with gmsh ID 0 (Necessary for Cell Construction)\n")
            f.write("Rectangle(0) = {" + f"{xmin[0]}, {ymin[0]}, 0, {xmax[0]-xmin[0]}, {ymax[0]-ymin[0]}" + "};\n")

        #Write the cell entries:
        for cell_obj in list_of_cell_objects:
            try:
                match cell_obj.type:
                    case "cell":
                        print ("Cell Encountered!")
                        f.write(cell_obj.write_gmsh_representation(dimensionality))
                    case _:
                        print("Unimplemented Volume Encountered!")

            except ValueError as e:
                print(f"Skipping cell due to error: {e}")

        #Write the boundary physical groups:
        f.write(constructMaterialPhysicalGroups(list_of_cell_objects, dimensionality))

    print(f"Finished {dimensionality}D conversion of {openmc_file}, converted file printed to {gmsh_file}")


# Running the function:

#Pincell Example (2D and 3D):
convert_to_gmsh('./OpenMC_Examples/pincellGeometry.xml', './convertedPincellGeometry_2D.geo', 2)
convert_to_gmsh('./OpenMC_Examples/pincellGeometry.xml', './convertedPincellGeometry_3D.geo', 3, extrudedLength = 3)

# Assorted Solids Example (3D):
convert_to_gmsh('./OpenMC_Examples/AssortedGeometry.xml', './convertedAssortedGeometry_3D.geo', 3)
