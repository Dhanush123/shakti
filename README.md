# shakti
## ML Deployment Platform
### The goal is to learn ML infrastructure development as well as be able to use this platform in ML side projects and hackathon projects under the constraint of a free tier on a cloud provider (in my case GCP)

[Planning resources and features roadmap](https://docs.google.com/document/d/1jN7PwvJvloXU3pV7AS4srayAnrhhSK6Zs2NMTsFPe8E/edit?usp=sharing)

- The platform currently makes use of Google Cloud Storage Bucket (like S3), Cloud Build (container builder), and Cloud Run (serverless containers).
- You can install the library in this repo locally with ```pip install -e .``` in the root folder.
- Usage Examples:
 - ```shakti upload ~/Downloads/mnist_model.joblib```
 - ```shakti list models```
 - ```shakti deploy models/mnist_model.joblib```
 - An example of client-usage is in the[shakti-client repo](https://github.com/Dhanush123/shakti-client)
 
### Other
- Utilities logic use to be a separate repo/pip package called [shakti-utils](https://github.com/Dhanush123/shakti-utils) but has been now merged into here (its commits before 3/8) won't show in this repo)
