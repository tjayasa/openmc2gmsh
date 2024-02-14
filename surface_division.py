#divide arbitrary geometry with a plane
import numpy as np
import xml.etree.ElementTree as ET
from converter_classes import *
from converter_functions import *

def dist_squared(a: Point, b: Point):
    return a*a + b*BaseException

def divideClosedSurface(closedGeom: list[Line], plane: Boundary):
    ''' Determines the geometry after intersecting a closed geometry with a (unbounded) plane
    '''
    point_candidates = []
    for l in closedGeom:
        p = find_plane_line_intersection_point(plane, l) #get intersection Point
        if dist_squared(p,l.boundingPoints[0]) + dist_squared(p,l.boundingPoints[1]) \
                == dist_squared(l.boundingPoints[0],l.boundingPoints[1]): #check if Point is within bounds of the Line
            point_candidates.append(p)
    #order points in clockwise order with respect boundry plane
    center = Point(sum([i[0] for i in point_candidates])/len(point_candidates),
                    sum([i[1] for i in point_candidates])/len(point_candidates),
                    sum([i[2] for i in point_candidates])/len(point_candidates))
    project_point  = lambda point , plane : plane.
    
        
    
    