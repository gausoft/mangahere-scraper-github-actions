from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging
import logging.handlers
import os

class ScraperHelper:

    @staticmethod
    def setupDriver():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("lang=en")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        return driver

    @staticmethod
    def initialize_logger():
        filename = os.path.join(os.getcwd(), 'status.log')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger_file_handler = logging.handlers.RotatingFileHandler(
            filename,
            maxBytes=1024 * 1024,
            backupCount=1,
            encoding="utf8",
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger_file_handler.setFormatter(formatter)
        logger.addHandler(logger_file_handler)
        return logger

    @staticmethod
    def resume_index(resume_file_path):
        index = 0
        if os.path.exists(resume_file_path):
            with open(resume_file_path, "r") as resume_file:
                index = int(resume_file.read().strip())
        return index

    @staticmethod
    def save_resume_index(resume_file_path, index):
        with open(resume_file_path, "w") as resume_file:
            resume_file.write(str(index))
