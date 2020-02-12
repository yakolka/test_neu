#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df1 = pd.read_csv("C:/Users/Iryna/Desktop/test/orders_s.csv")
df2 = pd.read_csv("C:/Users/Iryna/Desktop/test/products.csv")


# In[42]:


#drop dublicates based on two columns 'order_source_id' and 'product_id'
df1 = df1.drop_duplicates(subset=['order_source_id', 'product_id']) 


# In[43]:


#convert all names into Latin alphabet
def transliterate(name):


    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
           
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


df1["name"] = df1["name"].map(lambda x: transliterate(x))
df1["surname"] = df1["surname"].map(lambda x: transliterate(x))
df1["patronymic"] = df1["patronymic"].map(lambda x: transliterate(x))


  


# In[45]:


#cleaning 'product_id' column - leaving only 6 digits
df1['product_id'] = df1['product_id'].str.extract('^(\d{6})$', expand=False)

#dealing with Nan variables in 'product_id'
df1['product_id'] = pd.to_numeric(df1['product_id'], errors='coerce')
df1 = df1.dropna(subset=['product_id'])

#transforming 'product_id' column to int type for merging with products dataframe
df1['product_id']=df1['product_id'].astype(int)
final = df1.merge(df2,on='product_id')

final


# In[40]:


export_csv = final.to_csv("C:/Users/Iryna/Desktop/test/final.csv", index = None, header=True)


# In[ ]:





# In[51]:



# for defining similarity I used cosine similarity measure from sklearn. 
# is a measure of similarity between two non-zero vectors of an inner product space 
# that measures the cosine of the angle between them. 
# It use calculated measure between vectores, so I made one hot encoding for 
# categorical veriables And devide price by 1000 (obtained values around 1 - it allows make type 
# of toys and manufacture more valuable, but still makes difference in similarity based on prices)
# after all I calculated the average between all productes in supposed list
#it gives value of similarity between target product and several productes


def sim(product_id,a):
    
    target = df2[df2['product_id'] == product_id] 
    for n in a:      
        target = target.append(df2[df2['product_id'] == n])
    
    target = pd.concat([target.price.div(1000), pd.get_dummies(target['goods_group'], prefix = 'category'),
                        pd.get_dummies(target['manufacturer'], prefix = 'category')], axis=1)
   
    return sum((cosine_similarity(target)[0])[1:]) / len((cosine_similarity(target)[0])[1:])



    
sim(518303,[483259,518020,503982,538501,350926,521360])


# In[53]:


def n_sim(product_id,n):
    full = df2
    target = df2
    target = pd.concat([target.price.div(1000), pd.get_dummies(target['goods_group'], prefix = 'category'),
                        pd.get_dummies(target['manufacturer'], prefix = 'category')], axis=1)
   
    arr = list(cosine_similarity(target)[0])
    full = df2.assign(similarity=arr)
    full = full.sort_values(by=['similarity'])
    k = []
    for n in range (1,n+1):        
        k.append(full.at[n,'product_id'])
        
    return k
 
n_sim(527057, 7)


# In[56]:


#function takes product_id and N - number of most similar productes
# and return product_id these productes

def n_sim(product_id,n):
    
    full = df2    
    full = pd.concat([df2.price.div(1000), pd.get_dummies(df2['goods_group'], prefix = 'category'),
                        pd.get_dummies(df2['manufacturer'], prefix = 'category')], axis=1)
   
    arr = list(cosine_similarity(full)[0])
    full = df2.assign(similarity=arr)
    full = full.sort_values(by=['similarity'])
    k = []
    for n in range (1,n+1):        
        k.append(full.at[n,'product_id'])
        
    return k
 
n_sim(527057, 7)


# In[ ]:




