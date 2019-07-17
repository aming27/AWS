import boto3
from urllib.parse import unquote
import botocore
import shutil
import time
import boto.sqs
import subprocess
import requests
import os
import datetime
import uuid
import json
import base64
import logging
import platform 



def get_messages_from_queue(environments):
    sqs = boto3.client('sqs')
    
    for env in environments:
        queue_url = 'your-aws-queue-' + env
        number_of_messages = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])    
        number_of_messages = number_of_messages['Attributes']
        number_of_messages = number_of_messages['ApproximateNumberOfMessages']
        #print ('Number of messages in ' + env + ', queue = ' + number_of_messages)
    
        if number_of_messages == '0':            
            time.sleep(2)
        else:         
            
            response = sqs.receive_message(QueueUrl=queue_url, AttributeNames=['All'], MaxNumberOfMessages=1, MessageAttributeNames=['All'], VisibilityTimeout=0, WaitTimeSeconds=0)           
           
            print ('Response lenth = ' + str(len(response)))
            if len(response) != 2:                
                
            else:
                entries = [
                    {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                    for msg in response['Messages']
                ]
           
                resp = sqs.delete_message_batch(
                    QueueUrl=queue_url, Entries=entries
                )

                if len(resp['Successful']) != len(entries):
                    raise RuntimeError(
                        f"Failed to delete messages: entries={entries!r} resp={resp!r}"
                    )                  
                  
                
                return response

def main():    
    
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s : %(levelname)s : %(message)s',
                filename = 'listener.log',
                filemode = 'a',)
    
    all_env = { 'production', 'testing' }
    
    logging.info("Listener:")      
    
    while True:
        for message in get_queue_attributes(all_env):
            print(message)
        
    
    
if __name__ == '__main__':
    main()


