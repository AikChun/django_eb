from django.shortcuts import render
from django.http import JsonResponse
from todo_app.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt

import boto3
import time
import json
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def dashboard(request):
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


def download_file_from_s_three(request):

    token = request.POST['Token']
    topic_arn = request.POST['TopicArn']
    logger.error(token)

    return JsonResponse({'token': token, 'TopicArn': topic_arn})
