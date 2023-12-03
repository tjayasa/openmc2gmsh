import xml.etree.ElementTree as ET

def parse_openmc_plane(surface):
    """Parse OpenMC surface and return Gmsh points and lines."""
    coeffs = [float(c) for c in surface.get('coeffs').split()]
    a, b, c, d = coeffs
    # print(f"Processing surface with coeffs: {coeffs}")  # Debug print

    if a == 0 and b == 0:
        # Vertical line parallel to Y-axis
        return [(d/c, -10), (d/c, 10)]
    elif a == 0 and c == 0:
        # Horizontal line parallel to X-axis
        return [(-10, d/b), (10, d/b)]
    elif b == 0 and c == 0:
        # Vertical line parallel to Z-axis, intersecting X-axis
        return [(-d/a, -10), (-d/a, 10)]
    else:
        raise ValueError("Unsupported surface type")

def parse_openmc_quadric(surface):
    """Parse OpenMC quadric and return Gmsh command."""
    coeffs = [float(c) for c in surface.get('coeffs').split()]
    # Assuming coeffs define the quadric in some manner
    # This is a placeholder logic; real implementation depends on the actual quadric definition

    # Here's a placeholder for an ellipsoid; you'll need different logic for other types
    a, b, c, center_x, center_y, center_z = coeffs[:6]
    return f"Ellipsoid({{{center_x}, {center_y}, {center_z}}}, {a}, {b}, {c});"

def parse_openmc_torus(surface):
    """Parse OpenMC torus and return Gmsh command."""
    coeffs = [float(c) for c in surface.get('coeffs').split()]
    # Assuming coeffs represent [inner radius, outer radius, center_x, center_y, center_z, ...]
    inner_radius, outer_radius, center_x, center_y, center_z = coeffs[:5]

    # This is a placeholder syntax; adjust according to Gmsh's torus definition
    return f"Torus({{{center_x}, {center_y}, {center_z}}}, {inner_radius}, {outer_radius});"

def convert_to_gmsh(openmc_file, gmsh_file):
    """Convert OpenMC geometry to Gmsh format."""
    try:
        tree = ET.parse(openmc_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return

    points = {}
    lines = []
    other_geometries = []  # For storing non-plane geometries

    # Process each surface in the OpenMC file
    for surface in root.findall('surface'):
        surface_type = surface.get('type')
        try:
            if surface_type == 'plane':
                line_points = parse_openmc_plane(surface)
                line = []
                for point in line_points:
                    if point not in points:
                        points[point] = len(points) + 1
                    line.append(points[point])
                lines.append(tuple(line))
            elif surface_type == 'torus':
                torus_data = parse_openmc_torus(surface)
                other_geometries.append(torus_data)
            # Add more elif blocks for other types
            elif surface_type == 'quadric':
                quadric_data = parse_openmc_quadric(surface)
                other_geometries.append(quadric_data)
            else:
                print(f"Skipping unsupported surface type: {surface_type}")
        except ValueError as e:
            print(f"Skipping surface due to error: {e}")

    # Write to Gmsh file
    with open(gmsh_file, 'w') as f:
        for point, idx in points.items():
            f.write(f"Point({idx}) = {{{point[0]}, {point[1]}, 0, 1.0}};\n")
        for i, line in enumerate(lines, 1):
            f.write(f"Line({i}) = {{{line[0]}, {line[1]}}};\n")
        for geometry in other_geometries:
            f.write(f"{geometry}\n")  # Write other geometries like tori


# Running the function
convert_to_gmsh('/Users/webberqu417/Desktop/NERS/570/Project/simpleQuadric.xml', '/Users/webberqu417/Desktop/NERS/570/Project/convertedQuadric.geo')
