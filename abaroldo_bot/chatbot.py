
import boto3
import json
import requests
from telebot import TeleBot
from config import SECRET, BUCKET, SESSION, PLACE
import dynamo as d
import report as r
import tempfile
import os

def get_bot_token():

    session = boto3.session.Session()
    client = session.client(service_name = 'secretsmanager', region_name = "us-east-1")
    request = client.get_secret_value(SecretId = SECRET)
    # TOKEN = json.loads(request['SecretString'])['TOKEN']
    TOKEN = "1702654441:AAFIGTMFT40a14w_tVOkNisD6z9O4cqTX_E"
    return TOKEN

def get_bot_client():
    
    token = get_bot_token()
    return TeleBot(token)

def message_check(event):
    
    message = json.loads(event['body'])['message']
    chat_id = message['chat']['id']
    sender = message['from']['last_name']
    
    if "photo" in message.keys():
        text = "#"
        file_id = message['photo'][-1]['file_id']
    else:
        text = message['text']
        file_id = "#"
    
    return chat_id, text, file_id, sender
    
    
def put_image_on_bucket(file_id):
    
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir)
    
    # Temp & S3 paths
    image_key = file_id + ".jpg"
    temp_image_path = "{}/{}".format(temp_path, image_key)
    s3_image_path = "s3://{}/{}".format(BUCKET, image_key)

    # Bot get file from chat and download it
    bot = get_bot_client()
    image_obj = bot.get_file(file_id)
    download_image = bot.download_file(image_obj.file_path)
    
    # Save file on temp dir
    with open(temp_image_path, 'wb') as file:
        file.write(download_image)
        
    # Save file into S3 bucket
    client = boto3.client('s3')
    client.upload_file(temp_image_path, BUCKET, image_key)
    
    return image_key


def send_visit_report(visit_id, chat_id):
    
    metric = r.create_report(visit_id)
    
    bot = get_bot_client()
    bot.send_message(chat_id, 
    "Relatorio da Abare {}. Status: {}, Pontuacao: {} ({}). Constam {} itens irregulares, {} fotos e {} observacoes".format(
            metric['location'], 
            metric['classification'], 
            metric['points'], 
            metric['percent_points'], 
            metric['item_count'], 
            metric['img_count'], 
            metric['obs_count']
    ))
    bot.send_document(chat_id, data = open(metric['path'], 'rb'))
    bot.send_document(chat_id, data = open(metric['zip_path'], 'rb'))
    

