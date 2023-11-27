import xml.etree.ElementTree as ET

def parse_openmc_surface(surface):
    """Parse OpenMC surface and return salient information in the form of a dict (Gmsh points and lines)."""
    surface_id = [str(surface.get('id'))]
    surface_type = [str(surface.get('type'))]
    coeffs = [float(c) for c in surface.get('coeffs').split()]

    if surface_type == "plane":
        a, b, c, d = coeffs
        # Assuming only planar surfaces for simplicity (will definitely have to be more complex)
        if a == 0 and b == 0:
            # Vertical line
            return [(d/c, -10), (d/c, 10)]
        elif a == 0 and c == 0:
            # Horizontal line
            return [(-10, d/b), (10, d/b)]
        else:
            raise ValueError("Unsupported surface type")
    elif surface_type == "sphere":
        x0, y0, z0, r = coeffs



def convert_to_gmsh(openmc_file, gmsh_file):
    """Convert OpenMC geometry to Gmsh format."""
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

    # Process each surface in the OpenMC file
    for surface in surfaces:
        try:
            line_points = parse_openmc_surface(surface)
            line = []
            for point in line_points:
                if point not in points:
                    points[point] = len(points) + 1
                line.append(points[point])
            lines.append(tuple(line))
        except ValueError as e:
            print(f"Skipping surface due to error: {e}")

    # Write to Gmsh file
    with open(gmsh_file, 'w') as f:
        for point, idx in points.items():
            f.write(f"Point({idx}) = {{{point[0]}, {point[1]}, 0, 1.0}};\n")
        for i, line in enumerate(lines, 1):
            f.write(f"Line({i}) = {{{line[0]}, {line[1]}}};\n")

# Running the function
convert_to_gmsh('./simpleGeometry.xml', './convertedGeometry.geo')
