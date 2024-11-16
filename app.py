from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import re
import time
import pandas as pd
import asyncio
import psycopg2



load_dotenv()

# Telegram Bot Settings
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=TOKEN)

# Config database PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Creates the SQLAlchemy engine for PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

# Function to load HTML content of a web page using Selenium
def fetch_page(url):
    # Configure Selenium WebDriver for Chrome
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run the browser in headless mode (without opening a window)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Opens the specified URL in the browser
    driver.get(url)
    time.sleep(3)  # Time for page to fully load

    # Capture the HTML of the loaded page
    html = driver.page_source
    driver.quit()
    return html # return HTML as string

# Function to extract information from HTML using BeautifulSoup
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get product title from a <span> with specific id
    title_tag = soup.find("span", {"id": "productTitle"})
    title = title_tag.get_text(strip=True) if title_tag else "Título não encontrado"
    
    # Extract the discount percentage and convert it to a decimal value
    percentage_discount = soup.find(
        "span", 
        class_= "a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"
        ).get_text(strip=True)
    
    percentage_discount = float(re.sub(r"%|-","",percentage_discount)) / 100

    # Extracts the integer and fraction part of the new price and converts it to float
    price_int = soup.find(
        "span",
        class_= "a-price-whole"
    ).get_text(strip=True)

    price_frac = soup.find(
        "span",
        class_= "a-price-fraction"
    ).get_text(strip=True)

    new_price = float((price_int + price_frac).replace(",","."))
    
    # Extracts the original price of the product and converts it to float
    price = soup.find(
        "span",
        class_= "a-size-small aok-offscreen"
    ).get_text(strip=True)
    
    price = float(re.sub(r"De:|R\$|\s", "", price).replace(",", "."))

    # Get the time and transform it to the time string
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Returns a dictionary with the collected information
    return {
        'product_name': title,
        'old_price': price,
        'discount': percentage_discount,
        'new_price': new_price,
        'timestamp': timestamp
    }

# Function to connect to the database
def create_connection():
    
    # Create connection to PostgreSQL
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return conn

# Function to configure the database
def setup_database(conn):

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            old_price FLOAT,
            discount FLOAT,
            new_price FLOAT,
            timestamp TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()

# Function to save products info in database
def save_to_database(data, table_name='prices'):
    df = pd.DataFrame([data])
    df.to_sql(table_name, engine,if_exists='append', index=False)


async def send_telegram_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

# Main code to process a list of URLs
async def main():
    # Config database
    conn = create_connection()
    setup_database(conn)

    urls = [
        "https://www.amazon.com.br/gp/product/8537815128/ref=ox_sc_act_title_2?smid=A1ZZFT5FULY4LN&psc=1",
        "https://www.amazon.com.br/gp/product/8550804681/ref=ox_sc_act_title_1?smid=A3LDLKNBXD1VOA&psc=1",
        "https://www.amazon.com.br/Data-Science-para-neg%C3%B3cios-Fawcett/dp/8576089726/?_encoding=UTF8&pd_rd_w=gvwhu&content-id=amzn1.sym.09916995-565b-4f2a-a31f-48091c48a79c%3Aamzn1.symc.5111b5a7-85f4-4b0c-88b2-c0a74bb618a6&pf_rd_p=09916995-565b-4f2a-a31f-48091c48a79c&pf_rd_r=S7TGWKM01S3AF1VWZNNY&pd_rd_wg=oMbc9&pd_rd_r=772eadc7-6be9-47f3-b848-c0ab5272c421&ref_=pd_hp_d_btf_ci_mcx_mr_hp_atf_m"
    ]
    try:

        while True:

            for url in urls:
                
                # Makes the request and parses the page
                page_content = fetch_page(url)
                product_info = parse_page(page_content)

                message = (
                    f"Atualização do preço do produto '{product_info['product_name']}'\n"
                    f"Preço atual: R${product_info['new_price']:.2f}\n"
                    f"Desconto: {product_info['discount']*100:.0f}%"
                )
                # Send a message in telegram
                await send_telegram_message(message)
                # Save the product information
                save_to_database(product_info)

            # Wait 10 seconds to perform the next execution
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("Stopping execution")
    finally:
        # Close connection with database
        conn.close()

asyncio.run(main())