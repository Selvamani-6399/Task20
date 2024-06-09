import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# Helper function to download files


class LabourGOV:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.url = "https://labour.gov.in/"
        self.wait = WebDriverWait(self.driver, 10)

    def download_file(self, url, folder, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename}")

    def main(self):

        self.driver.get(self.url)
        self.driver.maximize_window()
        self.get_monthly_report()
        self.get_media_images()
        # Close the driver
        self.driver.quit()

    def get_monthly_report(self):
        # Navigate to "Documents" and download the Monthly Progress Report
        documents_menu = self.driver.find_element(
            By.XPATH, '//*[@id="nav"]/li[8]/a')
        actions = ActionChains(self.driver)
        actions.move_to_element(documents_menu).perform()
        time.sleep(2)
        monthly_documents_menu = self.driver.find_element(
            By.XPATH, '//*[@id="nav"]/li[7]/ul/li[2]/a')
        monthly_documents_menu.click()
        time.sleep(2)
        monthly_progress_report_link = self.driver.find_element(
            By.XPATH, '//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/a')
        monthly_progress_report_url = monthly_progress_report_link.get_attribute(
            'href')
        self.download_file(monthly_progress_report_url, '.',
                           'Monthly_Progress_Report.pdf')

    def get_media_images(self):
        # Navigate to "Media" > "Photo Gallery"
        media_menu = self.driver.find_element(
            By.XPATH, '//*[@id="nav"]/li[10]/a')
        media_menu.click()
        self.driver.find_element(
            By.XPATH, '//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/p/b/a').click()
        photo_gallery_link = self.driver.find_element(
            By.LINK_TEXT, "Photo Gallery")
        photo_gallery_link.click()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[1])

        # Create a folder to save the photos
        os.makedirs('Photo_Gallery', exist_ok=True)
        photo_container = self.driver.find_element(
            By.XPATH, '//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div[2]/table/tbody')
        # Download the first 10 photos

        photos = photo_container.find_elements(
            By.TAG_NAME, "img")
        for i, photo in enumerate(photos[:10]):
            photo_url = photo.get_attribute('src')
            self.download_file(photo_url, 'Photo_Gallery', f'photo_{i+1}.jpg')


if __name__ == "__main__":
    test = LabourGOV()
    test.main()