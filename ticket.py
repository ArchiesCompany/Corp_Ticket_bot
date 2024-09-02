import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import telebot

# Ваш Telegram токен
TOKEN = 
bot = telebot.TeleBot(TOKEN)

# ID группы в Telegram
CHAT_ID = '-4593159857'

# URL страницы
URL = 

# Настройка логирования
logging.basicConfig(filename='bot_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Настройки для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def get_status_value(driver):
    try:
        # Ожидание появления элемента с классом и data-testid
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="ECQQS F5_KS emotion-htny5q ezakuv35" and @data-testid="scalar-value"]'))
        )
        value_element = driver.find_element(By.XPATH, '//h1[@class="ECQQS F5_KS emotion-htny5q ezakuv35" and @data-testid="scalar-value"]')
        return int(value_element.text.strip())
    except Exception as e:
        logging.error(f"Ошибка при извлечении значения: {e}")
        return None

def check_status():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(URL)
        time.sleep(10)  # Ждем, пока страница полностью загрузится

        current_value = get_status_value(driver)
        if current_value is not None:
            logging.info(f"Текущие открытые тикеты: {current_value}")

            if current_value >= 1:
                message = f"Открытых тикетов: {current_value}"
                bot.send_message(CHAT_ID, message)
                logging.info(f"Сообщение отправлено: {message}")

        driver.quit()

    except Exception as e:
        logging.error(f"Ошибка при проверке страницы: {e}")

if __name__ == '__main__':
    previous_value = None
    while True:
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get(URL)
            time.sleep(10)  # Ждем, пока страница полностью загрузится

            current_value = get_status_value(driver)
            if current_value is not None:
                if current_value != previous_value:
                    logging.info(f"Изменение значения: {previous_value} -> {current_value}")
                    if current_value >= 1:
                        message = f"Открытых тикетов: {current_value}"
                        bot.send_message(CHAT_ID, message)
                        logging.info(f"Сообщение отправлено: {message}")
                    previous_value = current_value
            driver.quit()

        except Exception as e:
            logging.error(f"Ошибка при проверке страницы: {e}")

        time.sleep(300)  # Ждём 5 минут
