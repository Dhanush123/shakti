import os

from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.gapic.transports import (
    cluster_controller_grpc_transport)
from google.cloud.dataproc_v1.gapic.transports import (
    job_controller_grpc_transport)

from shakti.utils.constants import GCP_REGION, DATAPROC, SPARK_BUCKET_OUTPUT_PATH
from shakti.utils.utilities import file_from_path

dataproc_cluster_client = None
dataproc_job_client = None


def get_region_from_zone(zone):
    try:
        region_as_list = zone.split("-")[:-1]
        return "-".join(region_as_list)
    except (AttributeError, IndexError, ValueError):
        raise ValueError("Invalid zone provided, please check your input.")


def set_cluster_clients():
    global dataproc_cluster_client, dataproc_job_client

    if not dataproc_cluster_client or not dataproc_job_client:
        region = os.environ[GCP_REGION]
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        client_transport = (
            cluster_controller_grpc_transport.ClusterControllerGrpcTransport(
                address="{}-dataproc.googleapis.com:443".format(region)))
        job_transport = (
            job_controller_grpc_transport.JobControllerGrpcTransport(
                address="{}-dataproc.googleapis.com:443".format(region)))
        dataproc_cluster_client = dataproc_v1.ClusterControllerClient(
            client_transport)
        dataproc_job_client = dataproc_v1.JobControllerClient(job_transport)
    return dataproc_cluster_client, dataproc_job_client


def submit_dataproc_pyspark_job(dataproc_job_client, spark_job_path, spark_bucket_output_path, project_id, region, cluster_name, bucket_name):
    job_details = {
        "placement": {
            "cluster_name": cluster_name
        },
        "pyspark_job": {
            "main_python_file_uri": "gs://{}/{}/{}".format(bucket_name, DATAPROC, file_from_path(spark_job_path))
        }
    }

    result = dataproc_job_client.submit_job(
        project_id=project_id, region=region, job=job_details)
    job_id = result.reference.job_id

    print("Submitted job ID {} to the Dataproc Spark Cluster {}.".format(
        job_id, cluster_name))


def add_outputpath_to_job(spark_job_path, spark_bucket_output_path):
    mod_job_path = "{}/final-{}".format(os.getcwd(),
                                        file_from_path(spark_job_path))

    with open(spark_job_path, "r") as original_file, open(mod_job_path, "w") as modified_file:
        line = original_file.read()
        if SPARK_BUCKET_OUTPUT_PATH in line:
            line = line.replace(SPARK_BUCKET_OUTPUT_PATH,
                                '"{}"'.format(spark_bucket_output_path))
        modified_file.write(line)

    return mod_job_path
