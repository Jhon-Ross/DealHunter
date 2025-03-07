# **DealHunter**

O **DealHunter** é um bot que acessa o site da **Kabum** e filtra as melhores ofertas de produtos, enviando os resultados diretamente para o **Discord** e o **Telegram** de forma formatada e fácil de visualizar. Esse projeto visa facilitar a busca por promoções de tecnologia, como PCs, componentes de hardware e outros produtos eletrônicos.

## **Funcionalidades:**

- **Filtragem de ofertas:** O bot acessa o site da Kabum e filtra os melhores valores para produtos selecionados.
- **Envio para Discord e Telegram:** As ofertas são enviadas automaticamente para canais do Discord e grupos ou chats do Telegram, com a formatação adequada para facilitar a leitura.
- **Versão futura para WhatsApp:** Em uma futura atualização, o bot também enviará as ofertas para o WhatsApp, permitindo que você acompanhe as promoções diretamente no seu celular.
- **Dois modos de operação:**
  - **Modo Kabum:** Envia apenas os produtos da Kabum.
  - **Modo Customizado:** Permite que o usuário adicione manualmente produtos de vários sites e envie as ofertas filtradas.

---

## **Como Usar**

### **1. Instalação**

Clone o repositório:

```bash
git clone https://github.com/Jhon-Ross/DealHunter.git
```

**Entre na pasta do projeto:**
```bash
cd DealHunter
```

### **2. Dependências**
Instale as dependências necessárias com o seguinte comando:
```bash
pip install -r requirements.txt
```

### **3. Configuração**
Antes de rodar o bot, você precisa configurar os tokens do Discord e Telegram. Siga os passos abaixo para obter os tokens:

### Discord:
1. Crie um bot no <a href="https://discord.com/developers/docs/intro">Discord Developer Portal.</a>
2. Copie o Token do bot.

### Telegram:
1. Encontre o BotFather no Telegram.
2. Crie um bot e obtenha o Token.

Adicione esses tokens no arquivo de variavel de ambiente <a href="#">.env</a>

### 4. Execução
Para rodar o bot, utilize o comando abaixo, dependendo do modo que você deseja usar:

**Para o modo Kabum:**
```bash
python start/kabum.py
```

Para o modo Customizado (onde você pode adicionar produtos manualmente):
```bash
python start/produtos.py
```

### Como Funciona?
O bot utiliza web scraping para acessar o site da Kabum, filtrar os melhores preços de produtos selecionados e enviar as ofertas diretamente para o Discord e o Telegram. Além disso, você pode configurar um arquivo JSON com uma lista de produtos de vários sites para o bot buscar automaticamente as melhores ofertas.

# Estrutura do Projeto
```bash
DealHunter/
│
├── start/                   # Scripts para iniciar o bot
│   ├── kabum.py             # Envia produtos da Kabum para Discord e Telegram
│   └── produtos.py          # Envia produtos selecionados de vários sites
│
├── config.json              # Arquivo de configuração com tokens e parâmetros
├── requirements.txt         # Dependências do projeto
├── .gitignore               # Arquivos a serem ignorados pelo Git
├── README.md                # Este arquivo
└── precos_monitorados.json  # Armazena as ofertas encontradas
```
### Como Contribuir
Se você quiser contribuir para o projeto, siga as etapas abaixo:

1. **Fork** o repositório.

2. Crie uma nova branch:
```bash
git checkout -b minha-nova-feature
```
3. Faça as alterações desejadas e commit:
```bash
git commit -am 'Adiciona nova funcionalidade'
```
4. **Push** para a branch:
```bash
git push origin minha-nova-feature
```
5. Abra um **Pull Request** explicando suas alterações.

## **Licença**
Este projeto está licenciado sob a Licença Livre para Estudos (Non-Commercial, Study-Only License) - veja o arquivo <a href="#">LICENSE</a> para mais detalhes.