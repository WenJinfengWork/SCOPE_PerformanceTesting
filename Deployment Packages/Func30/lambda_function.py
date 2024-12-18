import boto3
import pandas as pd
from time import time
import re

s3 = boto3.client('s3')

cleanup_re = re.compile('[^a-z]+')


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def lambda_handler(event, context):
    bucket = event['input_bucket']
    key = event['key']
    # path = bucket + "/" + key
    # df = pd.read_csv('s3://' + path)

    model_path_data = '/tmp/' + key
    s3.download_file(bucket, key, model_path_data)
    df = pd.read_csv(model_path_data)

    start = time()
    df['Text'] = df['Text'].apply(cleanup)
    text = df['Text'].tolist()
    result = set()
    for item in text:
        result.update(item.split())
    print("Number of Feature : " + str(len(result)))

    feature = str(list(result))
    feature = feature.lstrip('[').rstrip(']').replace(' ', '')
    latency = time() - start
    print(latency)

    write_key = event['key'].split('.')[0] + ".txt"
    s3.put_object(Body=feature, Bucket=bucket, Key=write_key)
    return latency

# event1={"input_bucket":"bucketwendycyn","key":"reviews20mb.csv"}
# print(lambda_handler(event1,""))
# urllib3, six, jmespath, python-dateutil, botocore, s3transfer, boto3
