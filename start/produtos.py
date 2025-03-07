import os
import json
import requests
from dotenv import load_dotenv

# ========== CONFIGURAÇÕES ==========
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ========== VERIFICA CREDENCIAIS ==========
if not all([DISCORD_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    print("❌ Erro: Credenciais ausentes no arquivo .env. Verifique e tente novamente.")
    exit(1)


# ========== FUNÇÃO PARA TESTAR CONEXÃO COM TELEGRAM ==========
def testar_telegram():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok", False):
                print("✅ Conexão com Telegram OK!")
                return True
            else:
                print(f"❌ Erro na resposta da API do Telegram: {data.get('description', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro ao conectar no Telegram: Código {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar no Telegram: {e}")
        return False


# ========== FUNÇÃO PARA TESTAR CONEXÃO COM DISCORD ==========
def testar_discord():
    try:
        response = requests.head(DISCORD_WEBHOOK_URL)
        
        if response.status_code in [200, 204]:
            print("✅ Conexão com Discord OK!")
            return True
        else:
            print(f"❌ Erro ao conectar no Discord: Código {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar no Discord: {e}")
        return False


# ========== FUNÇÃO PARA ENVIAR TELEGRAM ==========
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID,
              "text": mensagem, "parse_mode": "Markdown"}
    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("✅ Enviado para Telegram!")
    else:
        print("❌ Erro ao enviar para Telegram:", response.text)


# ========== FUNÇÃO PARA ENVIAR DISCORD ==========
def enviar_discord(mensagem):
    data = {"content": mensagem}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ Enviado para Discord!")
    else:
        print("❌ Erro ao enviar para Discord:", response.text)


# ========== LER PRODUTOS DO JSON ==========
def carregar_produtos():
    try:
        with open("meus_produtos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'meus_produtos.json' não foi encontrado.")
        exit(1)
    except json.JSONDecodeError:
        print("❌ Erro: O arquivo 'meus_produtos.json' está corrompido ou mal formatado.")
        exit(1)


# ========== FORMATAR MENSAGEM ==========
def formatar_mensagem(produto):
    preco = produto.get("preco")

    if preco is None:
        preco_formatado = "Preço não disponível"
    elif isinstance(preco, (int, float)):
        preco_formatado = f"R$ {preco:.2f}"
    else:
        preco_formatado = str(preco)

    return (
        "🔔 *Promoção encontrada!* \n"
        f"📍 *{produto['nome']}* \n"
        f"💰 *Preço:* {preco_formatado} \n"
        f"🏬 *Loja:* {produto['loja']} \n"
        f"🔗 [Link do Produto]({produto['url']})"
    )


# ========== ENVIAR PRODUTOS ==========
def enviar_produtos():
    produtos = carregar_produtos()

    mensagens = []

    for produto in produtos:
        mensagens.append(formatar_mensagem(produto))

    mensagem_final = "\n\n".join(mensagens)

    enviar_telegram(mensagem_final)
    enviar_discord(mensagem_final)


# ========== EXECUTAR ==========
if __name__ == "__main__":
    print("🔍 Testando conexão com Telegram e Discord...\n")

    if testar_telegram() and testar_discord():
        print("\n✅ Conexões OK! Enviando produtos...\n")
        enviar_produtos()
    else:
        print("\n❌ Erro na conexão! Verifique as credenciais antes de continuar.")
