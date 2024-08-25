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
    

def read_geo_xml(openmc_file):
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

    mat_cell_map = {}
    univ_cell_map = {} # keeps track of geometry per universes 
    for cell in xml_cells:
        cell_id = int(cell.get("id"))
        cell_name = cell.get("name")
        cell_universe = cell.get("universe") if cell.get("universe") is None else int(cell.get("universe"))
        cell_mat = cell.get("material")
        cell_mat = 0 if cell_mat == "void" else int(cell_mat)
        cell_fill = cell.get("fill")
        
        cell_region = []

        cell_region = [id_map[int(i)] if i.replace('-','0').isdigit() else i for i in re.findall('(\(|\)|~|\||-?\d+)',cell.get("region"))]                
        
        print({"cell_id" : cell_id, 
               "cell_region": cell_region,
               "cell_mat" : cell_mat,
               "cell_name" : cell_name, 
               "cell_universe" : cell_universe,
               "cell_fill" : cell_fill
               })

        entity = Entity(id=cell_id,
               region=cell_region,
               material=cell_mat,
               name=cell_name,
               universe=cell_universe,
               fill=cell_fill)

        if cell_mat not in mat_cell_map:
            mat_cell_map[cell_mat] = []

        if cell_universe not in univ_cell_map:
            univ_cell_map[cell_universe] = []

        
        mat_cell_map[cell_mat] += entity.create_intersection()
        univ_cell_map[cell_universe] +=  mat_cell_map[cell_mat]
        
        # print(gmsh.model.occ.get_entities(3))

    gmsh.model.occ.synchronize()    
    return mat_cell_map, univ_cell_map

def read_mat_xml(omc_mat_file, mat_cell_map, id_univ_map):
    try:
        tree = ET.parse(omc_mat_file)
        root = tree.getroot()

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return
    root = tree.getroot()

    materials = root
    if materials is None:
        print("No <mats> element found in the XML file.")
        return

    xml_mats = materials.findall('material')
    
    if not xml_mats:
        print("No <material> elements found within <materials>.")
        return

    print(mat_cell_map)
    for mat in xml_mats:
        print(mat.get("id"))
        print(mat.get("name"))
        
        if int(mat.get("id")) not in Entity.mat_cell_map:
            continue

        gmsh.model.add_physical_group(3,
                                      [tag[1] for cell_obj in Entity.mat_cell_map[int(mat.get("id"))] for tag in cell_obj.tags],
                                      name=str(mat.get("id")) if mat.get("name") is None else mat.get("name"))

    