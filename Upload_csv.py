#!/usr/bin/env python
# coding: utf-8

# In[6]:


GOOGLE_APPLICATION_CREDENTIALS= "C:/Users/Iryna/Desktop/test/My Project 86647-22465f35ba79.json"
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Iryna/Desktop/test/My Project 86647-22465f35ba79.json"


# In[8]:


# [START bigquery_load_from_file]
from google.cloud import bigquery
client = bigquery.Client()
filename = "C:/Users/Iryna/Desktop/test/final.csv"
dataset_id = 'my_dataset'
table_id = 'my_table'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
# [END bigquery_load_from_file]


# In[ ]:




