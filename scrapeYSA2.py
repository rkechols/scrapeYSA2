import os
import time
from asyncio import wait_for
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException


START_URL = "https://ysa2.org/"
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")


def write_to_file(people_by_address):
	pass


class Person:
	def __init__(self, name, address, phone, email, birthday):
		self.name = name
		self.address = address
		self.phone = phone
		self.email = email
		self.birthday = birthday


def scrape_page():
	# load the login page
	page = webdriver.Chrome()
	page.get(START_URL)
	# find <input type="email" name="eml" placeholder="Email address" required="">
	# and <input type="password" name="pwd" placeholder="Password" required="">
	inputs = page.find_elements_by_tag_name("input")
	inputs[0].send_keys(LOGIN_EMAIL)
	inputs[1].send_keys(LOGIN_PASSWORD)
	# find <button type="submit">Log In</button>
	button = page.find_element_by_tag_name("button")
	click_then_wait(button)
	# find <table id="table-body">...</table>
	table = page.find_element_by_id("table-body")
	# save all the people's info
	people_by_address = dict()
	table_rows = table.find_elements_by_tag_name("tr")
	for row in table_rows:
		row_pieces = row.find_elements_by_tag_name("td")
		text_pieces = [piece.text for piece in row_pieces]
		person = Person(text_pieces[0], text_pieces[1], text_pieces[2], text_pieces[3], text_pieces[4])
		address_group = people_by_address.get(person.address, set())
		address_group.add(person)
		people_by_address[person.address] = address_group
	return people_by_address


# HELPFUL FUNCTIONS


def link_has_gone_stale(link):
	try:
		# poll the link with an arbitrary call
		link.find_elements_by_id('doesnt-matter')
		# if it doesn't throw an exception, the next page hasn't loaded yet
		return False
	except StaleElementReferenceException:
		# the link that we clicked is gone, meaning that we're on a new page
		return True


def click_then_wait(link):
	link.click()
	wait_for(link_has_gone_stale(link), 10)
	time.sleep(5)


if __name__ == "__main__":
	results = scrape_page()
	write_to_file(results)
