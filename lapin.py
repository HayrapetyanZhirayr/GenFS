import numpy as np

ZERO_BOUND = 10 ** (-8)
ENTITY_BOUND = 10 ** (-4)

def lapin(A):
    '''
    '''
    A = (A + A.T) / 2
    a_sums = np.ravel(abs(sum(A)))
    checked = np.array(a_sums > ENTITY_BOUND)
    is_correct = checked.all()

    if not is_correct:
        print('These entities are no good - remove them first!!!')
        print([i for i, j in enumerate(checked, 1) if not j])
        A = A[:, checked][checked, :]
        a_sums = a_sums[checked]

    matrix_dim, _ = A.shape
    C = np.empty((matrix_dim, matrix_dim))
    for i in range(matrix_dim):
        for j in range(matrix_dim):
            C[i, j] = A[i, j] / np.sqrt(a_sums[i] * a_sums[j])

    eig_vals, eig_vecs = np.linalg.eig(np.eye(matrix_dim) - C)
    eig_vals_diag = np.diag(eig_vals)
    nonzero_cond = np.array(eig_vals > ZERO_BOUND)
    nonzero_eig_vals_diag = eig_vals_diag[nonzero_cond, :][:, nonzero_cond]
    nonzero_eig_vecs = eig_vecs[:, nonzero_cond]
    B = nonzero_eig_vecs.dot(np.linalg.inv(nonzero_eig_vals_diag)).dot(nonzero_eig_vecs.T)

    return B
