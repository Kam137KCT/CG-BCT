import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_cube(vertices, edges, axis_line=None, ax=None, title=""):
    """Plot cube and rotation axis"""
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    # Plot vertices (only the first 3 columns for X, Y, Z)
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='blue')
    # Plot edges
    for edge in edges:
        ax.plot([vertices[edge[0], 0], vertices[edge[1], 0]],
                [vertices[edge[0], 1], vertices[edge[1], 1]],
                [vertices[edge[0], 2], vertices[edge[1], 2]], 'b-')

    # Plot rotation axis
    if axis_line is not None:
        ax.plot([axis_line[0], axis_line[3]],
                [axis_line[1], axis_line[4]],
                [axis_line[2], axis_line[5]], 'r--', linewidth=2, label='Rotation Axis')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    return ax

def translate_matrix(tx, ty, tz):
    """Create translation matrix"""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotate_x_matrix(angle):
    """Create rotation matrix for x-axis in radians"""
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def rotate_y_matrix(angle):
    """Create rotation matrix for y-axis in radians"""
    return np.array([
        [np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def rotate_z_matrix(angle):
    """Create rotation matrix for z-axis in radians"""
    return np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def arbitrary_rotation_matrix(x1, y1, z1, x2, y2, z2, angle):
    # Convert angle to radians
    angle = np.radians(angle)

    # Normalize the axis of rotation
    v = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    a = (x2 - x1) / v
    b = (y2 - y1) / v
    c = (z2 - z1) / v

    # Step 1: Translate to the origin
    T1 = translate_matrix(-x1, -y1, -z1)

    # Step 2: Rotation about the axis
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    
    # Construct the rotation matrix for the arbitrary axis
    R = np.array([
        [cos_angle + a**2 * (1 - cos_angle), a * b * (1 - cos_angle) - c * sin_angle, a * c * (1 - cos_angle) + b * sin_angle, 0],
        [b * a * (1 - cos_angle) + c * sin_angle, cos_angle + b**2 * (1 - cos_angle), b * c * (1 - cos_angle) - a * sin_angle, 0],
        [c * a * (1 - cos_angle) - b * sin_angle, c * b * (1 - cos_angle) + a * sin_angle, cos_angle + c**2 * (1 - cos_angle), 0],
        [0, 0, 0, 1]
    ])

    # Step 3: Inverse translation to return to original position
    T2 = translate_matrix(x1, y1, z1)

    # Final rotation matrix
    rotation_matrix = T2 @ R @ T1
    return rotation_matrix

def create_cube():
    """Create vertices and edges of a cube"""
    vertices = np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 1]
    ])
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    return vertices, edges

def transform_vertices(vertices, matrix):
    """Transform vertices using matrix multiplication"""
    transformed = (matrix @ vertices.T).T  # Apply the transformation matrix
    return transformed[:, :3]  # Only take the first three columns (X, Y, Z)

def main():
    # Create cube
    vertices, edges = create_cube()

    # Define rotation axis and angle
    x1, y1, z1 = [2, 1, 0]  # First point of axis
    x2, y2, z2 = [3, 3, 1]  # Second point of axis
    angle = 90  # degrees

    # Get composite transformation matrix
    composite = arbitrary_rotation_matrix(x1, y1, z1, x2, y2, z2, angle)

    # Transform vertices using matrix multiplication
    transformed_vertices = transform_vertices(vertices, composite)
    print(transformed_vertices)

    # Visualization
    fig = plt.figure(figsize=(12, 5))

    # Original cube
    ax1 = fig.add_subplot(121, projection='3d')
    plot_cube(vertices, edges, [x1, y1, z1, x2, y2, z2], ax1, "Original Cube")

    # Transformed cube
    ax2 = fig.add_subplot(122, projection='3d')
    plot_cube(transformed_vertices, edges, [x1, y1, z1, x2, y2, z2], ax2, f"Rotated {angle}° around axis")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
