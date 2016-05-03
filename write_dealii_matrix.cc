#include <iostream>
#include <fstream>

#include <deal.II/lac/sparsity_pattern.h>
#include <deal.II/lac/sparse_matrix.h>

using namespace std;
using namespace dealii;

using s_t =  dealii::SparsityPattern::size_type ;

int main()
{
    const s_t m = 5;
    SparsityPattern sp(m,m,3);
    SparseMatrix<double> matrix;

    for (s_t i = 0; i<m ; i++)
       sp.add(i,i);

    for (s_t i = 0; i<m-1 ; i++)
    {
       sp.add(i,i+1);
       sp.add(i+1,i);
    }
    sp.compress();

    matrix.reinit(sp);

    for (s_t i = 0; i<m ; i++)
       matrix.set(i,i,3);

    for (s_t i = 0; i<m-1 ; i++)
    {
       matrix.set(i,i+1,2.);
       matrix.set(i+1,i,2.);
    }

    ofstream out_file;
    out_file.open("sp");
    sp.block_write(out_file);
    out_file.close();
    out_file.clear();

    out_file.open("vls");
    matrix.block_write(out_file);
    out_file.close();

    cout << "... done!" << endl;
    return 0;
}
