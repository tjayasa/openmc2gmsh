import xml.etree.ElementTree as ET
import gmsh
from Converter import *


if not gmsh.is_initialized():
    gmsh.initialize()
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    gmsh.option.setNumber("Mesh.MeshSizeMin", 0.4)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 0.4)
    
def read_xml(openmc_file):
    """Convert OpenMC geometry to Gmsh format."""

    print(f"Beginning {3}D Conversion of {openmc_file}:")
    
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
    for surface in xml_surfaces:
        surface_id = int(surface.get('id'))
        surface_type = str(surface.get('type'))
        boundary_type = str(surface.get('boundary'))
        coeffs = [float(c) for c in surface.get('coeffs').split()]
        
        print({"surface_id" : surface_id, 
               "surface_type" : surface_type, 
               "boundry_type" : boundary_type, 
               "coeffs": coeffs})
        
        # surface is a plane:
        if surface_type == "x-plane":
            coeffs = [1, 0, 0, coeffs[0]]
            Plane(surface_id,coeffs)
            
        if surface_type == "y-plane":
            coeffs = [0, 1, 0, coeffs[0]]
            Plane(surface_id,coeffs)
            
        if surface_type == "z-plane":
            coeffs = [0, 0, 1, coeffs[0]]
            Plane(surface_id,coeffs)
            
        if surface_type == "z-cylinder":
            ZCylinder(surface_id,coeffs)
       
    # temp = Entity([])
    # temp.create_intersection([100003,4],200000)
    
    # factory = gmsh.model.occ
    # # factory.add_box(-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,-Prims.BOUNDING_VALUE/2,
    # #                            Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,Prims.BOUNDING_VALUE,0)     
    # factory.synchronize()
    # gmsh.fltk.run()   

    xml_cells = geometry.findall('cell')
    if not xml_cells:
        print("No <cell> elements found within <geometry>.")
        return
    
    
# read_xml("./OpenMC_Examples/./OpenMC_Examples/pincellGeometry.xml")
    