import os
import shutil

from shakti.utils.utilities import get_filename_noext
from shakti.utils.constants import TF_SERVING_FOLDER


def convert_keras_to_tf(model, local_model_path):
    # need convert h5 -> SavedModel for TF Serving
    h5_folder = os.path.dirname(local_model_path)
    tf_folder = os.path.join(h5_folder,
                             "1")
    model.save(tf_folder, save_format="tf", overwrite=True)
    parent_tf_folder = os.path.join(h5_folder, TF_SERVING_FOLDER)
    if os.path.exists(parent_tf_folder):
        shutil.rmtree(parent_tf_folder)
    os.mkdir(parent_tf_folder)
    shutil.move(tf_folder, parent_tf_folder)
