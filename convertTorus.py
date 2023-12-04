import xml.etree.ElementTree as ET

def convert_torus_to_gmsh(xml_file, geo_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the Gmsh file for writing
    with open(geo_file, 'w') as f:
        f.write("SetFactory(\"OpenCASCADE\");\n")

        # Iterate over each surface in the XML file
        for surface in root.findall('surface'):
            surface_type = surface.get('type')
            coeffs = surface.get('coeffs').split()

            # Check if the surface is a torus
            if surface_type in ['x-torus', 'y-torus', 'z-torus']:
                # Extract coefficients for the torus
                R, r, center_x, center_y, center_z = [float(c) for c in coeffs[:5]]
                
                # Write the Gmsh command for the torus
                f.write(f"R = {R}; // Major radius\n")
                f.write(f"r = {r}; // Minor radius\n")
                f.write(f"Torus(1) = {{{center_x}, {center_y}, {center_z}, R, r}};\n")

                # Apply rotation if necessary
                if surface_type == 'x-torus':
                    # Rotate 90 degrees about the Y-axis to align with the X-axis
                    f.write("Rotate {{0, 1, 0}, {0, 0, 0}, Pi/2} { Duplicata { Volume{1}; } };\n")
                elif surface_type == 'y-torus':
                    # Rotate -90 degrees about the X-axis to align with the Y-axis
                    f.write("Rotate {{1, 0, 0}, {0, 0, 0}, -Pi/2} { Duplicata { Volume{1}; } };\n")

                # Add mesh settings
                f.write("Mesh.CharacteristicLengthMin = 0.1;\n")
                f.write("Mesh.CharacteristicLengthMax = 0.1;\n")
                f.write("Mesh 3;\n")
            else:
                print(f"Skipping unsupported surface type: {surface_type}")

# Example usage
convert_torus_to_gmsh('simpleTorus.xml', 'x-output.geo')
