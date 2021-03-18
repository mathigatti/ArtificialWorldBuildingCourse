from vapory import *
import numpy as np

def matrix2render(threeDimensionalMatrix, output_path):
	distance = 4
	cube_size = 0.1

	camera = Camera('location', [distance, distance, distance], 'look_at', [0, 0, 0])
	light = LightSource([distance, 4*distance, 4*distance], 'color', [1, 1, 1])

	figure = []
	for matrix_i in range(len(threeDimensionalMatrix)):
		for row_i in range(len(threeDimensionalMatrix[matrix_i])):
			for cube_i in range(len(threeDimensionalMatrix[matrix_i][row_i])):
				if threeDimensionalMatrix[matrix_i][row_i][cube_i] == 1:
					new_cube = Box( [matrix_i*cube_size, row_i*cube_size, cube_i*cube_size], [ matrix_i*cube_size + cube_size, row_i*cube_size + cube_size, cube_i*cube_size + cube_size ], Texture( Pigment( 'color', [1, 1, 1] )))
					figure.append(new_cube)

	scene = Scene(camera, objects= [light]+ figure)
	scene.render(output_path, width=400, height=300)

threeDimensionalMatrix = np.load("data/test.npy")

matrix2render(threeDimensionalMatrix, "data/test.png")