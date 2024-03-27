import xml.etree.ElementTree as ET
import gmsh
from Converter import *
import re


if not gmsh.is_initialized():
    gmsh.initialize()
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    gmsh.option.setNumber("Mesh.MeshSizeMin", 0.4)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 0.4)

def get_id_map(xml_surfaces, compress = True) -> dict:
    """Returns the mapping from openMC ids to Gmsh tags (before encoding)"""
    id_map = {}
    for surface in xml_surfaces:
        curr_id = int(len(id_map)/2 + 1) if compress else int(surface.get('id'))
        id_map[int(surface.get('id'))] = curr_id
        id_map[-int(surface.get('id'))] = -curr_id
    return id_map
    

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
    
    print("surfaces:")
    id_map = get_id_map(xml_surfaces, False)
    # print(id_map)
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
            Plane(id_map[surface_id],coeffs)
            
        if surface_type == "y-plane":
            coeffs = [0, 1, 0, coeffs[0]]
            Plane(id_map[surface_id],coeffs)
            
        if surface_type == "z-plane":
            coeffs = [0, 0, 1, coeffs[0]]
            Plane(id_map[surface_id],coeffs)
            
        if surface_type == "x-cylinder":
            ZCylinder(id_map[surface_id],coeffs)
            
        if surface_type == "y-cylinder":
            YCylinder(id_map[surface_id],coeffs)
        
        if surface_type == "z-cylinder":
            ZCylinder(id_map[surface_id],coeffs)
        
        if surface_type == "sphere":
            Sphere(id_map[surface_id],coeffs)
            
        if surface_type == "x-torus":
            XTorus(id_map[surface_id], coeffs)
        
        if surface_type == "y-torus":
            XTorus(id_map[surface_id], coeffs)
            
        if surface_type == "z-torus":
            XTorus(id_map[surface_id], coeffs)
            

    xml_cells = geometry.findall("cell")
    if not xml_cells:
        print("No <cell> elements found within <geometry>.")
        return

    for cell in xml_cells:
        #<cell id="6" material="4" name="moderator" region="6 -7 8 -9 5" universe="3" />
        cell_id = int(cell.get("id"))
        cell_name = cell.get("name")
        cell_universe = cell.get("universe") if cell.get("universe") is None else int(cell.get("universe"))
        cell_mat = cell.get("material")
        cell_mat = 0 if cell_mat == "void" else int(cell_mat)
        cell_region = []

        # print(re.findall('(\(|\)|~|\||-?\d+)',cell.get("region")))
        cell_region = [id_map[int(i)] if i.replace('-','0').isdigit() else i for i in re.findall('(\(|\)|~|\||-?\d+)',cell.get("region"))]
        # print(cell_region)
                
        
        print({"cell_id" : cell_id, 
               "cell_region": cell_region,
               "cell_mat" : cell_mat,
               "cell_name" : cell_name, 
               "cell_universe" : cell_universe
               })

        entity = Entity(id=cell_id,
               region=cell_region,
               material=cell_mat,
               name=cell_name,
               universe=cell_universe)
        entity.create_intersection()
        # print(gmsh.model.occ.get_entities(3))
        
    gmsh.model.occ.synchronize()    
    # gmsh.fltk.run()
    # gmsh.finalize()
    
    
# read_xml("OpenMC_Examples/pincellGeometry.xml")
    