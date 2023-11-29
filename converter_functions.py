import numpy as np

def find_intersection_line(plane_dict1, plane_dict2):
    """Find the line of intersection between two planes."""

    a1 = plane_dict1["a"]
    b1 = plane_dict1["b"]
    c1 = plane_dict1["c"]
    d1 = plane_dict1["d"]

    a2 = plane_dict2["a"]
    b2 = plane_dict2["b"]
    c2 = plane_dict2["c"]
    d2 = plane_dict2["d"]
    
    normal_vector1 = np.array([a1, b1, c1])
    normal_vector2 = np.array([a2, b2, c2])

    #Normalizing the normal vectors:
    normal_vector1 = normal_vector1/np.linalg.norm(normal_vector1)
    normal_vector2 = normal_vector2/np.linalg.norm(normal_vector2)

    #Check that the two planes are not parallel (i.e. non-intersecting):
    if not do_planes_intersect(plane_dict1, plane_dict2):
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

    return {"x0":x, "y0":y, "z0":z, "alpha":direction_vector[0], "beta":direction_vector[1], "epsilon":direction_vector[2]}


def do_planes_intersect(plane_dict1, plane_dict2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    a1 = plane_dict1["a"]
    b1 = plane_dict1["b"]
    c1 = plane_dict1["c"]

    a2 = plane_dict2["a"]
    b2 = plane_dict2["b"]
    c2 = plane_dict2["c"]

    normal_vector1 = np.array([a1, b1, c1])
    normal_vector2 = np.array([a2, b2, c2])

    #Normalizing the normal vectors:
    normal_vector1 = normal_vector1/np.linalg.norm(normal_vector1)
    normal_vector2 = normal_vector2/np.linalg.norm(normal_vector2)

    #tolerance = 1e-5
    #print(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon])))

    return (not np.allclose(normal_vector1, normal_vector2))

def find_plane_line_intersection_point(plane_dict, line_dict):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    x0 = line_dict["x0"]
    y0 = line_dict["y0"]
    z0 = line_dict["z0"]
    alpha = line_dict["alpha"]
    beta = line_dict["beta"]
    epsilon = line_dict["epsilon"]

    a = plane_dict["a"]
    b = plane_dict["b"]
    c = plane_dict["c"]
    d = plane_dict["d"]

    if not does_line_intersect_plane(plane_dict, line_dict):
        raise ValueError("Requested Line and Plane do not Intersect")

    t = (d - (a*x0) - (b*y0) - (c*z0))/((alpha*a) + (beta*b) + (epsilon*c))

    x = x0 + (alpha*t)
    y = y0 + (beta*t)
    z = z0 + (epsilon*t)

    print(f"Point ({x}, {y}, {z})")

def does_line_intersect_plane(plane_dict, line_dict):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Equation of a Plane:
    # Ax + By + Cz = D

    alpha = line_dict["alpha"]
    beta = line_dict["beta"]
    epsilon = line_dict["epsilon"]

    a = plane_dict["a"]
    b = plane_dict["b"]
    c = plane_dict["c"]

    tolerance = 1e-5

    #print(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon])))

    return(abs(np.dot(np.array([a, b, c]), np.array([alpha, beta, epsilon]))) > tolerance)

def find_line_line_intersection_point(line_dict1, line_dict2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    tolerance = 1e-5

    x01 = line_dict1["x0"]
    y01 = line_dict1["y0"]
    z01 = line_dict1["z0"]
    alpha1 = line_dict1["alpha"]
    beta1 = line_dict1["beta"]
    epsilon1 = line_dict1["epsilon"]

    x02 = line_dict2["x0"]
    y02 = line_dict2["y0"]
    z02 = line_dict2["z0"]
    alpha2 = line_dict2["alpha"]
    beta2 = line_dict2["beta"]
    epsilon2 = line_dict2["epsilon"]

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

    #print(f"Intersection point = ({x}, {y}, {z})")
    return [x, y, z]



def do_lines_intersect(line_dict1, line_dict2):
    #Parametric Form of 3D Line:
    # x = x0 + alpha*t
    # y = y0 + beta*t
    # z = z0 + epsilon*t

    #Vector form of a line:
    # Line = p + (Real Number)*v

    tolerance = 1e-9

    x01 = line_dict1["x0"]
    y01 = line_dict1["y0"]
    z01 = line_dict1["z0"]
    alpha1 = line_dict1["alpha"]
    beta1 = line_dict1["beta"]
    epsilon1 = line_dict1["epsilon"]

    x02 = line_dict2["x0"]
    y02 = line_dict2["y0"]
    z02 = line_dict2["z0"]
    alpha2 = line_dict2["alpha"]
    beta2 = line_dict2["beta"]
    epsilon2 = line_dict2["epsilon"]

    p1 = np.array([x01, y01, z01])
    p2 = np.array([x02, y02, z02])

    v1 = np.array([alpha1, beta1, epsilon1])/np.linalg.norm([alpha1, beta1, epsilon1])
    v2 = np.array([alpha2, beta2, epsilon2])/np.linalg.norm([alpha2, beta2, epsilon2])

    if np.allclose(abs(v1), abs(v2)): #Check for parallel lines (will not intersect)
        return False
    else:
        return (abs(np.dot(np.cross(v1, v2), (p1-p2))) < tolerance)

def is_point_within_bounds(x, y, z, xmin, xmax, ymin, ymax, zmin, zmax):

    tolerance = 1e-5
    
    x_within_range = (x >= xmin-tolerance) and (x <= xmax+tolerance)
    y_within_range = (y >= ymin-tolerance) and (y <= ymax+tolerance)
    z_within_range = (z >= zmin-tolerance) and (z <= zmax+tolerance)
    
    return (x_within_range and y_within_range and z_within_range)