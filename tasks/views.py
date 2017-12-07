from django.shortcuts import render
from django.http import JsonResponse
from todo_app.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt

import urllib.request
import boto3
import time
import json
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def dashboard(request):
    print('dashboard')
    return render(request, "dashboard.html")


def upload_file(request):

    # Create an S3 client
    s3 = boto3.client('s3')

    filename = "file.txt"
    path_to_file = '{0}/{1}'.format(BASE_DIR, filename)
    bucket_name = 'last-hearth'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(path_to_file, bucket_name, "{0}.{1}".format(filename, str(time.time())))
    return render(request, "upload-file.html")


@csrf_exempt
def download_file_from_s_three(request):
    body_data = json.loads(request.body.decode('utf-8'))
    snsType = body_data.get('Type', '')

    if snsType == 'Notification':
        s_three = boto3.client('s3')

        message_string = body_data.get('Message', {})
        message = json.loads(message_string)
        records = message.get('Records', {})
        s = records[0].get('s3', {})
        bucket = s.get('bucket', {})
        bucket_name = bucket['name']
        obj = s.get('object', {})
        key_name = obj.get('key', {})

        response = s_three.get_object(
            Bucket=bucket_name,
            Key=key_name
        )

        stream_data = response['Body'].read()
        filename = key_name.split('/')[-1]

        with open(filename, 'wb') as f:
            f.write(stream_data)
            f.close()

    if snsType == 'SubscriptionConfirmation':
        subscription_response = ""
        with urllib.request.urlopen(body_data['SubscribeURL']) as response:
            subscription_response = response.read()

    return JsonResponse({}, status=400)
