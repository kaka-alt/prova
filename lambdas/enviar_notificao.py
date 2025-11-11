import json
import boto3

sns = boto3.client("sns", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

NOME_TABELA = "SolicitacoesTroca"

def lambda_handler(event, context):
    tabela = dynamodb.Table(NOME_TABELA)

    for registro in event["Records"]:
        corpo = json.loads(registro["body"])
        troca_id = corpo["troca_id"]
        usuario_id = corpo["usuario_id"]
        celular_atual = corpo["celular_atual"]
        celular_desejado = corpo["celular_desejado"]

        print(f"📲 Processando troca {troca_id} — {celular_atual} → {celular_desejado}")

        # Simula envio de SMS/E-mail
        sns.publish(
            PhoneNumber="+5599999999999",
            Message=f"Olá! Sua solicitação de troca ({celular_atual} por {celular_desejado}) está sendo processada."
        )

        # Atualiza status no DynamoDB
        tabela.update_item(
            Key={"troca_id": troca_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "NOTIFICADO"}
        )

        print(f"✅ Notificação enviada e status atualizado para NOTIFICADO")

    return {"statusCode": 200, "processados": len(event["Records"])}
