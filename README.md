### README.md


# 📦 Price Monitoring System with Python

Este projeto é uma solução automatizada para monitoramento de preços de produtos online, envio de notificações em tempo real via Telegram e armazenamento dos dados coletados em um banco PostgreSQL. Ideal para e-commerce, análises de mercado e gestão de estoques.

---

## 🛠️ **Funcionalidades**
- **Web Scraping**: Coleta de informações de páginas da Amazon utilizando Selenium e BeautifulSoup.
- **Banco de Dados**: Armazenamento das informações em um banco PostgreSQL para consulta e análise futura.
- **Notificações**: Envio de mensagens no Telegram com detalhes sobre os preços e descontos.
- **Execução Contínua**: Verificação periódica das URLs monitoradas.

---

## 🚀 **Tecnologias Utilizadas**
- **Python** (Linguagem principal)
- **Selenium** e **BeautifulSoup** para web scraping.
- **PostgreSQL** para banco de dados.
- **SQLAlchemy** e **pandas** para manipulação e persistência de dados.
- **Telegram Bot API** para envio de notificações.
- **dotenv** para gerenciamento de variáveis de ambiente.
- **Asyncio** para operações assíncronas.

---

## 📋 **Pré-requisitos**
1. **Python 3.8+** instalado.
2. **PostgreSQL** configurado.
3. Variáveis de ambiente configuradas:
   - `TELEGRAM_TOKEN` - Token do bot Telegram.
   - `TELEGRAM_CHAT_ID` - ID do chat para envio de mensagens.
   - `POSTGRES_DB` - Nome do banco de dados.
   - `POSTGRES_USER` - Usuário do banco.
   - `POSTGRES_PASSWORD` - Senha do banco.
   - `POSTGRES_HOST` - Host do banco.
   - `POSTGRES_PORT` - Porta do banco.

---

## 🔧 **Instalação**
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/preco-monitoramento.git
   cd preco-monitoramento
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente no arquivo `.env`.

5. Configure o banco de dados PostgreSQL:
   - Certifique-se de que o PostgreSQL está em execução.
   - As credenciais devem estar no arquivo `.env`.

---

## 🚀 **Como Executar**
1. Execute o script principal:
   ```bash
   python app.py
   ```
2. O sistema iniciará a coleta de dados das URLs configuradas e enviará mensagens para o Telegram com informações de preços.

---

## 📜 **Detalhes do Código**

### 1. **Web Scraping**
- **fetch_page(url)**: Utiliza Selenium para acessar a página e capturar o HTML.
- **parse_page(html)**: Usa BeautifulSoup para extrair nome do produto, preço antigo, desconto e preço atual.

### 2. **Banco de Dados**
- **setup_database(conn)**: Cria a tabela no PostgreSQL, caso não exista.
- **save_to_database(data, table_name='prices')**: Salva os dados coletados no banco usando pandas e SQLAlchemy.

### 3. **Telegram Bot**
- **send_telegram_message(text)**: Envia mensagens para um chat específico utilizando a API do Telegram.

### 4. **Execução Contínua**
- O loop principal verifica as URLs periodicamente (atualmente a cada 10 segundos), enviando notificações e salvando os dados no banco.

---

## 📈 **Casos de Uso**
- Monitoramento de preços para promoções.
- Armazenamento histórico de preços para análises.
- Alertas automatizados para tomadas de decisão.

---

## 🛠️ **Contribuições**
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 **Licença**
Este projeto está licenciado sob a [MIT License](LICENSE).

---

👨‍💻 Desenvolvido por [Seu Nome](https://linkedin.com/in/seuusuario). Vamos conversar? 🚀
```
