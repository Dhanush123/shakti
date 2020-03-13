from joblib import dump, load
from shakti.utils.gcp.firebase import initialize_db
from shakti.utils.constants import SKLEARN


def upload_model_metadata(local_model_path, model_id, model_type):
    db = initialize_db()
    metadata = get_model_metadata(local_model_path, model_type)
    doc_ref = db.collection("models").document(model_id)
    doc_ref.set(metadata)


def get_model_metadata(local_model_path, model_type):
    metadata = {}
    if model_type == SKLEARN:
        model = load(local_model_path)
        metadata["model_library"] = SKLEARN
        metadata["library_version"] = model.__getstate__()['_sklearn_version']
        metadata["model_type"] = type(model).__name__
        metadata["hyperparameters"] = model.get_params()
    return metadata
