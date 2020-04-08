from googleapiclient import discovery
from googleapiclient import errors

from shakti.utils.constants import TRAIN_ERROR, TRAIN_SUCCESS


def submit_aiplatform_train_request(job_spec, train_project_id):
    cloudml = discovery.build("ml", "v1")
    request = cloudml.projects().jobs().create(
        body=job_spec, parent=train_project_id)
    try:
        response = request.execute()
        print()
        print(response)
    except errors.HttpError as err:
        # Something went wrong, print out some information.
        print(TRAIN_ERROR)
        print(err._get_reason())
