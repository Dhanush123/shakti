import os

from shakti.utils.gcp.aiplatform import submit_aiplatform_train_request
from shakti.utils.utilities import get_train_dir, run_bash_cmd, file_from_path, get_date_for_id, arg_dict_to_list
from shakti.utils.constants import CPU, GPU, TRAIN_ERROR, TRAIN, MODELS, TRAIN_ARGS, TRAIN_INPUTS, GCP_REGION, GCP_DEFAULT_REGION, OUTPUT_PATH_ARG, GCS_BUCKET_NAME, PROJECT_ID, TF


def train(model_name, model_type=TF, hardware_type=GPU, **kwargs):
    train_dir = get_train_dir()

    train_args = ["--stream-logs"]
    if kwargs[TRAIN_ARGS]:
        train_args.extend(arg_dict_to_list(kwargs[TRAIN_ARGS]))

    region = kwargs.get(GCP_REGION, os.environ.get(
        GCP_REGION, GCP_DEFAULT_REGION))
    bucket_name = kwargs.get(GCS_BUCKET_NAME, os.environ[GCS_BUCKET_NAME])

    # currently this cmd only support TF GPU
    # TODO: move some config code to another file if support more model/hardware combos
    train_inputs = {
        "scaleTier": "standard_gpu",
        "pythonModule": "{}.{}".format(file_from_path(train_dir), TRAIN),
        "args": ["--stream-logs"],
        "region": region,
        "jobDir": kwargs.get(OUTPUT_PATH_ARG, "gs://{}/{}".format(bucket_name, MODELS)),
        "scheduling": {"maxRunningTime": "7200s"}
    }
    if kwargs[TRAIN_INPUTS]:
        for key, value in kwargs[TRAIN_INPUTS].items():
            train_inputs[key] = value

    job_spec = {
        "jobId": "{}-{}".format(model_name, get_date_for_id()), "trainingInput": train_inputs}

    train_project_id = 'projects/{}'.format(
        kwargs.get(PROJECT_ID, os.environ[PROJECT_ID]))

    submit_aiplatform_train_request(job_spec, train_project_id)
