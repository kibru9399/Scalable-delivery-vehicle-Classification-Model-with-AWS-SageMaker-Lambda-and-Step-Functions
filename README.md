
# Scalable and Safe Image Classification Model with AWS SageMaker, Lambda, and Step Functions

As an MLE, the  goal is to ship a scalable and safe model. Once the model becomes available to other teams on-demand, it’s important that it can scale to meet demand, and that safeguards are in place to monitor and control for drift or degraded performance.
In this project, I used AWS Sagemaker to build an image classification model that can tell bicycles apart from motorcycles. l deployed the model, and used AWS Lambda functions to build supporting services, and AWS Step Functions to compose the model and services into an event-driven application.
#### Project Steps Overview
#### Step 1: Data staging
Extract the data from a hosting service
Transform it into a usable shape and format
Load it into a production system (loading it into s3)
In other words, we're going to do some simple ETL!
#### Step 2: Model training and deployment
We configure Model Monitor to track our deployment. We'll define a DataCaptureConfig object.  At the end of the project, we can explore the data_capture directory in S3 to find crucial data about the inputs and outputs Model Monitor has observed on our model endpoint over time.
With that done, deploy your model on a single ml.m5.xlarge instance with the DataCaptureConfig  attached.
####  Step 3: Lambdas and step function workflow
The operations team can use Step Functions to orchestrate serverless workflows. One of the nice things about Step Functions is that workflows can call other workflows, so the team can easily plug our workflow into the broader production architecture for Scones.In this next stage, I wrote and deployed three Lambda functions and then used the Step Functions visual editor to chain them together. 

The first Lambda function will copy an object from S3, base64 encode it, and then return it to the step function as image_data in an event.

The next function is responsible for the classification part - we're going to take the image output from the previous function, decode it, and then pass inferences back to the the Step Function.

Finally, we need to filter out low-confidence inferences. We define a threshold between 1.00 and 0.000; if  the model predicts at.70 and above for it's highest confidence label, we would want to pass that inference to the downstream system.

With the lambdas in place, we can use the Step Functions visual editor to construct a workflow that chains them together. In the Step Functions console, there is an option to author a Standard step function Visually.
####  Step 4: Testing and evaluation
 several step function invocations using data from the ./test folder. This process gives confidence that the workflow both succeeds AND fails as expected. In addition, SageMaker Model Monitor will generate recordings of our data and inferences, which we can visualize.

