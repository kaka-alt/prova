# 📱 Aplicativo de Troca de Celulares

## 💡 Descrição
Este projeto simula um sistema de trocas de celulares utilizando uma arquitetura totalmente serverless baseada na AWS.  
Quando um usuário solicita uma troca, o sistema grava a requisição no banco de dados, envia uma mensagem para uma fila e notifica o proprietário do celular via SMS

## 🏗️ Arquitetura
1. **API Gateway** recebe a solicitação HTTP do aplicativo.
2. **Lambda 1 (`criar_solicitacao_troca_lambda`)** valida os dados, grava a solicitação no **DynamoDB** e envia uma mensagem à **fila SQS**.
3. **SQS (`fila-troca-notificacoes`)** armazena as mensagens até que sejam processadas.
4. **Lambda 2 (`enviar_notificacao_lambda`)** é acionada automaticamente pela fila e:
   - Envia notificações via **Amazon SNS** (simulação de SMS/e-mail);
   - Atualiza o status da solicitação no **DynamoDB**.

### 🔹 Serviços AWS Utilizados
- **Amazon API Gateway** — ponto de entrada da aplicação  
- **AWS Lambda** — funções que processam os eventos  
- **Amazon SQS** — fila de mensagens para processamento assíncrono  
- **Amazon SNS** — envio de SMS/e-mail  
- **Amazon DynamoDB** — banco de dados para armazenar solicitações


## 🚀 Objetivo
Demonstrar uma arquitetura moderna, escalável e assíncrona de trocas de celulares com persistência e notificações automáticas.
