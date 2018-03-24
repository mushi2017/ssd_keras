'''
Miscellaneous data generator utilities.

Copyright (C) 2018 Pierluigi Ferrari

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import division
import numpy as np

def apply_inverse_transforms(y_pred_decoded, inverse_transforms):
    '''
    Takes a list or Numpy array of decoded predictions and applies a given list of
    transforms to them. The list of inverse transforms would usually contain the
    inverter functions that some data transformations return. This function would
    normally be used to transform predictions that were made on a transformed image
    back to the original image.

    Arguments:
        y_pred_decoded (list or array): Either a list of length `batch_size` that
            contains Numpy arrays that contain the predictions for each batch item
            or a Numpy array. If this is a list of Numpy arrays, the arrays would
            usually have the shape `(num_predictions, 6)`, where `num_predictions`
            is different for each batch item. If this is a Numpy array, it would
            usually have the shape `(batch_size, num_predictions, 6)`. The last axis
            would usually contain the class ID, confidence score, and four bounding
            box coordinates for each prediction.
        inverse_predictions (list): A nested list of length `batch_size` that contains
            for each batch item a list of functions that take one argument (one element
            of `y_pred_decoded` if it is a list or one slice along the first axis of
            `y_pred_decoded` if it is an array) and return an output of the same shape
            and data type.

    Returns:
        The transformed predictions, which have the same structure as `y_pred_decoded`.
    '''

    if isinstance(y_pred_decoded, list):

        y_pred_decoded_inv = []

        for i in range(len(y_pred_decoded)):
            y_pred_decoded_inv.append(np.copy(y_pred_decoded[i]))
            for inverter in inverse_transforms[i]:
                y_pred_decoded_inv[i] = inverter(y_pred_decoded[i])

    elif isinstance(y_pred_decoded, np.ndarray):

        y_pred_decoded_inv = np.copy(y_pred_decoded)

        for i in range(len(y_pred_decoded)):
            for inverter in inverse_transforms[i]:
                y_pred_decoded_inv[i] = inverter(y_pred_decoded[i])

    else:
        raise ValueError("`y_pred_decoded` must be either a list or a Numpy array.")

    return y_pred_decoded_inv
