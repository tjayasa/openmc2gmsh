from Converter import *
import gmsh

# read_xml("OpenMC_Examples/AssortedGeometry.xml")
# read_xml("OpenMC_Examples/pincellGeometry.xml")
cell_mat_map, cell_id_map = read_geo_xml("OpenMC_Examples/complex_cell_geo.xml")
read_mat_xml("OpenMC_Examples/complex_cell_mat.xml",cell_mat_map, cell_id_map)

v = gmsh.view.add("comments")
gmsh.view.addListDataString(v, [10, -10], ["OMC's Complex_Cell"])

gmsh.fltk.run()
gmsh.finalize()
