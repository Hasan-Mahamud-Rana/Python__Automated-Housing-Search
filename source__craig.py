import requests
from bs4 import BeautifulSoup

# Class craig list class
class craiglstClass:

  # Constructor
  def __init__(self, param):
    # assign value 
    self.param = param

  # Function to set url from form data
  def setUrl(self):

    town = self.param['town']
    min_price = self.param['range-min']
    max_price = self.param['range-max']
    leasetype = self.param['leasetype']

    if leasetype == 'short-term':
      rent_period_url = '1'
    elif leasetype == 'long-term':
      rent_period_url = '4'
    else:
      rent_period_url = '4'
    
    housing_type = self.param['property']
    
    if housing_type == 'apartment':
        housing_type_url = '1'
    elif housing_type == 'condo':
        housing_type_url = '2'
    elif housing_type == 'House':
        housing_type_url = '5'
    elif housing_type == 'Room':
        housing_type_url = '1'
    else:
        housing_type_url = '1'       
       
    
    url = 'https://' + town + '.craigslist.org/search/apa?' + 'min_price='+ str(min_price) + '&max_price=' + str(max_price) + '&availabilityMode=0' + '&housing_type_url=' + housing_type_url + '&rent_period_url=' + rent_period_url + '&sale_date=all+dates'
    # print(url)
    return url

  # Function to get listing from url
  def getListing(self):
    # request get method
    r = requests.get(
        self.setUrl(), 
        headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        )

    # extract content from request object
    content = r.content
    # initilize BeautifulSoup html parser
    soup = BeautifulSoup(content, 'html.parser')

    # Find search result items
    listing = soup.find_all('li', {'class':'result-row'})
    
    l = []

    # Loop through the listing and collect required information 
    for item in listing:

      meta = item.find('div', {'class':'result-info'}).find('span',{'class':'result-meta'})

      d = {}

      try:
          d['title'] = item.find('div', {'class':'result-info'}).find('h3',{'class':'result-heading'}).find('a').text.strip() 
      except:
          d['title'] = ''
      try:
          d['price'] = meta.find('span',{'result-price'}).text.strip() 
      except:
          d['price'] = ''
      try:
          d['distance'] = ''
      except:
          d['distance'] = ''    
      try:
          d['address'] = meta.find('span',{'result-hood'}).text.strip() 
      except:
          d['address'] = ''
      try:
          d['area'] = self.param['town']
      except:
          d['area'] = ''
      try:
          d['town'] = self.param['town']
      except:
          d['town'] = ''
      try:
          d['province'] = self.param['province']
      except:
          d['province'] = ''
      try:
          d['date-posted'] = item.find('div', {'class':'result-info'}).find('time',{'class':'result-date'}).text.strip()
      except:
          d['date-posted'] = ''

      l.append(d)
      
    return l