
import boto3
import json
from datetime import datetime, timedelta
from config import DYNAMO_DB

def new_visit_check_int(text):

    visit_date = datetime.strftime(datetime.now() - timedelta(hours = 3), '%d/%m/%Y')
    visit_hour = datetime.strftime(datetime.now() - timedelta(hours = 3), '%H:00')
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    response = dynamo_db.put_item(
        Item = {
            "visit_id": "Sede {}, {} {}".format(text, visit_date, visit_hour),
            "location": text, 
            "visit_date": visit_date,
            "visit_hour": visit_hour,
            "irregular": [], 
            "png_file": [], 
            "bullets": [],
            "reported": "false"
        })

def ensure_unique_check_in():
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    try:
        for item in dynamo_db.scan()['Items']:
            if item['reported'] == "true":
                pass
            else:
                dynamo_db.delete_item(Key = {"visit_id": item['visit_id']})
    except:
        pass
    
def put_item_on_checklist(item_checked):

    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        
        if item['reported'] == 'false':
            key = item["visit_id"]
        
            if item_checked not in item['irregular']:
                irregular_item = item["irregular"]
                irregular_item.append(item_checked)
                dynamo_db.update_item(
                    Key = {'visit_id': key},
                    UpdateExpression = "SET irregular= :var1",
                    ExpressionAttributeValues = {':var1': irregular_item}
                )
                return True
            else:
                return False
            
def list_items_checked():
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            found = item['irregular']
            if len(found) == 0:
                found.append("Nao encontrei nenhum item marcado ainda..")
            return found
        
    return ["Nao encontrei nenhum item marcado ainda.."]

def list_obs_checked():
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            found = item['bullets']
            if len(found) == 0:
                found.append("Nenhuma observacao anotada pra esta visita ainda")
            return found
        
    return ["Nenhuma observacao anotada pra esta visita ainda"]
    
    
def check_in_exists():
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        try:
            if item['reported'] == 'false':
                return True
        except:
            pass

    return False

def check_out_visit():

    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            dynamo_db.update_item(
                Key = {'visit_id': item["visit_id"]},
                UpdateExpression = "SET reported= :var1",
                ExpressionAttributeValues = {':var1': 'true'}
            )
            return "Boa! Registrei Check-Out pra {}. Agora voce ja pode solicitar um relatorio dessa visita".format(
                item["visit_id"])

    return "Nossa que estranho, fui fazer o Check-Out mas nao achei nenhum Check-In aberto de visitas.."


def list_items_to_remove():
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            return item['irregular']
    return []


def remove_item_from_checklist(remove_item):
    
    remove_item = remove_item[remove_item.find(" ") + 1:]
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            key = item["visit_id"]
            current_list = item['irregular']
            update_list = []
            
            for item in current_list:
                if item != remove_item:
                    update_list.append(item)

            dynamo_db.update_item(
                Key = {'visit_id': key},
                UpdateExpression = "SET irregular= :var1",
                ExpressionAttributeValues = {':var1': update_list}
            )

def register_obs(obs):

    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            current_obs = item["bullets"]
            current_obs.append(obs.replace("/obs", "").strip())
            
            dynamo_db.update_item(
                Key = {'visit_id': item["visit_id"]},
                UpdateExpression = "SET bullets= :var1",
                ExpressionAttributeValues = {':var1': current_obs}
            )
            
def register_image_key(image_key):

    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'false':
            
            current_png = item["png_file"]
            current_png.append(image_key)
            
            dynamo_db.update_item(
                Key = {'visit_id': item["visit_id"]},
                UpdateExpression = "SET png_file= :var1",
                ExpressionAttributeValues = {':var1': current_png}
            )
            
def get_report_key(visit_id):
    
    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    key = dynamo_db.get_item(Key = {"visit_id": visit_id})
    item = key['Item']
    
    return item

def list_checked_out_visits():

    dynamo_db = boto3.resource("dynamodb").Table(DYNAMO_DB)
    check_out = []
    for item in dynamo_db.scan()['Items']:
        if item['reported'] == 'true':
            check_out.append(item['visit_id'])
        
    return check_out


