#! /usr/bin/env python3
import sys

from solid import scad_render_to_file
from solid.objects import cube
from solid.utils import right, up, forward
import numpy as np

def matrix2render(threeDimensionalMatrix):
	distance = 15
	cube_size = 1

	figure = cube([0.1, 0.1, 0.1], center=True)
	for matrix_i in range(len(threeDimensionalMatrix)):
		for row_i in range(len(threeDimensionalMatrix[matrix_i])):
			for cube_i in range(len(threeDimensionalMatrix[matrix_i][row_i])):
				if threeDimensionalMatrix[matrix_i][row_i][cube_i] == 1:
				    new_cube = right(matrix_i*cube_size)(cube([cube_size, cube_size, cube_size], center=True))
				    new_cube = up(row_i*cube_size)(new_cube)
				    new_cube = forward(cube_i*cube_size)(new_cube)

				    figure += new_cube

	SEGMENTS = 48
	file_out = scad_render_to_file(figure)
	print(f"{__file__}: SCAD file written to: \n{file_out}")

if __name__ == '__main__':
	matrix_size = 30
	threeDimensionalMatrix = np.load("data/test.npy")
	figure = matrix2render(threeDimensionalMatrix)
