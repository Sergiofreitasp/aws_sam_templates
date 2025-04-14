import json
import boto3 # Importando a biblioteca boto3 para trabalhar com os serviços da AWS
import os # Para recuperar variáveis de ambiente


rekognition_client = boto3.client("rekognition") # Instanciando o cliente do Rekognition
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    
    # captura do evento de PUT do amazon S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    print(event)
    print(bucket_name)
    print(file_name)
   
    #chamada do evento para dectçao de labels do rekognition
    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket':bucket_name, 'Name': file_name }},
        MaxLabels=10,
        MinConfidence=80
    )

    #lista de labels detectados
    labels = [label['Name'] for label in response['Labels']]

    print(labels)
    
    sqs_client.send_message(
        QueueUrl=os.environ['SQS_URL'],
        MessageBody=json.dumps({
            'bucket': bucket_name,
            'key': file_name,
            'labels': labels
        })
    )
    

    
