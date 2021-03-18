import bpy
import numpy as np

with open('data/test.npy', 'rb') as f:
    matrix_3d = np.load(f)

i = 0
for matrix_2d in matrix_3d:
    j = 0
    for row in matrix_2d:
        k = 0
        for value in row:
            if value == 1:
                bpy.ops.mesh.primitive_cube_add(location=(i,j,k))
            k += 1
        j+=1
    i+=1