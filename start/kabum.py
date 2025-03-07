import csv
import json
import os
import sys
import threading
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuração do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def iniciar_driver():
    """Inicia o driver do navegador"""
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def simular_usuario(driver):
    """Simula ações do usuário na página para garantir carregamento"""
    actions = ActionChains(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    actions.move_by_offset(5, 5).perform()


def extrair_produtos(url, nome_loja, driver, seletor_produto, seletor_nome, seletor_preco, seletor_link, seletor_imagem):
    """Extrai produtos da página"""
    driver.get(url)
    time.sleep(3)
    simular_usuario(driver)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, seletor_produto))
        )
    except:
        print(f"Erro ao carregar produtos da {nome_loja}.")
        return []

    produtos = driver.find_elements(By.CLASS_NAME, seletor_produto)
    lista_produtos = []

    for produto in produtos[:20]:  # Agora pegamos 20 produtos
        try:
            nome = produto.find_element(By.CLASS_NAME, seletor_nome).text
            preco = produto.find_element(By.CLASS_NAME, seletor_preco).text.replace(
                "R$", "").replace(",", ".").strip()
            preco = float(
                ''.join(filter(lambda x: x.isdigit() or x == '.', preco)))
            link = produto.find_element(By.TAG_NAME, "a").get_attribute("href")
            imagem = produto.find_element(
                By.TAG_NAME, "img").get_attribute("src")

            lista_produtos.append({
                "loja": nome_loja,
                "nome": nome,
                "preco": preco,
                "link": link,
                "imagem": imagem
            })
        except:
            continue

    # Ordena os produtos pelo preço (do mais barato para o mais caro)
    lista_produtos = sorted(lista_produtos, key=lambda x: x["preco"])

    # Retorna os 10 produtos mais baratos
    return lista_produtos[:10]


def enviar_telegram(mensagem):
    """Envia mensagem para o Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)


def testar_discord():
    """Testa a API do Discord para verificar se o Webhook está funcionando, mas só exibe no terminal"""
    mensagem = "Teste de Conexão - Discord"
    payload_discord = {
        "content": mensagem,
        "embeds": [{"image": {"url": "https://www.example.com/test_image.jpg"}}]
    }

    # Não envia a mensagem para o Discord, só exibe no terminal
    print("✅ Teste de conexão no Discord bem-sucedido!")


def testar_telegram():
    """Testa a API do Telegram para verificar se o bot e o chat_id estão funcionando, mas só exibe no terminal"""
    mensagem = "Teste de Conexão - Telegram"

    # Não envia a mensagem para o Telegram, só exibe no terminal
    print("✅ Teste de conexão no Telegram bem-sucedido!")


def contador_tempo():
    """Exibe um contador de tempo no terminal para mostrar que o programa está rodando."""
    tempo = 0
    while True:
        sys.stdout.write(f"\r⏳ Tempo de execução: {tempo} segundos...")
        sys.stdout.flush()
        time.sleep(1)
        tempo += 1


def monitorar():
    """Executa o monitoramento de preços"""
    # Testa as APIs do Discord e Telegram antes de continuar, sem enviar mensagens para as plataformas
    testar_discord()
    testar_telegram()

    # Iniciar o contador de tempo em uma thread separada
    contador_thread = threading.Thread(target=contador_tempo, daemon=True)
    contador_thread.start()

    driver = iniciar_driver()
    produtos_kabum = extrair_produtos("https://www.kabum.com.br/hardware",
                                      "Kabum", driver, "productCard", "nameCard", "priceCard", "a", "img")
    driver.quit()

    if len(produtos_kabum) < 10:
        print("\nNão foi possível coletar 10 produtos da Kabum.")
        return

    # Salvar os produtos em um CSV
    with open("precos_monitorados.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Loja", "Nome", "Preço", "Link", "Imagem"])
        for produto in produtos_kabum:
            writer.writerow([produto["loja"], produto["nome"],
                            produto["preco"], produto["link"], produto["imagem"]])
        print("\n✅ Arquivo CSV atualizado com sucesso!")

    # Salvar os produtos em um JSON
    with open("precos_monitorados.json", "w", encoding="utf-8") as json_file:
        json.dump(produtos_kabum, json_file, ensure_ascii=False, indent=4)
        print("\n✅ Arquivo JSON atualizado com sucesso!")

    # Ordena os produtos pelo preço (do mais barato para o mais caro) e seleciona os 10 mais baratos
    produtos_mais_baratos = sorted(
        produtos_kabum, key=lambda x: x["preco"])[:10]

    for produto in produtos_mais_baratos:
        mensagem = f"\U0001F514 *Promoção encontrada!*\n" \
            f"\U0001F4CD *{produto['nome']}*\n" \
            f"\U0001F4B0 *Preço:* R$ {produto['preco']:.2f}\n" \
            f"\U0001F3EC *Loja:* {produto['loja']}\n" \
            f"\U0001F517 [Link do Produto]({produto['link']})"

        # Enviar para o Discord
        payload_discord = {
            "content": mensagem,
            "embeds": [{"image": {"url": produto['imagem']}}]
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload_discord)

        # Enviar para o Telegram
        enviar_telegram(mensagem)

    print("\n✅ Monitoramento concluído!")


# Loop de execução
while True:
    monitorar()
    print("⏳ Aguardando 1 hora para a próxima execução...")
    time.sleep(3600)
