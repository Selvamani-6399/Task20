from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class Cowin:
    def __init__(self):
        # Initialize the driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def main(self):
        self.driver.get("https://www.cowin.gov.in/")
        self.driver.maximize_window()

        # Open "Create FAQ" and "Partners" in new tabs
        faq_link = self.driver.find_element(
            By.XPATH, '//*[@id="navbar"]/div[4]/div/div[1]/div/nav/div[3]/div/ul/li[4]/a')
        partners_link = self.driver.find_element(
            By.XPATH, '//*[@id="navbar"]/div[4]/div/div[1]/div/nav/div[3]/div/ul/li[5]/a')

        # Open links in new windows
        faq_link.send_keys(Keys.CONTROL + Keys.RETURN)
        partners_link.send_keys(Keys.CONTROL + Keys.RETURN)

        # Switch to new windows and get their handles
        windows = self.driver.window_handles
        print("Window handles:", windows)

        # Close the new windows
        for window in windows[1:]:
            self.driver.switch_to.window(window)
            sleep(1)
            print("Current URL :", self.driver.current_url)
            self.driver.close()

        # Switch back to the main window
        self.driver.switch_to.window(windows[0])

        # Verify we're back on the main page
        print("Current URL after closing windows:", self.driver.current_url)

        # Close the driver
        self.driver.quit()


if __name__ == "__main__":
    test = Cowin()
    test.main()