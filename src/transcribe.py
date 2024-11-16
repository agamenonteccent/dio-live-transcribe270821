import boto3
import uuid
import json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::transcribe-output-bucket/*"
    }
  ]
}

  "s3_input_uri": "s3://transcribe-input-bucket/audiofile.mp3",
  "s3_output_bucket": "transcribe-output-bucket"

def lambda_handler(event, context):
    transcribe = boto3.client('transcribe')
    job_name = "TranscribeJobExample"
    job_uri = event['s3_input_uri']
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=event['s3_output_bucket']
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job started!')
    }

    record = event['Records'][0] # arquivo enviado pelo trigger após o upload no S3
    
    s3bucket = record['s3']['bucket']['name'] # bucket de entrada que dispara o trigger
    s3object = record['s3']['object']['key'] # arquivo para ser processado
    
    s3Path = "s3://" + s3bucket + "/" + s3object # caminho para localizar o arquivo dentro do bucket de entrada
    jobName = s3object + '-' + str(uuid.uuid4()) # cria novo nome único para o job

    client = boto3.client('transcribe') # instancia um cliente python do Transcribe

    # parâmetros para iniciar um job de transcrição
    response = client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='pt-BR', # código do idioma
        MediaFormat='mp4', # formato do arquivo
        Media={
            'MediaFileUri': s3Path 
        },
        OutputBucketName = "<seu_bucket_de_saida>" # bucket de saída para receber o arquivo JSON com a transacrição
    )


    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName'] # resposta do job executado
    }
