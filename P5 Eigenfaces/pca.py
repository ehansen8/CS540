'''
Evan Hansen
CS 540
P5: Eigenfaces
'''

import scipy.io
import scipy.linalg
import numpy as np
import matplotlib.pyplot as plt


# Load the dataset from a provided .mat file,
# re-center it around the origin
# and return it as a NumPy array of floats
def load_and_center_dataset(filename):
    dataset = scipy.io.loadmat(filename)
    x = dataset['fea']
    x = x.astype(float)
    x = x - np.mean(x, axis=0)
    n = len(x)
    d = len(x[0])

    return x


# Calculate and return the covariance matrix
# of the dataset as a NumPy matrix (d x d array)
def get_covariance(dataset):
    n = len(x)
    covariance = (1 / (n - 1)) * np.dot(np.transpose(dataset), dataset)

    return covariance


# Perform eigen decomposition on the covariance matrix S
# and return a diagonal matrix (NumPy array) with the
# largest m eigenvalues on the diagonal, and a matrix (NumPy array)
# with the corresponding eigenvectors as columns
def get_eig(S, m):
    n = len(S)
    w, v = scipy.linalg.eigh(S, eigvals=(n - m, n - 1))
    v = v[:, ::-1]
    w = np.diag(w[::-1])

    return w, v


# Project each image into your m-dimensional space and
# return the new representation as a d x 1 NumPy array
def project_image(image, U):
    alpha = image @ U
    x_hat = alpha @ U.T
    return x_hat


# Use matplotlib to display a visual representation of the
# original image and the projected image side-by-side
def display_image(orig, proj):
    orig_32 = np.reshape(orig, (32, 32))
    proj_32 = np.reshape(proj, (32, 32))

    fig, (ax1, ax2) = plt.subplots(1, 2)
    bar1 = ax1.imshow(orig_32.T, aspect='equal')
    ax1.set_title("Original")

    bar2 = ax2.imshow(proj_32.T, aspect='equal')
    ax2.set_title("Projection")

    fig.colorbar(bar1, ax=ax1, fraction=.047, pad=.05)
    fig.colorbar(bar2, ax=ax2, fraction=.047, pad=.058)
    plt.show()
