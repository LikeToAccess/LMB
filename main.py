# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Find Lunch!?
# author            : Ian Ault
# email             : ianault2022@isd282.org
# date              : 02-14-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import os
import time
import datetime
from selenium import webdriver
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

	def wait_until_elements(self, stratagy, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		elements = wait.until(
			EC.presence_of_all_elements_located(
				(
					stratagy, locator
				)
			)
		)
		return elements

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def run(self, url):
		
		print("Opening URL")
		# current_day = datetime.date.today()[:2]
		self.open_link(url)
		month = self.wait_until_elements(By.XPATH, "//*[@class=\"sc-iwsKbI cpOFXO currentmonth\"]")

		lunch = {}
		# foods = {}
		for day in month:
			day_information = day.text.replace("\nzoom_in", "").split("\n")
			lunch_items = day_information[2:]

			lunch[day_information[0]] = {
				"lunch_items": lunch_items,
				"day":         day_information[1],
			}

			# for count, lunch_item in enumerate(lunch_items):
			# 	foods[lunch_item] = day.find_element(By.XPATH, "//a[@class=\"menuItem\"]")
			# 	# print(foods[lunch_item].text)
			# 	print(lunch_item)
			# print("")

		# print(lunch)
		print(lunch[datetime.datetime.now().strftime("%d")])

		# print(lunch)
		# print(list(foods.keys()))
		# foods["Sweet Potato Waffle Fries"].click()




if __name__ == "__main__":
	scraper = Scraper()
	scraper.run("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b234ee534a13863843e4b9&menuType=610aacdb534a1367458b4683&siteCode=20001&showAllNutrients=false")
	scraper.run("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b23594534a132c7b43e4cf&menuType=6102de69534a13557755dde1&siteCode=20001&showAllNutrients=false")
	scraper.run("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b236bd534a13200843e4ae&menuType=6102de5b534a13a26355ddef&siteCode=20001&showAllNutrients=false")
	scraper.run("https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b2340e534a132a3c43e4b7&menuType=6102dd39534a13477155de0b&siteCode=20001&showAllNutrients=false")
	scraper.close()
