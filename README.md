# shakti
## ML Deployment Platform

- The goal is to learn ML infrastructure development as well as be able to use this platform in ML side projects and hackathon projects in a public cloud (currently only GCP) at little to no cost (by utilizing free tier services where possible).

[Planning resources and features roadmap](https://docs.google.com/document/d/1jN7PwvJvloXU3pV7AS4srayAnrhhSK6Zs2NMTsFPe8E/edit?usp=sharing)

- The platform currently makes use of Google Cloud Storage Bucket (like S3), Cloud Firestore (NoSQL DB), Cloud Build (container builder), Cloud Run (serverless containers), Flask, and TensorFlow Serving.
To setup the shakti library in this repo:
 1) In the root folder of the repo run ```pipenv install```. Ideally you should be using pyenv along with pipenv like I did to install various Python versions. While developing the library, I used 3.7.
 2) You can now install the library locally with ```pip install -e .``` in the root folder.
 3) You also need to have a GCP account, download the [SDK/CLI](https://cloud.google.com/sdk/docs) and set an active service account and project. 
 4) Manually create a GCS Bucket (covered in always free tier), Firestore instance (covered in always free tier), and Dataproc cluster (uses trial credits, create/delete as necessary).
- Usage Examples:
 - ```shakti upload ~/Downloads/mnist_model.joblib```
 - ```shakti upload ~/Downloads/data.csv```
 - ```shakti list models```
 - ```shakti list data```
 - ```shakti deploy sklearn models/mnist_model.joblib```
 - ```shakti deploy tf models/kerastest.h5```
 - ```shakti process testspark.py```
 - ```shakti train test-modelfolder```
 
 - An example of client-usage is in the [shakti-client](https://github.com/Dhanush123/shakti-client) repo. I use that repo to test the functionality of this one.
 
Other
- Currently supports deploying scikit-learn and TensorFlow models (including Keras by converting h5 to pb).
- The upload cmd path refers to a relative path in the bucket
- When deploy cmd is run, metadata is uploaded to Firestore
- Model and dataset uploads are saved in the bucket as is Spark job outputs
- The train cmd only supports TF on GPU currently
- In progress: A deployed model (currently only sklearn, TF too in the future) will log its predictions to Firestore. This can't be tested yet until the pip package has been published.
- Utilities logic use to be a separate repo/pip package called [shakti-utils](https://github.com/Dhanush123/shakti-utils) but has been now merged into here (its commits before 3/8) won't show in this repo)
