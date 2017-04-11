
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-reader
# + data source: http://jsonstudio.com/resources/
# ****

# In[1]:

import pandas as pd
import numpy as np


# ## imports for Python, Pandas

# In[2]:

import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas.pydata.org/pandas-docs/stable/io.html#normalization

# In[3]:

# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[4]:

# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[ ]:




# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[5]:

# further populate tables created from nested element
json_normalize(data,'counties', ['state', 'shortname', ['info', 'governor']])


# In[6]:

# load json as string
json.load((open('data/world_bank_projects_less.json')))


# In[7]:

# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[8]:
# 1. Find the 10 countries with most projects
df = pd.read_json('data/world_bank_projects.json')
df.countryname.value_counts().head(10)


# In[9]:
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
json_string = json.load((open('data/world_bank_projects.json')))
df_theme = json_normalize(json_string, 'mjtheme_namecode')
df_theme.name.value_counts().head(10)


# In[10]:
#3. Create a dataframe with the missing names filled in.

df_theme_lookup= df_theme[df_theme.name != '']  # Remove null entries
df_theme_lookup = df_theme_lookup.drop_duplicates() # remove duplicate entries of themecode and name
lookup_series = df_theme_lookup.set_index('code').name #create a series for lookup based on theme code
lookup_series


# In[11]:

#df_theme.loc[df_theme.name == '','name'] = df_theme['code'].map(lookup_series)
df_theme['name'] = df_theme['code'].map(lookup_series)
df_theme


# In[12]:

df_theme.name.value_counts().head(10)


# In[ ]:



