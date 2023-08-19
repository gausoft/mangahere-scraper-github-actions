from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from scraper_helper import ScraperHelper

import csv
import random
import os


def main():
    logger = ScraperHelper.initialize_logger()
    driver = ScraperHelper.setupDriver()

    data_directory = os.path.join(os.getcwd(), 'data')
    # Create the "data" directory if it doesn't exist
    os.makedirs(data_directory, exist_ok=True)

    csv_file_path = os.path.join(data_directory, 'manga_database.csv')
    resume_file_path = os.path.join(data_directory, 'resume.txt')

    csv_header = ['Title', 'Subtitle', 'Rating', 'Link', 'Image']

    lastpage = ScraperHelper.resume_index(resume_file_path)
    current_page = lastpage + 1

    scraped_page = 0
    target_page = 2 # random.choice([4, 10, 15, 20])  # Choose a random minimum number of elements to retrieve
    print(f'We wanna scrape {target_page} pages')

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if current_page == 1:
            logger.info(f"First time creating : {csv_file_path} file")
            writer.writerow(csv_header)

        while scraped_page < target_page:
            url = f'https://www.mangahere.cc/directory/{current_page}.htm?az'
            driver.get(url)

            try:
                elements = driver.find_elements(By.CLASS_NAME, 'manga-list-1-list > li')
                logger.info(f'{len(elements)} found on page : {current_page}')
                if len(elements) == 0:
                    break
                for element in elements:
                    title = element.find_element(By.CSS_SELECTOR, '.manga-list-1-item-title > a').get_attribute('title')
                    subtitle = element.find_element(By.CSS_SELECTOR, '.manga-list-1-item-subtitle > a').text
                    link = element.find_element(By.CSS_SELECTOR, '.manga-list-1-item-title > a').get_attribute('href')
                    img_src = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    rating = element.find_element(By.CSS_SELECTOR, '.item-score').text

                    writer.writerow([title, subtitle, rating, link, img_src])

                current_page += 1
                scraped_page += 1
                ScraperHelper.save_resume_index(resume_file_path, current_page)
                logger.info(f"Scraped: {url}")

                if scraped_page >= target_page:
                    break
            except NoSuchElementException:
                logger.error("The element does not exist.")

    driver.quit()

if __name__ == "__main__":
    main()
