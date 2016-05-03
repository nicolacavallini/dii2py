import numpy as np
<<<<<<< HEAD:read_deal_matrix.py
import matplotlib.pyplot as plt
from scipy.sparse import *
=======
import scipy.sparse as sp

def stampa():
    print 'sono un cretino'
    return
>>>>>>> read_matrix:__init__.py

from dii2py import *

def read_matrix(prefix):
    """
    Reading `dealii::SparseMatrix<double>`.

    Parameters
    ----------
    prefix : string
        Prefix to prepend to the SparsityPattern and Values filenames.

    Examples
    --------
    >> val = read_matrix_values('vls')
    >> matrix = read_matrix(directory+prefix)
    >> plt.spy(matrix)
    >> plt.show()

    """
    (rows,cols,rowstart, columns) = read_sparsity_pattern(directory+'sp')
    val = read_matrix_values(directory+'vls')
    return sp.csr_matrix((val, columns, rowstart), (rows, cols))
