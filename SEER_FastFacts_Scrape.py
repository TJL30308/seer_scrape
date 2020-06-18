#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


# In[ ]:


url = f'https://seer.cancer.gov/statfacts'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html')
cancers = soup.find_all("div", class_='alphaList rpw')


# In[ ]:


links = []

for a in soup.find_all('a', href=True):
    links.append(a['href'])

cancer_links = links[144:186]


# In[ ]:


cancer_dict = {}

i = 0

while i < len(cancer_links):
    try:

        data_cancer = f'https://seer.cancer.gov{cancer_links[i]}'

        a_response = requests.get(data_cancer)
        soup = BeautifulSoup(a_response.text, 'html')

        span_array = soup.find("div", class_='glance-factSheet').findAll('span')

        cancer = soup.find('h1').text.strip().split(":")[1].lstrip()
        cases = int(span_array[1].text.strip().replace(",",""))
        
        cancer_dict.update({cancer : cases})

        print(f'Estimated New Cases of {cancer} in 2020')
        print(cases)
        print(data_cancer)
        print('--------------------')
    
        i += 1
        
    except (AttributeError, IndexError):
        print(f'{cancer}: error - check page')
        print(data_cancer)
        print('--------------------')
    
        i += 1
        
print('task complete')


# In[ ]:


df = pd.DataFrame.from_dict(cancer_dict, orient='index')
df


# In[ ]:




