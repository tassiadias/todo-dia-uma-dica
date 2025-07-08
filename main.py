import os
import random
from twilio.rest import Client

# Carrega variáveis de ambiente
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM") 
DESTINATION_NUMBER = os.getenv("DESTINATION_NUMBER")      

# Lê dicas e histórico
with open("dicas.txt", "r", encoding="utf-8") as f:
    todas_dicas = [linha.strip() for linha in f if linha.strip()]

try:
    with open("enviadas.txt", "r", encoding="utf-8") as f:
        dicas_enviadas = set(linha.strip() for linha in f)
except FileNotFoundError:
    dicas_enviadas = set()

# Seleciona dica não enviada
dicas_disponiveis = list(set(todas_dicas) - dicas_enviadas)

if not dicas_disponiveis:
    dicas_enviadas.clear()
    dicas_disponiveis = todas_dicas

dica_escolhida = random.choice(dicas_disponiveis)

# Envia mensagem via Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
    from_="whatsapp:" + os.getenv("TWILIO_WHATSAPP_FROM"),
    to="whatsapp:" + os.getenv("DESTINATION_NUMBER"),
    body=f"📊 Dica do dia:\n{dica_escolhida}"
)

print(f"Mensagem enviada com SID: {message.sid}")

# Registra dica como enviada
with open("enviadas.txt", "a", encoding="utf-8") as f:
    f.write(dica_escolhida + "\n")
