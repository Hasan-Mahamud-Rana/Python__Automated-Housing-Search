# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 00:05:41 2021

@author: Hasan Mahamud Rana
"""
import streamlit as st
import pandas as pd
import re
from geopy.geocoders import Nominatim

# Dashboard title
st.title('Avaialable near you')

DATA_URL        = ('output/result.csv')

# Enable cache
@st.cache

# get and prepare data
def load_data(nrows):
    data        = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase   = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Data loading/ loader text and success
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

# Show listing 
st.write(data.iloc[: , 1:])

# initilize geolocator
geolocator      = Nominatim(user_agent='lms4u')

lat = []
lng = []
# loop thorougg te address 
for i in range(len(data)) :
  if data.loc[i, 'address']:
    a = re.sub("[\(\[].*?[\)\]]", "", str(data.loc[i, 'address']))
    address       =  a + ', ' + data.loc[i, 'town'] + ', ' + data.loc[i, 'province']
    # Get adreess to location latitude and longitude 
    location      = geolocator.geocode(address)
    #print(address)
    #print(location.latitude, location.longitude)
    lat.append(location.latitude)
    lng.append(location.longitude)

# Create dataframe from latitude and longitude 
dfForMap = pd.DataFrame({'latitude': lat, 'longitude': lng})
#print(dfForMap)

# Display map using newly created dataframe dfForMap
st.map(dfForMap)