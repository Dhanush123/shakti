import os
from joblib import dump, load
import shutil

from tensorflow import keras

from shakti.utils.gcp.firebase import initialize_db
from shakti.utils.constants import SKLEARN, TF, MODELS
from shakti.utils.utilities import get_filename_noext
from shakti.utils.tf import convert_keras_to_tf


def upload_model_metadata(local_model_path, model_id, model_type):
    db = initialize_db()
    metadata = get_model_metadata(local_model_path, model_type)
    doc_ref = db.collection(MODELS).document(model_id)
    doc_ref.set(metadata)


def get_model_metadata(local_model_path, model_type):
    metadata = {}
    if model_type == SKLEARN:
        model = load(local_model_path)
        metadata["model_library"] = SKLEARN
        metadata["library_version"] = model.__getstate__()['_sklearn_version']
        metadata["model_type"] = type(model).__name__
        metadata["hyperparameters"] = model.get_params()
    elif model_type == TF:
        model = keras.models.load_model(local_model_path)
        metadata["model_library"] = TF
        # need to stringify b/c Firestore current doesn't support storing tuples which are used for layer shapes
        metadata["config"] = str(model.get_config())
        if local_model_path.find("h5"):
            convert_keras_to_tf(model, local_model_path)
    return metadata
