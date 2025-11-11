import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
sqs = boto3.client("sqs", region_name="us-east-1")

NOME_TABELA = "SolicitacoesTroca"
URL_FILA = "https://sqs.us-east-1.amazonaws.com/123456789012/fila-troca-notificacoes"

def lambda_handler(event, context):
    corpo = json.loads(event.get("body", "{}"))
    usuario_id = corpo.get("usuario_id")
    celular_atual = corpo.get("celular_atual")
    celular_desejado = corpo.get("celular_desejado")

    if not all([usuario_id, celular_atual, celular_desejado]):
        return {"statusCode": 400, "body": json.dumps({"erro": "Campos obrigatórios faltando."})}

    troca_id = str(uuid.uuid4())
    criado_em = datetime.utcnow().isoformat()

    # Grava no DynamoDB
    tabela = dynamodb.Table(NOME_TABELA)
    tabela.put_item(Item={
        "troca_id": troca_id,
        "usuario_id": usuario_id,
        "celular_atual": celular_atual,
        "celular_desejado": celular_desejado,
        "status": "PENDENTE",
        "criado_em": criado_em
    })

    # Envia mensagem para a fila SQS
    sqs.send_message(
        QueueUrl=URL_FILA,
        MessageBody=json.dumps({
            "troca_id": troca_id,
            "usuario_id": usuario_id,
            "celular_atual": celular_atual,
            "celular_desejado": celular_desejado
        })
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"mensagem": "Solicitação de troca registrada com sucesso!", "troca_id": troca_id})
    }
