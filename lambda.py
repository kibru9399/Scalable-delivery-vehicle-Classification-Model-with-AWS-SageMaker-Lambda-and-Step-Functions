#THE FIRST LAMBDA FUNCTION 'serializeImageData'

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


#THE SECOND LAMBDA FUNCTION 'inferenceFunction'
import boto3
import json
import base64
# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-01-18-08-00-04-381" ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["image_data"])
    
    runtime = boto3.Session().client('sagemaker-runtime')
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image)
    
    predictions = json.loads(response['Body'].read().decode())
    # Instantiate a Predictor
   
    
    # We return the data back to the Step Function    
    event["inferences"] = predictions
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


#THE THIRD LAMBDA FUNCTION 'thresholdChecker'

import json


THRESHOLD = 0.99


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['inferences'] ## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences)>THRESHOLD ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)}
