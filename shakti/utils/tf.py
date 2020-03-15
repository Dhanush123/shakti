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
    # rename tf file to be same as keras file
    os.rename(os.path.join(tf_folder, "saved_model.pb"), os.path.join(
        tf_folder, "{}.pb".format(get_filename_noext(local_model_path))))

    parent_tf_folder = os.path.join(h5_folder, TF_SERVING_FOLDER)
    if os.path.exists(parent_tf_folder):
        shutil.rmtree(parent_tf_folder)
    os.mkdir(parent_tf_folder)
    shutil.move(tf_folder, parent_tf_folder)

    # # change folder name to be version name
    # version_folder = os.path.join(h5_folder, "1")
    # os.rename(tf_folder, version_folder)
    # # move version folder under folder to use in tf serving

    # os.mkdir(os.path.join(h5_folder, "tf_model"))
    # shutil.move(tf_folder,)
    # # remove h5 file
    # os.remove(local_model_path)

    # # move TF pb file to cur dir
    # tf_file = "saved_model.pb"
    # shutil.copy(os.path.join(tf_folder, tf_file), h5_folder)
    # # give TF file same name as original Keras file
    # os.rename(os.path.join(h5_folder, tf_file), os.path.join(
    #     h5_folder, get_filename_noext(local_model_path))+".pb")
    # # remove temp tf folder + Keras file
    # shutil.rmtree(tf_folder)
    # os.remove(local_model_path)
