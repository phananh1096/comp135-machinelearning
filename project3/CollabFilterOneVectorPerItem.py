# Make sure you use the autograd version of numpy (which we named 'ag_np')
# to do all the loss calculations, since automatic gradients are needed
import autograd.numpy as ag_np

# Use helper packages
from AbstractBaseCollabFilterSGD import AbstractBaseCollabFilterSGD
from utils import load_dataset

# Some packages you might need (uncomment as necessary)
## import pandas as pd
## import matplotlib

# No other imports specific to ML (e.g. scikit) needed!

class CollabFilterOneVectorPerItem(AbstractBaseCollabFilterSGD):
    ''' One-vector-per-user, one-vector-per-item recommendation model.

    Assumes each user, each item has learned vector of size `n_factors`.

    Attributes required in param_dict
    ---------------------------------
    mu : 1D array of size (1,)
    b_per_user : 1D array, size n_users
    c_per_item : 1D array, size n_items
    U : 2D array, size n_users x n_factors
    V : 2D array, size n_items x n_factors

    Notes
    -----
    Inherits *__init__** constructor from AbstractBaseCollabFilterSGD.
    Inherits *fit* method from AbstractBaseCollabFilterSGD.
    '''

    def init_parameter_dict(self, n_users, n_items, train_tuple):
        ''' Initialize parameter dictionary attribute for this instance.

        Post Condition
        --------------
        Updates the following attributes of this instance:
        * param_dict : dict
            Keys are string names of parameters
            Values are *numpy arrays* of parameter values
        '''
        # TODO fix the lines below to have right dimensionality & values
        # TIP: use self.n_factors to access number of hidden dimensions
        random_state = self.random_state # inherited
        self.param_dict = dict(
            mu=ag_np.ones(1),
            b_per_user=ag_np.ones(n_users),
            c_per_item=ag_np.ones(n_items),
            U=random_state.randn(n_users,self.n_factors),
            V=random_state.randn(n_items,self.n_factors),
            )

    def predict(self, user_id_N, item_id_N,
                mu=None, b_per_user=None, c_per_item=None, U=None, V=None):
        ''' Predict ratings at specific user_id, item_id pairs

        Args
        ----
        user_id_N : 1D array, size n_examples
            Specific user_id values to use to make predictions
        item_id_N : 1D array, size n_examples
            Specific item_id values to use to make predictions
            Each entry is paired with the corresponding entry of user_id_N

        Returns
        -------
        yhat_N : 1D array, size n_examples
            Scalar predicted ratings, one per provided example.
            Entry n is for the n-th pair of user_id, item_id values provided.
        '''
        # TODO: Update with actual prediction logic
        N = user_id_N.size
        yhat_N = ag_np.full(N,mu) + b_per_user[user_id_N] + c_per_item[item_id_N] + ag_np.einsum('ij,ij->i',U[user_id_N],V[item_id_N])
        return yhat_N


    def calc_loss_wrt_parameter_dict(self, param_dict, data_tuple):
        ''' Compute loss at given parameters

        Args
        ----
        param_dict : dict
            Keys are string names of parameters
            Values are *numpy arrays* of parameter values

        Returns
        -------
        loss : float scalar
        '''
        # TODO compute loss
        # TIP: use self.alpha to access regularization strength
        y_N = data_tuple[2]
        yhat_N = self.predict(data_tuple[0], data_tuple[1], **param_dict)
        loss_grad = ag_np.sum(ag_np.square(y_N - yhat_N))
        penalty = self.alpha * (ag_np.einsum('ij->',ag_np.square(param_dict['U'])) + ag_np.einsum('ij->',ag_np.square(param_dict['V'])))
        loss_total = penalty + loss_grad
        return loss_total    

if __name__ == '__main__':
    train_tuple, valid_tuple, test_tuple, n_users, n_items = load_dataset()
    model = CollabFilterOneVectorPerItem(
        n_factors=2, alpha=0.00,
        n_epochs=50, step_size=0.5)
    model.init_parameter_dict(n_users, n_items, train_tuple)
    model.fit(train_tuple, valid_tuple)

