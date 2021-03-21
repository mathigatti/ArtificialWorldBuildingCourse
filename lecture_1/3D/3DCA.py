import multiprocessing
from multiprocessing import Manager
import itertools

import numpy as np
from tqdm import tqdm

moore_neighbourhood = set(itertools.permutations([1,-1]*3 + [0,0], 3))
vonneumann_neighbourhood = [(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)]
neighbourhood = vonneumann_neighbourhood
def parse_results(results):
  new_matrix = [[[0 for _ in range(matrix_size)] for _ in range(matrix_size)] for _ in range(matrix_size)]
  for result in results:
    i, j, k, v = result
    new_matrix[i][j][k] = v
  return np.array(new_matrix)

matrix_size = 100
interval = 10
matrix = np.zeros((matrix_size,matrix_size,matrix_size)).astype(int)

size = int(matrix_size/2+interval)-int(matrix_size/2-interval)

matrix[int(matrix_size/2-interval):int(matrix_size/2+interval),int(matrix_size/2-interval):int(matrix_size/2+interval),int(matrix_size/2-interval):int(matrix_size/2+interval)] = np.random.randint(2, size=(size,size,size))

cells = [(i,j,k) for i in range(1, matrix_size-1) for j in range(1,matrix_size-1) for k in range(1,matrix_size-1)]

def apply_rule(coordinates):
  i, j, k = coordinates

  alive = (matrix[i,j,k] == 1)
  neighbours = sum(matrix[i+i2,j+j2,k+k2] for i2,j2,k2 in neighbourhood)
  #print(neighbours)
  if not alive and neighbours in [1,3]:
    return (i, j, k, 1)
  if alive and neighbours in range(0,7):
    return (i, j, k, 1)
  else:
    return (i, j, k, 0)

iterations = 20
cpus = multiprocessing.cpu_count()

for _ in tqdm(range(iterations)):
  with multiprocessing.Pool(processes=cpus) as pool:
    results = pool.map(apply_rule, cells)
  matrix = parse_results(results)

with open('data/test.npy', 'wb') as f:
    np.save(f, matrix)
