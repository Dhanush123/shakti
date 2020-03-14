# shakti
## ML Deployment Platform

- The goal is to learn ML infrastructure development as well as be able to use this platform in ML side projects and hackathon projects under the constraint of a free tier on a cloud provider (in my case GCP)

[Planning resources and features roadmap](https://docs.google.com/document/d/1jN7PwvJvloXU3pV7AS4srayAnrhhSK6Zs2NMTsFPe8E/edit?usp=sharing)

- The platform currently makes use of Google Cloud Storage Bucket (like S3), Cloud Firestore (NoSQL DB), Cloud Build (container builder), and Cloud Run (serverless containers).
To setup the shakti library in this repo:
 1) In the root folder of the repo run ```pipenv install```. Ideally you should be using pyenv along with pipenv like I did to install various Python versions. While developing the library, I used 3.8.1.
 2) You can now install the library locally with ```pip install -e .``` in the root folder.
- Usage Examples:
 - ```shakti upload ~/Downloads/mnist_model.joblib```
 - ```shakti list models```
 - ```shakti deploy models/mnist_model.joblib```
 - An example of client-usage is in the [shakti-client](https://github.com/Dhanush123/shakti-client) repo
 
Other
- The upload cmd path refers to a relative path in the bucket
- When deploy cmd is run, metadata is uploaded to firestore
- Utilities logic use to be a separate repo/pip package called [shakti-utils](https://github.com/Dhanush123/shakti-utils) but has been now merged into here (its commits before 3/8) won't show in this repo)
