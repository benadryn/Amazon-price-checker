import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib

load_dotenv("H:/Python/.env")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

url = "https://www.amazon.com.au/Apple-iPhone-Pro-Max-256/dp/B09V3HGK9V/ref=sr_1_10?keywords=iphone%2B13%2Bpro%2Bmax&" \
      "qid=1651822112&sprefix=iph%2Caps%2C285&sr=8-10&th=1"
response = requests.get(url)
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
price = float(soup.find(class_="a-price-whole").getText().replace(",", "") + soup.find(class_="a-price-fraction").getText())
title = soup.find(id="productTitle").getText().strip()
preferred_price = 20000
if price < preferred_price:
    message = f"{title} is now ${int(price)}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n {title} fell below your preferred price!\n{url}"
        )