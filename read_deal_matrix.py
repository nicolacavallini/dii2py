import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import *

from dii2py import *

if __name__ == "__main__":

    directory = './build/' # suppose you run the c++ in the build desirectory

    (rows,cols,rowstart, columns) = read_sparsity_pattern(directory+'sp')
    val = read_matrix_values(directory+'vls')

    matrix = csr_matrix((val, columns, rowstart), (rows, cols))
    print matrix.todense()
