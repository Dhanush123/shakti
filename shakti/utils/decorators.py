import os
import re
from functools import wraps
from flask import request
from werkzeug.utils import secure_filename

from shakti.utils.gcp.firebase import initialize_db
from shakti.utils.gcp.googlebucket import gcs_file_upload
from shakti.utils.constants import MODELS, REQUESTBODY, TEMP_FLASK_SAVE_DIR, MODEL_RESPONSE_TYPE, TEXT, IMAGE, RESPONSE

from shakti.utils.utilities import get_date_for_id, get_env_creds


def log_request(func):
    @wraps(func)
    def logger(*args, **kwargs):
        # TODO: uncomment this code and test once can publish pip package and add package to Dockerfile
        # db = initialize_db()
        # request_body, request_files = str(
        #     request.get_json(force=True)), request.files

        # model_id = re.findall(
        #     r"[^,]+-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}", request.host)[0]
        # doc_ref = db.collection(MODELS).document(
        #     model_id).collection(REQUESTBODY)
        # date = get_date_for_id()

        # doc_ref.update({date: request_body})

        # for file_name, file_data in request_files:
        #     file_name = secure_filename(file_name.filename)
        #     temp_path = "{}/{}".format(TEMP_FLASK_SAVE_DIR, file_name)
        #     file_data.save(temp_path)
        #     bucket_path = "{}/{}".format(MODELS, model_id)
        #     gcs_file_upload(bucket_path, temp_path)

        return func(*args, **kwargs)
    return logger


def log_response(func):
    @wraps(func)
    def logger(response):
        # TODO: uncomment this code and test once can publish pip package and add package to Dockerfile
        # get_env_creds()
        # db = initialize_db()
        # model_id = re.findall(
        #     r"[^,]+-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}", request.host)[0]

        # model_response_type = os.environ.get(MODEL_RESPONSE_TYPE, TEXT)

        # if model_response_type == TEXT:
        #     doc_ref = db.collection(MODELS).document(
        #         model_id).collection(REQUESTBODY)
        #     date = get_date_for_id()
        #     doc_ref.update({date: response})
        # elif model_response_type == IMAGE:
        #     temp_response = [response] if not isinstance(
        #         response[RESPONSE], list) else response
        #     for count, image in enumerate(temp_response[RESPONSE]):
        #         temp_path = "{}/{}".format(TEMP_FLASK_SAVE_DIR, str(count+1))
        #         image.save(temp_path)
        #         bucket_path = "{}/{}".format(MODELS, model_id)
        #         gcs_file_upload(bucket_path, temp_path)

        return func(response)
    return logger
