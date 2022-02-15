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

	def run(self):
		print("Opening URL")
		self.driver.get("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61a7b36a534a139d668b4568")


if __name__ == "__main__":
	scraper = Scraper()
	scraper.run()
