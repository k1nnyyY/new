import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка драйвера для подключения к удалённому Selenium-контейнеру


def setup_driver():
    # URL сервиса Selenium в Docker Compose
    selenium_url = "http://selenium:4444/wd/hub"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Запуск без интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options
    )
    # Подключаемся к frontend по имени сервиса
    driver.get("http://frontend_app:3000")
    return driver

# Функция для симуляции человеческого ввода


def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.2)

# Функция для заполнения формы


def fill_form(driver):
    # Открываем файл с данными
    with open("data.txt", "r") as file:
        data = {}
        for line in file:
            key, value = line.strip().split('=')
            data[key] = value

    # Вводим данные в поля формы
    mos_field = driver.find_element(By.NAME, "mos")
    human_typing(mos_field, data['mos'])

    inpol_field = driver.find_element(By.NAME, "inpol")
    human_typing(inpol_field, data['inpol'])

    first_name_field = driver.find_element(By.NAME, "first_name")
    human_typing(first_name_field, data['first_name'])

    last_name_field = driver.find_element(By.NAME, "last_name")
    human_typing(last_name_field, data['last_name'])

    passport_code_field = driver.find_element(By.NAME, "passport_code")
    human_typing(passport_code_field, data['passport_code'])

    country_field = driver.find_element(By.NAME, "country")
    human_typing(country_field, data['country'])

    email_field = driver.find_element(By.NAME, "email")
    human_typing(email_field, data['email'])

    # Выбор радио-кнопки
    radio_button = driver.find_element(
        By.XPATH, f"//input[@type='radio' and @value='{data['radio_choice']}']")
    radio_button.click()

    # Ввод даты рождения
    date_field = driver.find_element(By.NAME, "date_of_birth")
    date_field.send_keys(data['date_of_birth'])

    # Ввод имени и фамилии опекуна
    guardian_field = driver.find_element(By.NAME, "guardian_name")
    human_typing(guardian_field, data['guardian_name'])

    # Прохождение капчи вручную
    print("Пройди капчу вручную, затем нажми Enter...")
    input()

    # Нажатие кнопки отправки
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

# Основная функция для запуска скрипта


def main():
    driver = setup_driver()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mos")))
    fill_form(driver)
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
