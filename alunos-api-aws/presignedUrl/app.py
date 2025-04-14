import json
import boto3 # Importando a biblioteca boto3 para trabalhar com os serviços da AWS
import os # Para recuperar variáveis de ambiente
import uuid # Para gerar um identificador único

s3_client = boto3.client('s3') # Criando um cliente para o serviço S3

def lambda_handler(event, context):
    
    # FileName (nome do arquivo) que será enviado para o S3

    # Content-type  (tipo do arquivo) que será enviado para o S3

   

    # https://y3qyccqdtj.execute-api.us-east-2.amazonaws.com/Prod/hello?fileName=arquivo.txt&contentType=text/plain

    query_params = event.get("queryStringParameters", {}) # -> ?fileName=arquivo.txt&contentType=text/plain
    file_name = query_params.get("fileName")
    content_type = query_params.get("contentType")

    expiration_time = 3600 # Tempo de expiração do link gerado em segundos

    # Import da váriavel de ambiente do nome do bucket

    bucket_name = os.environ.get("BUCKET_NAME")

    # Gerando um identificador único para o arquivo

   

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": file_name,
            "ContentType": content_type
        },
        ExpiresIn=expiration_time

    )

    return {

        "statusCode": 200,
        "body": json.dumps({
            "message": "Url pré assinada criada com sucesso",
            "url": presigned_url,
            "expiration_time": expiration_time,
            "file_name": file_name,
            "content_type": content_type
        }),

    }
