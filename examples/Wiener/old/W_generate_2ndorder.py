import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import pandas as pd
import os
import h5py


#a = [1.0, 0.3, -0.3]
#b = [0.0, -0.3, 0.3]
#c = []

a = [1, 0.6, -0.6]
b = [1, -0.6, 0.6]

c1= -0.3
c2 = 0.5

var_w = 1.0
var_u = 1.0
var_e = 0.1

save_dataset = False

def static_nl(y_lin):
    y_nl = np.clip(y_lin, c1, c2)
    return y_nl


if __name__ == '__main__':

    n_real = 50
    N = 1000
    add_noise = True # add process noise
    output_filename = 'dataset_2o.h5'
    dataset_name = 'train_nonoise'

    # In[]
    var_w = add_noise*var_w

    std_w = np.sqrt(var_w)
    std_e = np.sqrt(var_e)
    std_u = np.sqrt(var_u)
    # In[Wiener with noise model]
    u = std_u*np.random.randn(n_real, N)
    x0 = scipy.signal.lfilter(b, a, u, axis=-1)
    w = std_w*np.random.randn(n_real, N)
    x = x0 + w
    y0 = static_nl(x)
    e = std_e*np.random.randn(n_real, N)
    y = y0+e


    # In[Plot]
    plt.figure()
    plt.plot(y[0, :], 'r', label='y')
    plt.plot(y0[0, :], 'g', label='y0')
    plt.legend()

    plt.figure()
    plt.plot(x[0, :], 'g', label='x')
    plt.plot(x0[0, :], 'r', label='x0')
    plt.legend()

    # In[Save]
    if save_dataset:
        if not (os.path.exists('../data')):
            os.makedirs('data')
        filename = os.path.join('data', output_filename)
        hf = h5py.File(filename, 'a')
        ds_signal = hf.create_group(dataset_name)  # signal group
        ds_signal.create_dataset('u', data=u[..., None])
        ds_signal.create_dataset('x0', data=x0[..., None])
        ds_signal.create_dataset('w', data=w[..., None])
        ds_signal.create_dataset('y0', data=y0[..., None])
        ds_signal.create_dataset('y', data=y[..., None])
        hf.close()


