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
    if np.allclose(normal_vector1, normal_vector2):
        print("Planes Do Not Intersect!")
        return [0, 0, 0, 0, 0, 0]

    direction_vector = np.cross(normal_vector1, normal_vector2)

    #Normalizing the line direction vector:
    direction_vector = direction_vector/np.linalg.norm(direction_vector)

    print(direction_vector)

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

    return [x, y, z, direction_vector[0], direction_vector[1], direction_vector[2]]