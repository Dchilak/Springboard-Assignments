
# coding: utf-8

# # XML example and exercise
# ****
# + study examples of accessing nodes in XML tree structure  
# + work on exercise to be completed and submitted
# ****
# + reference: https://docs.python.org/2.7/library/xml.etree.elementtree.html
# + data source: http://www.dbis.informatik.uni-goettingen.de/Mondial
# ****

# In[1]:

from xml.etree import ElementTree as ET


# ## XML example
# 
# + for details about tree traversal and iterators, see https://docs.python.org/2.7/library/xml.etree.elementtree.html

# In[2]:

document_tree = ET.parse( './data/mondial_database_less.xml' )


# In[3]:

# print names of all countries
for child in document_tree.getroot():
    print (child.find('name').text)


# In[4]:

# print names of all countries and their cities
for element in document_tree.iterfind('country'):
    print ('* ' + element.find('name').text + ':'),
    capitals_string = ''
    for subelement in element.getiterator('city'):
        capitals_string += subelement.find('name').text + ', '
    print (capitals_string[:-2])


# ****
# ## XML exercise
# 
# Using data in 'data/mondial_database.xml', the examples above, and refering to https://docs.python.org/2.7/library/xml.etree.elementtree.html, find
# 
# 1. 10 countries with the lowest infant mortality rates
# 2. 10 cities with the largest population
# 3. 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
# 4. name and country of a) longest river, b) largest lake and c) airport at highest elevation

# In[5]:

import pandas as pd
import numpy as np
document = ET.parse( './data/mondial_database.xml' )


# In[6]:

#1. 10 countries with the lowest infant mortality rates


# In[7]:

#country_mortrate_dict = {}
data=[]
for element in document.findall('country'):
    country = element.find('name').text
    mortrate = element.find('infant_mortality')
    if mortrate is not None:
#        country_mortrate_dict['country'] = float(mortrate.text)
       data.append([country,float(mortrate.text)]) 

country_mortrate_df = pd.DataFrame(data,columns=(['name','infant_mortality']))
country_mortrate_df.sort_values('infant_mortality').head(10)
#df=pd.DataFrame(country_mortrate_dict.items(),columns=(['name','infant_mortality']))


# In[8]:

#2. 10 cities with the largest population


# In[9]:

populations=[]
for element in document.findall('.//city'):
    city=element.find('name').text
    pop_data=[]
    for subelement in element.getiterator('population'):
        population=subelement.text
        pop_data.append([(int(subelement.get('year'))), int(population)])
    if pop_data!=[]:
        max_population =max(pop_data)[1]
        max_year=max(pop_data)[0]
    populations.append([city,max_population,max_year])
    
pop_df=pd.DataFrame(populations,columns=(['city','population','year']))

pop_df.sort_values('population',ascending=(False)).head(10)


# In[10]:

#3. 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)


# In[11]:

data=[]
for element in document.iterfind('country'):
    country = element.find('name').text
    populations=[]
    for subelement in element.getiterator('population'):
        population=subelement.text
        populations.append([int(subelement.get('year')), int(population)])
    pop_max=max(populations)[1]
    for subelement in element.getiterator('ethnicgroup'):
        ethnicgroup = subelement.text
        if ethnicgroup is not None:
            percentage=float(subelement.get('percentage'))
            ethnic_pop = percentage * pop_max/ 100
            data.append([country,pop_max,percentage,ethnicgroup,ethnic_pop]) 
        
df = pd.DataFrame(data,columns=(['country','pop_max','percentage','ethnicgroup','ethnic_pop']))
pd.options.display.float_format = '{:20,.2f}'.format
df    
        


# In[12]:

t=df.groupby('ethnicgroup',as_index=False).ethnic_pop.sum()
pd.options.display.float_format = '{:20,.2f}'.format
t.sort_values('ethnic_pop',ascending=(False)).head(10)


# In[13]:

#4. name and country of a) longest river, b) largest lake and c) airport at highest elevation


# In[41]:

countries={}
for element in document.iterfind('country'):
    countryid= element.get('car_code')
    countryname=element.find('name').text
    countries[countryid]= countryname


# In[42]:

rivers=[]
for river in document.iterfind('river'):
    river_name = river.find('name').text
    for country in river.get('country').split():
        length=river.find('length')
        if length is not None:
            length =float(length.text)
            rivers.append([river_name,length,countries[country]])
river_df = pd.DataFrame(rivers,columns=(['river','length','country']))


# In[45]:

lakes=[]
for lake in document.iterfind('lake'):
    lake_name = lake.find('name').text
    for country in lake.get('country').split():
        area=lake.find('area')
        if area is not None:
            area =float(area.text)
            lakes.append([lake_name,area,countries[country]])
lake_df = pd.DataFrame(lakes,columns=(['lake','area','country']))


# In[67]:

airports=[]
for airport in document.iterfind('airport'):
    airport_name = airport.find('name').text
    for country in airport.get('country').split():
        elevation=airport.find('elevation').text
        if elevation is not None:
            elevation =float(elevation)
            airports.append([airport_name,elevation,countries[country]])
airport_df = pd.DataFrame(airports,columns=(['airport','elevation','country']))


# In[68]:

river_df[river_df.length == river_df.length.max()]


# In[69]:

lake_df[lake_df.area == lake_df.area.max()]


# In[71]:

airport_df[airport_df.elevation == airport_df.elevation.max()]


# In[ ]:



