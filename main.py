# -*- coding: utf-8 -*-
# filename          : main.py
# description       : 
# author            : Ian Ault
# email             : ianault2022@isd282.org
# date              : 02-14-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
from selenium import webdriver
import os
import time
import datetime
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
	def __init__(self):
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument(f"user-data-dir={user_data_dir}")
		options.add_argument("--disable-gpu")
		# options.add_argument("log-level=3")
		self.executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
		self.driver = webdriver.Chrome(executable_path=os.path.abspath(self.executable), options=options)
		print("Init finished")
		#time.sleep(10)

	def wait_until_element(self, stratagy, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		element = wait.until(
			EC.presence_of_element_located(
				(
					stratagy, locator
				)
			)
		)
		return element

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def run(self):
		print("Opening URL")
		# current_day = datetime.date.today()[:2]
		self.open_link("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61a7b36a534a139d668b4568")
		print(self.wait_until_element(By.XPATH, "//*[@class=\"sc-ifAKCX fsjfiH notranslate\"]/span").text)


if __name__ == "__main__":
	scraper = Scraper()
	scraper.run()
