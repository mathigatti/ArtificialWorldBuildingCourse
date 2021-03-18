import copy
import itertools
import math
import multiprocessing
import os

import numpy as np
from stl import mesh

ON = 1
OFF = 0
CHECKED_OFF = 42
CHECKED_ON = 43

def a_cube(cube_size):
  # Define the 8 vertices of the cube
  vertices = np.array([\
      [-1*cube_size, -1*cube_size, -1*cube_size],
      [+1*cube_size, -1*cube_size, -1*cube_size],
      [+1*cube_size, +1*cube_size, -1*cube_size],
      [-1*cube_size, +1*cube_size, -1*cube_size],
      [-1*cube_size, -1*cube_size, +1*cube_size],
      [+1*cube_size, -1*cube_size, +1*cube_size],
      [+1*cube_size, +1*cube_size, +1*cube_size],
      [-1*cube_size, +1*cube_size, +1*cube_size]])
  # Define the 12 triangles composing the cube
  faces = np.array([\
      [0,3,1],
      [1,3,2],
      [0,4,7],
      [0,7,3],
      [4,5,6],
      [4,6,7],
      [5,1,2],
      [5,2,6],
      [2,3,6],
      [3,7,6],
      [0,1,5],
      [0,5,4]])

  # Create the mesh
  cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
  for i, f in enumerate(faces):
      for j in range(3):
          cube.vectors[i][j] = vertices[f[j],:]
  return cube

def matrix2render(threeDimensionalMatrix):
  cube_size = 1
  cubes = []

  for matrix_i in range(len(threeDimensionalMatrix)):
    for row_i in range(len(threeDimensionalMatrix[matrix_i])):
      for cube_i in range(len(threeDimensionalMatrix[matrix_i][row_i])):
        if threeDimensionalMatrix[matrix_i][row_i][cube_i] == 1:
            new_cube = a_cube(cube_size)

            new_cube.x += cube_size*matrix_i
            new_cube.y += cube_size*row_i
            new_cube.z += cube_size*cube_i

            cubes.append(new_cube.data.copy())

  cubes_mesh = mesh.Mesh(np.concatenate(cubes))

  cubes_mesh.save('data/matrix.stl')

options_full = set(itertools.permutations([1,1,1,-1,-1,-1, 0, 0],3))
options_simple = set(itertools.permutations([1, 0, 0])) | set(itertools.permutations([-1, 0, 0]))

def vecinos42(threeDimensionalMatrix,matrix_i,row_i,cube_i):
  result = 0
  for i,j,k in options_simple:
    if threeDimensionalMatrix[matrix_i+i][row_i+j][cube_i+k] == CHECKED_OFF:
      result += 1
  return result

def vecinos(carray,matrix_i,row_i,cube_i):
  result = 0
  for i,j,k in options_simple:
    if getArrayValue(carray,matrix_i+i,row_i+j,cube_i+k) == ON:
      result += 1
  return result

def updateArray(carray,i,j,k,newvalue):
  carray[i*(matrix_size**2) + j*matrix_size + k] = newvalue

def getArrayValue(carray,i,j,k):
  return carray[i*(matrix_size**2) + j*matrix_size + k]

def applyRule(matrix_indexes):
  
  for i,j,k in matrix_indexes:
    ns = vecinos(carray,i,j,k)
    v = getArrayValue(carray,i,j,k)
    if v == 0 and ns in [1,2,3]:
      updateArray(carray_new,i,j,k,1)
    if v == 1 and ns in [0,5,6]:
      updateArray(carray_new,i,j,k,0)

def matrixDetectBorders(threeDimensionalMatrix):
  result = threeDimensionalMatrix.copy()

  while True:
    for matrix_i in range(1,len(threeDimensionalMatrix)-1):
      for row_i in range(1,len(threeDimensionalMatrix[matrix_i])-1):
        for cube_i in range(1,len(threeDimensionalMatrix[matrix_i][row_i])-1):
          if threeDimensionalMatrix[matrix_i][row_i][cube_i] == OFF and 0 < vecinos42(threeDimensionalMatrix,matrix_i,row_i,cube_i):
            result[matrix_i][row_i][cube_i] = CHECKED_OFF
          elif threeDimensionalMatrix[matrix_i][row_i][cube_i] == ON and 0 < vecinos42(threeDimensionalMatrix,matrix_i,row_i,cube_i):
            result[matrix_i][row_i][cube_i] = CHECKED_ON

    if (result==threeDimensionalMatrix).all():
      return threeDimensionalMatrix

    threeDimensionalMatrix = result

from multiprocessing import Array

def np2array(npmatrix):
  array = Array('i', [0]*(matrix_size**3))

  for matrix_i in range(matrix_size):
    for row_i in range(matrix_size):
      for cube_i in range(matrix_size):
        array[matrix_i*(matrix_size**2) + row_i*matrix_size + cube_i] = npmatrix[matrix_i][row_i][cube_i]

  return array

def array2np(array):

  npmatrix = np.zeros((matrix_size,matrix_size,matrix_size))

  for matrix_i in range(matrix_size):
    for row_i in range(matrix_size):
      for cube_i in range(matrix_size):
        npmatrix[matrix_i][row_i][cube_i] = array[matrix_i*(matrix_size**2) + row_i*matrix_size + cube_i]

  return npmatrix

def initialRandomMatrix():
  threeDimensionalMatrix = np.ones((matrix_size,matrix_size,matrix_size)).astype(int)*CHECKED_OFF
  threeDimensionalMatrix[1:-1,1:-1,1:-1] = (np.random.rand(matrix_size-2,matrix_size-2,matrix_size-2)>0.9).astype(int)
  return threeDimensionalMatrix


def initialMatrix():
  threeDimensionalMatrix = np.ones((matrix_size,matrix_size,matrix_size)).astype(int)*CHECKED_OFF
  threeDimensionalMatrix[1:-1,1:-1,1:-1] = np.zeros((matrix_size-2,matrix_size-2,matrix_size-2))
  middle = int(matrix_size/2)
  threeDimensionalMatrix[middle][middle][middle] = ON
  return threeDimensionalMatrix

if __name__ == '__main__':
  threeDimensionalMatrix = np.load("data/test.npy")
  #threeDimensionalMatrix = matrixDetectBorders(threeDimensionalMatrix)
  matrix2render(threeDimensionalMatrix)