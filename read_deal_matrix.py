# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 16:28:02 2014

@author: nicola
"""
import numpy as np
from scipy.sparse import *

def read_sparsity_pattern(filename):
    header = ''
    with open(filename,'r') as f:
        byte = f.read(1)
        while (byte!=']'):        
            header += byte
            byte = f.read(1)
        header = header[1:]
        data = [int(n) for n in header.split()]
        [max_dim,\
        rows,\
        cols,\
        max_vec_len,\
        max_row_length,\
        compressed,\
        store_diagonal_first_in_row] = data    
        brakets = f.read(1)
        rowstart = np.fromfile(f, dtype=np.uint64, count=rows+1)
        brakets = f.read(2)
        columns =  np.fromfile(f, dtype=np.uint64, count=max_vec_len)
    return rows,cols,rowstart, columns
    
def read_matrix_values(filename):
    header = ''
    with open(filename,'r') as f:
        byte = f.read(1)
        while (byte!=']'):        
            header += byte
            byte = f.read(1)
        header = header[1:]
        max_len = int(header)
        brakets = f.read(1)
        val = np.fromfile(f, dtype=np.float64, count=max_len)
    return val
        
if __name__ == "__main__":
    
    (rows,cols,rowstart, columns) = read_sparsity_pattern('sp')
    val = read_matrix_values('vls')
    
    matrix = csr_matrix((val, columns, rowstart), (rows, cols))
    print matrix.todense()