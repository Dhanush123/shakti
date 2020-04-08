import os

from shakti.utils.constants import PROJECT_ID, GCP_REGION, GCS_BUCKET_NAME, GCP_DATAPROC_CLUSTER, DATAPROC, GCP_DEFAULT_REGION, OUTPUT_PATH_ARG, DATA
from shakti.utils.utilities import get_env_creds
from shakti.utils.gcp.dataproc import set_cluster_clients, submit_dataproc_pyspark_job, add_outputpath_to_job
from shakti.utils.gcp.googlebucket import gcs_file_upload


def submit_pyspark_job(spark_job_path, **kwargs):
    get_env_creds()
    project_id = kwargs.get(PROJECT_ID, os.environ[PROJECT_ID])
    region = kwargs.get(GCP_REGION, os.environ.get(
        GCP_REGION, GCP_DEFAULT_REGION))
    cluster_name = kwargs.get(GCP_DATAPROC_CLUSTER,
                              os.environ[GCP_DATAPROC_CLUSTER])
    bucket_name = kwargs.get(GCS_BUCKET_NAME, os.environ[GCS_BUCKET_NAME])

    _, dataproc_job_client = set_cluster_clients()

    spark_bucket_output_path = kwargs.get(
        OUTPUT_PATH_ARG, "gs://{}/{}".format(bucket_name, DATA))

    mod_job_path = add_outputpath_to_job(
        spark_job_path, spark_bucket_output_path)
    gcs_file_upload(bucket_name, DATAPROC, mod_job_path)

    submit_dataproc_pyspark_job(dataproc_job_client, mod_job_path,
                                spark_bucket_output_path, project_id, region, cluster_name, bucket_name)

    os.remove(mod_job_path)
