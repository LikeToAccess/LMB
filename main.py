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
import datetime
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


links = [
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b234ee534a13863843e4b9&\
menuType=610aacdb534a1367458b4683&siteCode=20001&showAllNutrients=false",  # Grab N Go
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b23594534a132c7b43e4cf&\
menuType=6102de69534a13557755dde1&siteCode=20001&showAllNutrients=false",  # Grill Line
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b236bd534a13200843e4ae&\
menuType=6102de5b534a13a26355ddef&siteCode=20001&showAllNutrients=false",  # Hot Sandwich Line
	"https://www.schoolnutritionandfitness.com/webmenus2/#/view-no-design?id=61b2340e534a132a3c43e4b7&\
menuType=6102dd39534a13477155de0b&siteCode=20001&showAllNutrients=false",  # Daily Dish
]

days_of_the_week = {
	"MON": "Monday",
	"TUE": "Tuesday",
	"WED": "Wednesday",
	"THU": "Thursday",
	"FRI": "Friday",
	"SAT": "Saturday",
	"SUN": "Sunday",
}


def read_file(filename, encoding="utf8"):
	with open(filename, "r", encoding=encoding) as file:
		lines = file.read().split("\n")

	return lines

def write_file(filename, data, encoding="utf8"):
	with open(filename, "w", encoding=encoding) as file:
		file.write(data)


class Scraper:
	def __init__(self):
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument(f"user-data-dir={user_data_dir}")
		options.add_argument("--disable-gpu")
		# options.add_argument("log-level=3")
		# self.executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		print("Init finished")
		#time.sleep(10)

	def wait_until_element(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		element = wait.until(
			EC.presence_of_element_located(
				(
					selector, locator
				)
			)
		)
		return element

	def wait_until_elements(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		elements = wait.until(
			EC.presence_of_all_elements_located(
				(
					selector, locator
				)
			)
		)
		return elements

	def find_element(self, selector, sequence):
		return self.driver.find_element(selector, sequence)

	def find_elements(self, selector, sequence):
		return self.driver.find_elements(selector, sequence)

	def wait_until_element_by_xpath(self, sequence):
		return self.wait_until_element(By.XPATH, sequence)

	def wait_until_elements_by_xpath(self, sequence):
		return self.wait_until_elements(By.XPATH, sequence)

	def find_element_by_xpath(self, sequence):
		return self.find_element(By.XPATH, sequence)

	def find_elements_by_xpath(self, sequence):
		return self.find_elements(By.XPATH, sequence)

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def get_lunch(self, url):
		self.open_link(url)

		month = self.wait_until_elements(
			By.XPATH,
			'//*[@class="sc-iwsKbI cpOFXO currentmonth"]')
		menu = self.wait_until_element_by_xpath(
			'//*[@id="ng-view"]/react-app/div[1]/div/div[2]/div[2]/span').text

		lunch = {}
		for day in month:
			day_information = day.text.replace("\nzoom_in", "").split("\n")
			extranious_characters = "}{"
			lunch_items = []
			for data in enumerate(day_information[2:]):
				_, lunch_item = data
				lunch_items.append(
					lunch_item.translate(
						{ord(i): None for i in extranious_characters}
					).replace(
						"w/", " with "
					)
				)
			day_information[1] = days_of_the_week[day_information[1]]

			lunch[day_information[0]] = {
				"lunch_items": lunch_items,
				"day":         day_information[1],
				"menu_type":   menu
			}

		return lunch, menu

	def run(self):
		print("Opening URL")
		full_month_lunch_schedule = {}
		for link in links:
			lunch, menu_type = self.get_lunch(link)
			# print(str(lunch).replace("': {", "':\n{"))
			full_month_lunch_schedule[menu_type] = lunch
			# print(lunch)

		# print(full_month_lunch_schedule)
		print(lunch[datetime.datetime.now().strftime("%d")])


if __name__ == "__main__":
	scraper = Scraper()
	scraper.run()
	scraper.close()
