from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrap_data():
    from selenium.webdriver.chrome.service import Service

    download_service = Service()
    driver = webdriver.Chrome(service=download_service)
    driver.maximize_window()

    open_website(driver)
    prepare(driver)
    data = scrap(driver)
    driver.quit()
    return data

def open_website(driver):
    # Otwieranie strony Steam
    url = "https://store.steampowered.com/category/science_fiction/"
    driver.get(url)

def prepare(driver):
    time.sleep(5)
    # Zamkniecie popupu
    popup_close_button = driver.find_element(By.ID, "rejectAllButton")
    popup_close_button.click()

    menu_button = driver.find_element(By.XPATH, "//div[text()='Typ']")
    driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
    menu_button.click()

    # Wybranie kategorii Gry
    games_button = driver.find_element(By.XPATH, "//a[text()='Gry']")
    driver.execute_script("arguments[0].click();", games_button)

    time.sleep(2)

def scrap(driver):
    # zecrolluj na dół listy
    driver.execute_script('window.scroll(0, document.body.scrollHeight-2000)')
    time.sleep(2)

    # Powtarzanie procesu
    for i in range(60):
        load_more_button = driver.find_element(By.CLASS_NAME, '_2tkiJ4VfEdI9kq1agjZyNz.Focusable')
        load_more_button.click()
        driver.execute_script('window.scroll(0, document.body.scrollHeight-2000)')
        time.sleep(2)

    return GetTitlesWithDetails(driver)

def GetTitlesWithDetails(driver):
    import pandas as pd

    games_data = []
    game_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'v9uRg57bwOaPsvAnkXESO')]")

    for game in game_containers:
        try:
            # Pobranie tytułu gry
            title = game.find_element(By.XPATH, ".//div[contains(@class, '_3rrH9dPdtHVRMzAEw82AId')]//a//div").text.strip()

            # Pobranie tagów
            tags_container = game.find_element(By.XPATH, ".//div[contains(@class, '_3wryhCRrTuMULeq_YjNk-s')]")
            tag_elements = tags_container.find_elements(By.XPATH, ".//div[contains(@class, '_2bkP-3b7dvr0a_qPdZEfHY')]//a")
            tags = ', '.join([tag.text.strip() for tag in tag_elements if tag.text.strip()])

            # Pobranie ceny gry
            try:
                price_container = game.find_element(By.XPATH, ".//div[contains(@class, 'kW6m4Sjqacp5hykrj5LEo')]//div[contains(@class, '_2s-O5T3qJJYR2AUq4b9jIN')]")
                price = price_container.find_element(By.XPATH, ".//div[contains(@class, '_3j4dI1yA7cRfCvK8h406OB')]").text.strip()
            except:
                price = "Free to Play"

            # Pobranie daty wydania
            try:
                release_date = game.find_element(By.XPATH, ".//div[contains(@class, '_3wryhCRrTuMULeq_YjNk-s')]//div[contains(@class, '_3a6HRK-P6LK0-pxRKXYgyP')]//div[contains(@class, '_1qvTFgmehUzbdYM9cw0eS7')]").text.strip()
            except:
                release_date = "Brak daty"

            # Pobranie nacechowania recenzji
            try:
                review_sentiment = game.find_element(By.XPATH, ".//div[contains(@class, '_3wryhCRrTuMULeq_YjNk-s')]//a[contains(@class, '_3qvppfM_u0yn2jrpoUo8RM')]//div[contains(@class, '_3ZWs0kB-1tuqQtie9KK-E7')]//div[contains(@class, '_2nuoOi5kC2aUI12z85PneA')]").text.strip()
            except:
                review_sentiment = "Brak informacji"

            # Pobranie liczby recenzji
            try:
                review_count = game.find_element(By.XPATH, ".//div[contains(@class, '_3wryhCRrTuMULeq_YjNk-s')]//a[contains(@class, '_3qvppfM_u0yn2jrpoUo8RM')]//div[contains(@class, '_3ZWs0kB-1tuqQtie9KK-E7')]//div[contains(@class, '_1wXL_MfRpdKQ3wZiNP5lrH')]").text.strip()
            except:
                review_count = "0"

            # Dodanie gry do listy
            games_data.append({
                "Tytuł": title,
                "Tagi": tags,
                "Cena": price,
                "Data wydania": release_date,
                "Nacechowanie recenzji": review_sentiment,
                "Liczba recenzji": review_count
            })

        except Exception as e:
            print(f"Problem z przetwarzaniem gry: {e}")

    # Konwersja do DataFrame
    df = pd.DataFrame(games_data)
    return df
