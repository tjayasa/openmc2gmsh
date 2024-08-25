import sys
import gmsh
from Converter import read_geo_xml, read_mat_xml

def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid arguments. Must pass in the geometry and material xml files to convert to gmsh")
        exit(1)
    omc_geo_path = sys.argv[1]
    omc_mat_path = sys.argv[2]
    cell_mat_map, cell_id_map = read_geo_xml(omc_geo_path)
    read_mat_xml(omc_mat_path,cell_mat_map, cell_id_map)

    v = gmsh.view.add("comments")
    gmsh.view.addListDataString(v, [10, -10], ["viewing " + omc_geo_path])

    gmsh.fltk.run()
    gmsh.finalize()

if __name__ == '__main__':
    main()