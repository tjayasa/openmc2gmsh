import numpy as np
from converter_classes import *

def find_intersection_line(plane1, plane2):
    """Find the line of intersection between two planes."""

    a1 = plane1.coeffs["a"]
    b1 = plane1.coeffs["b"]
    c1 = plane1.coeffs["c"]
    d1 = plane1.coeffs["d"]

    a2 = plane2.coeffs["a"]
    b2 = plane2.coeffs["b"]
    c2 = plane2.coeffs["c"]
    d2 = plane2.coeffs["d"]
    
    normal_vector1 = np.array([a1, b1, c1])
    normal_vector2 = np.array([a2, b2, c2])

    #Normalizing the normal vectors:
    normal_vector1 = normal_vector1/np.linalg.norm(normal_vector1)
    normal_vector2 = normal_vector2/np.linalg.norm(normal_vector2)

    #Check that the two planes are not parallel (i.e. non-intersecting):
    if not do_planes_intersect(plane1, plane2):
        print("Planes Do Not Intersect!")
        return None

    direction_vector = np.cross(normal_vector1, normal_vector2)

    #Normalizing the line direction vector:
    direction_vector = direction_vector/np.linalg.norm(direction_vector)

    #print(direction_vector)

    if direction_vector[2] != 0:
        
        #Calculate x:
        if b2 == 0:
            x = d2/a2
        else:    
            x = (d1 - (b1*d2)/(b2))/(a1 - (b1*a2)/(b2))

        #Calculate y:
        if a2 == 0:
            y = d2/b2
        else:
            y = (d1 - (a1*d2)/(a2))/(b1 - (a1*b2)/(a2))

        #Fix z=0:
        z = 0

    elif direction_vector[1] != 0:

        #Calculate x:
        if c2 == 0:
            x = d2/a2
        else:
            x = (d1 - (c1*d2)/(c2))/(a1 - (c1*a2)/(c2))

        #Fix y=0:
        y = 0

        #Calculate z:
        if a2 == 0:
            z = d2/c2
        else:
            z = (d1 - (a1*d2)/(a2))/(c1 - (a1*c2)/(a2))

    elif direction_vector[0] != 0:

        #Fix x=0:
        x = 0

        #Calculate y:
        if c2 == 0:
            y = d2/b2
        else:
            y = (d1 - (c1*d2)/(c2))/(b1 - (c1*b2)/(c2))

        #Calculate z:
        if b2 == 0:
            z = d2/c2
        else:
            z = (d1 - (b1*d2)/(b2))/(c1 - (b1*c2)/(b2))

    else:
        raise ValueError("Orientation Vector Equals Zero Vector!")

    print(f"Point: ({x}, {y}, {z}), Direction: <{direction_vector[0]}, {direction_vector[1]}, {direction_vector[2]},>")

    intersection_line = line("straight")
    intersection_line.setCoefficients(x, y, z, direction_vector[0], direction_vector[1], direction_vector[2])

    return intersection_line


def do_planes_intersect(plane1, plane2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    a1 = plane1.coeffs["a"]
    b1 = plane1.coeffs["b"]
    c1 = plane1.coeffs["c"]

    a2 = plane2.coeffs["a"]
    b2 = plane2.coeffs["b"]
    c2 = plane2.coeffs["c"]

    normal_vector1 = np.array([a1, b1, c1])
    normal_vector2 = np.array([a2, b2, c2])

    #Normalizing the normal vectors:
    normal_vector1 = normal_vector1/np.linalg.norm(normal_vector1)
    normal_vector2 = normal_vector2/np.linalg.norm(normal_vector2)

    #tolerance = 1e-5
    #print(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon])))

    return (not np.allclose(normal_vector1, normal_vector2))

def find_plane_line_intersection_point(plane1, line1):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    x0 = line1.coeffs["x0"]
    y0 = line1.coeffs["y0"]
    z0 = line1.coeffs["z0"]
    alpha = line1.coeffs["alpha"]
    beta = line1.coeffs["beta"]
    epsilon = line1.coeffs["epsilon"]

    a = plane1.coeffs["a"]
    b = plane1.coeffs["b"]
    c = plane1.coeffs["c"]
    d = plane1.coeffs["d"]

    if not does_line_intersect_plane(plane1, line1):
        raise ValueError("Requested Line and Plane do not Intersect")

    t = (d - (a*x0) - (b*y0) - (c*z0))/((alpha*a) + (beta*b) + (epsilon*c))

    x = x0 + (alpha*t)
    y = y0 + (beta*t)
    z = z0 + (epsilon*t)

    intersection_point = point(x, y, z)
    return intersection_point

    print(f"Point ({x}, {y}, {z})")

def does_line_intersect_plane(plane1, line1):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    alpha = line1.coeffs["alpha"]
    beta = line1.coeffs["beta"]
    epsilon = line1.coeffs["epsilon"]

    a = plane1.coeffs["a"]
    b = plane1.coeffs["b"]
    c = plane1.coeffs["c"]

    tolerance = 1e-5

    #print(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon])))

    return(abs(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon]))) > tolerance)

