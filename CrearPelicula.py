import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido en la API de peliculas",
                "evento": event
            }
        }))
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Pelicula guardada exitosamente en DynamoDB",
                "pelicula": pelicula,
                "dynamodb_response": {
                    "HttpStatusCode": response.get('ResponseMetadata', {}).get('HTTPStatusCode')
                }
            }
        }))
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
        
    except Exception as e:
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "error_tipo": type(e).__name__,
                "error_mensaje": str(e),
                "evento_origen": event
            }
        }))
        
        return {
            'statusCode': 500,
            'error': type(e).__name__,
            'message': f"Error interno al procesar la solicitud: {str(e)}"
        }
