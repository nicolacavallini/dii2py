import numpy as np
import scipy.sparse as sp

def read_sparsity_pattern(filename):
    """
    Reading the `dealii::SparsityPattern`.

    Parameters
    ----------
    filename : string
        Filename that stores the sparsity pattern.

    Examples
    --------
    >> (rows,cols,rowstart, columns) = read_sparsity_pattern('sp')
    """
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
    """
    Reading the values for `dealii::SparseMatrix<double>`.

    Parameters
    ----------
    filename : string
        Filename that stores the values.

    Examples
    --------
    >> val = read_matrix_values('vls')
    >> matrix = csr_matrix((val, columns, rowstart), (rows, cols))
    """
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

def read_matrix(prefix):
    """
    Reading `dealii::SparseMatrix<double>`.

    Parameters
    ----------
    prefix : string
        Prefix to prepend to the SparsityPattern and Values filenames.
        Supposed the matrix has been saved `prefix_sp` and `prefix_vls`
        for the SparsityPattern and Values respectively.

    Examples
    --------
    >> val = read_matrix_values('vls')
    >> matrix = read_matrix(directory+prefix)
    >> plt.spy(matrix)
    >> plt.show()

    """
    (rows,cols,rowstart, columns) = read_sparsity_pattern(prefix+'_sp')
    val = read_matrix_values(prefix+'_vls')
    return sp.csr_matrix((val, columns, rowstart), (rows, cols))
