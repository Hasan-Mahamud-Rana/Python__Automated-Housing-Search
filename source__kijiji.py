# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 00:05:41 2021

@author: Hasan Mahamud Rana
"""
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Class kijiji class
class kijijiClass:

  # Constructor
  def __init__(self, param):
    self.param = param

  # Function to get url from form data also with the help of selenium
  def getUrl(self):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.kijiji.ca/')
    #SearchKeyword = '//*[@id="SearchKeyword"]'
    search = '//*[@id="MainContainer"]/div[1]/div/div/div/header/div[3]/div/div[2]/form/button[2]'

    #driver.find_element_by_xpath(SearchKeyword).send_keys("Student housing")
    # click at KIJIJI search button
    driver.find_element_by_xpath(search).click()

    # Get url and extract category value
    url = driver.current_url
    url = url.rsplit('/', 1)[-1]
    url = url.rsplit('?', 1)[0]

    return url

  # Function to set url from form data 
  def setUrl(self):

    category = 'c34'
    street = self.param['street']
    town = self.param['town']
    province = self.param['province']
    rangeMin = self.param['range-min']
    rangeMax = self.param['range-max']
    price = rangeMin + '__' + rangeMax

    leasetype = self.param['leasetype']
    if leasetype == 'short-term':
      leasetypeUrl = 'b-short-term-rental'
    elif leasetype == 'long-term':
      leasetypeUrl = 'b-apartments-condos'
    else:
      leasetypeUrl = 'b-for-rent'
    
    propertyType = self.param['property']

    baseUrl = 'https://www.kijiji.ca/'
    
    return baseUrl + leasetypeUrl + '/' + province + '/' + category + self.getUrl() + '?address=' + street + '+' + town + '+' + province + '&ad=offering' + '&radius=5.0' + '&price='+ price

  # Function to get listing from url

  def getListing(self):

    # print(self.setUrl())
    r = requests.get(
        self.setUrl(), 
        headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        )

    # extract content from request object
    content = r.content

    # initilize BeautifulSoup html parser
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find search result items
    listing = soup.find_all('div', {'class':'search-item'})
    
    l = []
    for item in listing:
      d = {}
      try:
          d['title'] = item.find('a', {'class':'title'}).text.strip()
      except:
          d['title'] = ''
      try:
          d['price'] = item.find('div', {'class':'price'}).text.strip()
      except:
          d['price'] = ''
      try:
          d['distance'] = item.find('div', {'class':'distance'}).text.strip().replace('< ', '')
      except:
          d['distance'] = ''
      try:
          d['area'] = item.find('div', {'class':'location'}).find('span').text.strip()
      except:
          d['area'] = ''
      try:
          d['address'] = item.find('div', {'class':'rental-info'}).find('span',{'class':'intersection'}).text.strip()
      except:
          d['address'] = ''
      try:
          d['town'] = self.param['town']
      except:
          d['town'] = ''
      try:
          d['province'] = self.param['province']
      except:
          d['province'] = ''
      try:
          d['date-posted'] = item.find('div', {'class':'location'}).find('span', {'class':'date-posted'}).text.strip().replace('< ', '')
      except:
          d['date-posted'] = ''

      l.append(d)

    return l