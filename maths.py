import math
import pygame


def distance_segment_to_point(A: pygame.Vector2, B: pygame.Vector2, C: pygame.Vector2):
    # Compute vectors AC and AB
    AC = sub(C, A)
    AB = sub(B, A)

    # Get point D by taking the projection of AC onto AB then adding the offset of A
    D = add(proj(AC, AB), A)

    AD = sub(D, A)
    # D might not be on AB so calculate k of D down AB (aka solve AD = k * AB)
    # We can use either component, but choose larger value to reduce the chance of dividing by zero
    k = abs(AB.x) > abs(AB.y)
    k = AD.x / AB.x if k else AD.y / AB.y

    # Check if D is off either end of the line segment
    if k <= 0.0:
        return math.sqrt(hypot2(C, A))
    elif k >= 1.0:
        return math.sqrt(hypot2(C, B))

    return math.sqrt(hypot2(C, D))


# Define some common functions for working with vectors
def add(a, b):
    return pygame.Vector2(a.x + b.x, a.y + b.y)


def sub(a, b):
    return pygame.Vector2(a.x - b.x, a.y - b.y)


def dot(a, b):
    return a.x * b.x + a.y * b.y


def hypot2(a, b):
    return dot(sub(a, b), sub(a, b))


def proj(a, b):
    k = dot(a, b) / dot(b, b)
    return pygame.Vector2(k * b.x, k * b.y)


def is_point_in_sector(px, py, cx, cy, radius, start_angle, end_angle):
    # Calculate the distance from the center to the point
    dx = px - cx
    dy = py - cy
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Check if the point is within the radius
    if distance > radius:
        return False

    # Calculate the angle of the point
    angle = math.atan2(dy, dx)  # Angle in radians

    # Normalize angles to be within [0, 2π]
    angle = angle % (2 * math.pi)

    # Check if the angle is within the sector's angles
    if start_angle < end_angle:
        return start_angle <= angle <= end_angle
    else:  # Sector wraps around 0 radians
        return angle >= start_angle or angle <= end_angle


def is_rectangle_in_sector(rect_x, rect_y, rect_w, rect_h, cx, cy, radius, start_angle, end_angle):
    # Define the corners of the rectangle
    corners = [
        (rect_x, rect_y),  # Top-left
        (rect_x + rect_w, rect_y),  # Top-right
        (rect_x, rect_y + rect_h),  # Bottom-left
        (rect_x + rect_w, rect_y + rect_h)  # Bottom-right
    ]

    # Check each corner
    for corner in corners:
        if is_point_in_sector(corner[0], corner[1], cx, cy, radius, start_angle, end_angle):
            return True  # At least one corner is inside the sector

    # Check each edge of the rectangle
    edges = [
        ((rect_x, rect_y), (rect_x + rect_w, rect_y)),  # Top edge
        ((rect_x, rect_y), (rect_x, rect_y + rect_h)),  # Left edge
        ((rect_x + rect_w, rect_y), (rect_x + rect_w, rect_y + rect_h)),  # Right edge
        ((rect_x, rect_y + rect_h), (rect_x + rect_w, rect_y + rect_h))  # Bottom edge
    ]

    for edge in edges:
        if does_edge_intersect_sector(edge[0], edge[1], cx, cy, radius, start_angle, end_angle):
            return True  # At least one edge intersects the sector

    return False  # No corners or edges are inside the sector


def does_edge_intersect_sector(start, end, cx, cy, radius, start_angle, end_angle):
    # Check multiple points along the edge
    steps = 20  # Number of points to check along the edge
    for i in range(steps + 1):
        t = i / steps
        px = start[0] * (1 - t) + end[0] * t
        py = start[1] * (1 - t) + end[1] * t
        if is_point_in_sector(px, py, cx, cy, radius, start_angle, end_angle):
            return True
    return False
