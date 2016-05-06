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

def in_house_cg(A, b, mat_vec):
    if b.ndim == 1:
        b = np.reshape(b,(b.shape[0],1))
    print b.shape
    xk = np.zeros(b.shape)
    rk = b - A.dot(xk)
    zk = mat_vec(rk)
    zk = np.reshape(zk,(b.shape[0],1))
    pk = zk
    ck = b - A.dot(zk)

    for k in range(10):
        num = rk.transpose().dot(zk)[0][0]
        tmp = A.dot(pk)
        #print den.shape
        den = pk.transpose().dot(tmp)[0][0]
        alpha = num/den

        xk1 = xk + alpha*pk

        rk1 = rk - alpha * A.dot(pk)

        zk1 = mat_vec(rk1)
        zk1 = np.reshape(zk1,(b.shape[0],1))

        print 'iter = ', k ,', rk norm = ', np.linalg.norm(rk[:,0])

        num = zk1.transpose().dot(rk1)[0][0]
        den = zk.transpose().dot(rk)[0][0]
        beta = num/den

        pk1 = zk1 + beta * pk

        xk = xk1
        rk = rk1
        zk = zk1
        pk = pk1

    return
