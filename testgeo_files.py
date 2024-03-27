from Converter import *
import gmsh

# read_xml("OpenMC_Examples/AssortedGeometry.xml")
# read_xml("OpenMC_Examples/pincellGeometry.xml")
read_xml("OpenMC_Examples/complex_cell.xml")
gmsh.fltk.run()
gmsh.finalize()
