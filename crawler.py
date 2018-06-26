#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re
import time
import threading
from pymongo import MongoClient

def craw():
    print('\n')
    print('----------------------------------------------')
    print(time.ctime())
    found_results = ['497925426', '497796355']

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome = webdriver.Chrome(chrome_options=chrome_options)

    search_url = 'https://ba.olx.com.br/grande-salvador/salvador/instrumentos-musicais/violoes?mit=4&mit=6&pe=700&ps=100&q=viol%C3%A3o'

    print('Searching...')
    chrome.get(search_url)

    print('Find list')
    items_list = chrome.find_elements_by_css_selector(
        'div.section_OLXad-list ul.list li.item a.OLXad-list-link')

    def filter_found_items(item):
        if item.get_attribute('id') in found_results:
            # return False
            return True
        else:
            # return True
            return False

    filtered_links = [x.get_attribute('href') for x in list(
        filter(filter_found_items, items_list))]

    print('New items: ', len(filtered_links))

    for link in filtered_links:
        chrome.get(link)
        title = chrome.find_element_by_css_selector(
            'h1.OLXad-title').text.strip()
        date = chrome.find_element_by_css_selector(
            'div.OLXad-date p.text').text.strip()
        price = chrome.find_element_by_css_selector(
            'div.OLXad-price span.actual-price').text.strip()
        olx_id = chrome.find_element_by_css_selector(
            'div.OLXad-id p.text strong.description').text.strip()
        print(link)
        print(title)
        print(date)
        print(price)
        print(olx_id)

    print('Close browser')
    chrome.quit()
    threading.Timer(10, craw).start()

def mongo():
  client = MongoClient('mongodb://admin:avisa!00@ds119171.mlab.com:19171/avisa-logo')
  banco = client['avisa-logo']
  users = banco['users']
  print(users.find_one())

# craw()
mongo()
