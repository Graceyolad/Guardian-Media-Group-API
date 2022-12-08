#!/usr/bin/env python
# coding: utf-8

# # Extracting data about Nigeria from Guardian Media Group API, converting data to a csv file and Exploring the data using Python

# ## Facts about Nigeria
# ### population of 211.4 million
# ### official language is English
# ### over 500 indigenous languages are spoken
# ### more than 25o ethnic groups
# ### largest producer of oil and gas in Africa
# ### Nigeria's largest city is Lagos with a population of over 14 million

# ## Data Extraction

# ### Importing necessary modules

# In[1]:


import requests
import json
import pandas as pd
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from pivottablejs import pivot_ui
from skimpy import skim
import seaborn as sns


# #### Extracting data from guardian media group api using 'Nigeria' as search word.

# In[2]:


#before anyone can get data from the guarduan media group api, you need to register on the platform and get an api key
#my api key is personal to me so i replaced it with 'myapikey' for the purpose of documentation of this project
#guardian media group has a documentation on how get dater using filters such as keywords, tags, date and so on. You can check it out!
api_key = 'myapikey'
link = 'https://content.guardianapis.com/search?to-date=2022-12-03&page-size=200&q=nigeria&api-key=myapikey'
response = requests.get(link)    


# In[3]:


# checking the extracted data in json format
response.json()


# In[4]:


#converting extracted data to dataframe format
data= pd.json_normalize(response.json()['response']['results'])
data


# I was able to successfully extract only one page of the data which consists of 200 rows. However, there are a total of 75 pages and a total of 15000 rows of data that contain information about Nigeria. Hence, i decided to create a for loop that helps me extract data for each of the 75 pages.
# 

# In[5]:


#extracting all the required data 
page_size = 200

my_data = []

for page in range(75):
    print('-----')
    page = page + 1
    url = f'https://content.guardianapis.com/search?to-date=2022-12-03&page-size=200&q=nigeria&api-key=myapikey'
    
    print('Requesting', url)
    
    response = requests.get(url)
    data = response.json()
    my_data.extend(data['response']['results'])
    print(url)


# In[6]:


#displaying the total extracted data
my_data


# In[7]:


#converting the extracted data from json to dataframe
df = pd.DataFrame(my_data)
df


# In[9]:


#converting datetime to date and saving it in a new column 'date'
df['date'] = pd.to_datetime(df['webPublicationDate']).dt.date


# In[17]:


#converting date column to datetime datatype
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
df


# In[18]:


#exporting data to csv 
df.to_csv('Nigeria.csv', index =False)


# ### data extraction complete code

# In[ ]:


#extracting data from guardian media group api using 'Justin Trudeau' as search word.

api_key = 'myapikey'
link = 'https://content.guardianapis.com/search?page-size=200&q=Justin%20Trudeau&api-key=myapikey'
response = requests.get(link)  

#converting extracted data to dataframe format
data= pd.json_normalize(response.json()['response']['results'])


#extracting all the required data from all the pages and appending the data
page_size = 200

my_data = []

for page in range(75):
  
    page = page + 1
    url = f'https://content.guardianapis.com/search?page={page}&page-size={page_size}&q=Justin%20Trudeau&api-key=myapikey'
    
    response = requests.get(url)
    data = response.json()
    my_data.extend(data['response']['results'])
    

#converting the extracted data from json to dataframe
df = pd.DataFrame(my_data)

#converting datetime to date and saving it in a new column 'date'
df['date'] = pd.to_datetime(df['webPublicationDate']).dt.date


# ## Data Exploration

# In[19]:


#checking the shape of the data
df.shape


# In[20]:


#checking the columns
df.columns


# In[21]:


#quick info about the data
df.info()


# In[22]:


#how maany unique values are there
df.nunique()


# In[23]:


#data summary
skim(df)


# In[17]:


#quick check for duplicate records
df.duplicated()


# #### Data Summary
# ##### There are 15000 observations and 12 features
# ##### Data types include object,boolian and datetime
# ##### The pillarId and pillarName columns have 225 nulls while the other columns have complete records
# 

# In[25]:


#showing all the information about Nigeria from 2018-01-01 till 2022-11-23
data_filtered=df.query("date >= '2018-01-01' and date <= '2022-11-23'")
data_filtered_date_sorted = data_filtered.sort_values(by = 'date')
data_filtered_date_sorted


# In[27]:


#counting the number of articles about Nigeria from 2018-01-01 till 2022-11-23
data_filtered_date_sorted[data_filtered_date_sorted['type'] == 'article']['date'].value_counts()


# In[28]:


#showing the date and count of articles about Nigeria since 2018-01-01 till 2022-11-23 and sorting by the earliest date
data_filtered[data_filtered['type'] == 'article']['date'].value_counts().sort_index()


# In[29]:


#Average number of articles of all days for the above mentioned period
(data_filtered[data_filtered['type'] == 'article']['date'].value_counts()).mean()


# In[30]:


#section with the most written article for the entire data
df[df['type'] == 'article']['sectionId'].value_counts()
#The world section has the most written article for the entire data


# In[31]:


#section with the most written article between 2018-01-01 and 2022-11-23
data_filtered[data_filtered['type'] == 'article']['sectionId'].value_counts()
#The world section has the most written article for the investigated time period


# In[37]:


#further exploration of the filtered_data
pivot_ui(data_filtered_date_sorted)
#the prevalent press publication type is article


# In[38]:


#pillarname by count of articles
pivot_ui(data_filtered_date_sorted)
#article-news had the highest amount of information about Nigeria