def find_line_line_intersection_point(line1, line2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    tolerance = 1e-5

    x01 = line1.coeffs["x0"]
    y01 = line1.coeffs["y0"]
    z01 = line1.coeffs["z0"]
    alpha1 = line1.coeffs["alpha"]
    beta1 = line1.coeffs["beta"]
    epsilon1 = line1.coeffs["epsilon"]

    x02 = line2.coeffs["x0"]
    y02 = line2.coeffs["y0"]
    z02 = line2.coeffs["z0"]
    alpha2 = line2.coeffs["alpha"]
    beta2 = line2.coeffs["beta"]
    epsilon2 = line2.coeffs["epsilon"]

    p1 = np.array([x01, y01, z01])
    p2 = np.array([x02, y02, z02])

    v1 = np.array([alpha1, beta1, epsilon1])
    v2 = np.array([alpha2, beta2, epsilon2])

    a = np.array([[alpha1, -1*alpha2], [beta1, -1*beta2], [epsilon1, -1*epsilon2]])
    b = np.array([[x02 - x01], [y02 - y01], [z02 - z01]])

    t = np.linalg.lstsq(a,b,rcond=None)[0][0]
    #print(f"t = {t}")

    x = x01 + alpha1*t
    y = y01 + beta1*t
    z = z01 + epsilon1*t

    intersection_point = point(x, y, z)
    #print(f"Intersection point = ({x}, {y}, {z})")
    return intersection_point



def do_lines_intersect(line1, line2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Vector form of a line:
    # Line = p + (Real Number)*v

    tolerance = 1e-5

    x01 = line1.coeffs["x0"]
    y01 = line1.coeffs["y0"]
    z01 = line1.coeffs["z0"]
    alpha1 = line1.coeffs["alpha"]
    beta1 = line1.coeffs["beta"]
    epsilon1 = line1.coeffs["epsilon"]

    x02 = line2.coeffs["x0"]
    y02 = line2.coeffs["y0"]
    z02 = line2.coeffs["z0"]
    alpha2 = line2.coeffs["alpha"]
    beta2 = line2.coeffs["beta"]
    epsilon2 = line2.coeffs["epsilon"]

    p1 = np.array([x01, y01, z01])
    p2 = np.array([x02, y02, z02])

    v1 = np.array([alpha1, beta1, epsilon1])/np.linalg.norm([alpha1, beta1, epsilon1])
    v2 = np.array([alpha2, beta2, epsilon2])/np.linalg.norm([alpha2, beta2, epsilon2])

    if np.allclose(abs(v1), abs(v2)): #Check for parallel lines (will not intersect)
        return False
    else:
        return (abs(np.dot(np.cross(v1, v2), (p1-p2))) < tolerance)

def is_point_within_bounds(input_point, xmin, xmax, ymin, ymax, zmin, zmax):

    tolerance = 1e-5
    
    x_within_range = (input_point.x >= xmin-tolerance) and (input_point.x  <= xmax+tolerance)
    y_within_range = (input_point.y  >= ymin-tolerance) and (input_point.y  <= ymax+tolerance)
    z_within_range = (input_point.z  >= zmin-tolerance) and (input_point.z  <= zmax+tolerance)
    
    return (x_within_range and y_within_range and z_within_range)

def find_plane_bounding_points(plane1, top_boundary, bottom_boundary, front_boundary, back_boundary, right_boundary, left_boundary):

    xmin = left_boundary.coeffs["d"]
    xmax = right_boundary.coeffs["d"]
    ymin = back_boundary.coeffs["d"]
    ymax = front_boundary.coeffs["d"]
    zmin = bottom_boundary.coeffs["d"]
    zmax = top_boundary.coeffs["d"]

    list_of_boundaries = [top_boundary, bottom_boundary, front_boundary, back_boundary, left_boundary, right_boundary]


    list_of_intersects = []
    list_intersect_nums = []
    bounding_points = []

    for i in range(0,6):
        intersect =  find_intersection_line(plane1, list_of_boundaries[i])
        if intersect is not None:
            list_of_intersects.append(intersect)

    i = 0
    print(len(list_of_intersects))

    for index1 in range(0,len(list_of_intersects)):
        for index2 in range(index1+1,len(list_of_intersects)):

            if do_lines_intersect(list_of_intersects[index1], list_of_intersects[index2]):

                point = find_line_line_intersection_point(list_of_intersects[index1], list_of_intersects[index2])
                #print (f"Lines {index1} and {index2} intersect.")

                if is_point_within_bounds(point, xmin, xmax, ymin, ymax, zmin, zmax):

                    print (f"Lines {index1} and {index2} intersect in bounds.")
                    #print(f"Intersection Point ({point.x}, {point.y}, {point.z}) is within bounds")
                    bounding_points.append(point)

                    if list_of_intersects[index1].gmsh_id not in plane1.boundingLineIDs:
                        plane1.addBoundingLine(list_of_intersects[index1])

                    if list_of_intersects[index2].gmsh_id not in plane1.boundingLineIDs:
                        plane1.addBoundingLine(list_of_intersects[index2])

                    list_intersect_nums.append(index2)

                    list_of_intersects[index1].addBoundingPoint(point)
                    list_of_intersects[index2].addBoundingPoint(point)
                
            #i = i+1


    for point in bounding_points:
        print(f"Point({point.gmsh_id}) = {'{'} {round(float(point.x), 5)}, {round(float(point.y), 5)}, {round(float(point.z), 5)}{'}'};")

    for line in plane1.boundingLines:
        print(f"Line({line.gmsh_id}) = {'{'} {line.boundingPoints[0].gmsh_id}, {line.boundingPoints[1].gmsh_id}{'}'};")

    print(len(plane1.boundingLines))
    print(plane1.boundingLineIDs)

#def write_gmsh_reprsentation(input_surface, dimensionality)

#def find_bounding_points(plane1):
