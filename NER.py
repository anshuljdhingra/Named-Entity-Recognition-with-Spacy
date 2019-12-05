
# coding: utf-8

# In[868]:


import spacy 
#nlp = spacy.load('en_core_web_lg')
#nlp = spacy.load('en_vectors_web_lg')
nlp = spacy.load('en')
import re
import nltk
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import os
import xlsxwriter
from spacymodelstopwords import * 
from xlrd import open_workbook, XLRDError
import warnings
warnings.filterwarnings("ignore")


# In[869]:


loc = r'C:\Users\Gaurav.Anand\Downloads\Web Scraping AI\Website_Extraction_results.csv'
savepath = 'C:\\Users\\Gaurav.Anand\\Downloads\\Web Scraping AI\\webpages\\'
newp = 'C:\\Users\\Gaurav.Anand\\Downloads\\Web Scraping AI\\webpages\\'
excelpath = "C:\\Users\\Gaurav.Anand\\Downloads\\Web Scraping AI\\output\\"
filepath = 'C:\\Users\\Gaurav.Anand\\Downloads\\Web Scraping AI\\extracts\\'
path = 'C:\\Users\\Gaurav.Anand\\Downloads\\Web Scraping AI\\webpages\\'


# In[870]:


# In[871]:


#nlp = spacy.load('en_web_core_sm')


# In[872]:


def strip_url(url):
    return re.sub('\W+','', url)


# In[873]:


import xlrd
import csv

import pandas as pd 
df2 = pd.read_csv(loc, encoding='cp1252',header=None)


# In[874]:


df2.head()


# In[875]:


#test = list(range(0,22)) + list(range(23,53))


# In[876]:


#df2 = df2.iloc[list(range(0,22)) + list(range(23,53)), :]


# In[877]:


df2 = df2[[0,1,2]]


# In[878]:


df2.dropna(axis=0, inplace=True)


# In[879]:


df2.head()


# In[880]:


df2['main'] = df2[0].apply(lambda x: strip_url(x))


# In[881]:


df2['ind'] = df2[1].apply(lambda x: strip_url(x))


# In[882]:


df2.reset_index(drop=True,inplace=True)


# In[883]:


df2.head()


# In[884]:


#df2[2][0] = 'Fail'


# In[885]:


#df2.loc[df2[2] == 'Success'][['main', 'ind']]


# In[886]:


web_dict = dict(zip(df2['ind'], df2[1]))


# In[887]:


print(web_dict)


# In[888]:


df2 = df2.loc[df2[2] == 'Success']


# In[889]:


df2.head()


# In[890]:


df3 = df2.groupby(by='main')


# In[891]:
import glob, os, os.path
filelists = glob.glob(os.path.join(savepath, "*.txt"))
for f in filelists:
    os.remove(f)


#savepath = 'C://Users//Anshul.Dhingra//Desktop//NER//Input//webpages//'
for i in df2.main.unique():
    #print(i)
    fil =  i + '.txt'
    print(fil)
    with open((os.path.join(savepath,fil)), 'w+', encoding = 'utf-8') as f:
        #print(f)
        for j in df3.get_group(i)['ind']:
            print(j)
            text = ""
            text = str(j) + '.txt'
            f.write(text)
            f.write('\n')
    #print(df3.get_group(i)['ind'])


# In[892]:


#a = df3.get_group(df2.main.unique()[1])['ind']


# In[893]:


#newp = 'C://Users//Anshul.Dhingra//Desktop//NER//Input//webpages//'
fname = []
import glob, os
os.chdir(newp)
for file in glob.glob("*.txt"):
    fname.append(file)

#fname.append('abc.txt')


# In[894]:


print(fname)


# In[895]:


import glob, os, os.path

filelist = glob.glob(os.path.join(excelpath, "*.csv"))
for f in filelist:
    os.remove(f)


# In[896]:


'''#path = 'C://Users//Anshul.Dhingra//Desktop//NER//Input//webpages//'
for f_ in fname:
    excelworkbook = f_.split('.')[0] + '.xlsx'
    #excelpath = "C:\\Users\\Anshul.Dhingra\\Desktop\\NER\\Output\\"
    excelfinal = (os.path.join(excelpath, excelworkbook))
    print(excelworkbook)
    workbook = xlsxwriter.Workbook(excelfinal)
    worksheet = workbook.add_worksheet()'''


# In[ ]:


#path = 'C://Users//Anshul.Dhingra//Desktop//NER//Input//webpages//'
for f_ in fname: #
    with open(os.path.join(path, f_), encoding='utf-8', errors='ignore') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    print(content)
    #startrow=0
    #filepath = 'C://Users//Anshul.Dhingra//Desktop//NER//Input//webpages//extracts//'
    for c in content:
        exists = os.path.isfile(os.path.join(filepath,c))
		#exists = os.path.isfile(os.path.join(filepath,c))
        print(exists)
        print(c)
        if exists:
            with open((os.path.join(filepath,c)), 'r', encoding = 'utf-8', errors='ignore') as myfile:
                #file=myfile.read().replace('\n', ' ')
                file=myfile.read().rstrip('\r\n')
                document = nlp(file)
                entities = [e.string for e in document.ents if 'PERSON'==e.label_] 
                entities = list((set(entities)))
                print (entities)
                names = []
                for word in entities:
                    if word not in stop:
                        print(word)
                        word.replace("\n", "")
                        word.replace("\t", "")
                        #word.replace("  ", "")
                        names.append(word)
                names = set(names)
                names = ', '.join(names)
                #names = names.replace('"', '\'')
                names = names.replace('\n', '')
                l = names.split(',')
                print(l)
                final_names = []
                for word in l:
                    if re.match(r'\s', word):
                        word = word.lstrip()

                    if " " in word:
                        final_names.append(word)
                final_names = [name for name in final_names if name not in stop]
                print(final_names)
                def extract_phone_numbers(file):
                    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
                    phone_numbers = r.findall(file)
                    return [re.sub(r'\D', '', number) for number in phone_numbers]

                def extract_email_addresses(file):
                    r = re.compile(r'[\w\.-]+@[\w\.-]+')
                    return r.findall(file)

                numbers = set(extract_phone_numbers(file))
                emails = set(extract_email_addresses(file))

                doc = nlp(file)
                company = []
                for ent in doc.ents:
                     if ent.label_ == 'GPE'  and ent.text not in company: #ent.label_ == 'LOC' or
                        company.append(ent.text)
                print (set(company))

                address = []
                for word in set(company):
                    if word not in stop:
                        print(word)
                        word.replace("\n", "")
                        word.replace("\t", "")
                        #word.replace("  ", "")
                        address.append(word)
                address = ', '.join(address)
                #names = names.replace('"', '\'')
                address = address.replace('\n', '')

                print(address)

                l2 =address.split(',')
                print(l2)
                final_address = []
                for word in l2:
                    word = word.strip()
                    final_address.append(word)
                #    if re.match(r'\s', word):


                final_address = [add for add in final_address if add not in stop]
                print(final_address) 

                df = pd.DataFrame(data = [final_names, final_address, list(numbers), list(emails)])
                df = df.T
                df.columns = ['Name', 'Address', 'Contact#', 'Email']
                df['Title'] = ' '
                df['URL'] = c
                df['URL'] = df['URL'].apply(lambda x: x.split('.')[0])
                #df['URL'] = df['URL'][0]
                df['URL'] = df['URL'].map(web_dict)
                df['URL'] = df['URL'].drop_duplicates(keep='first')
                df.fillna(value = ' ', inplace=True)
                df = df[['Name', 'Title','Address', 'Contact#', 'Email', 'URL']]
                print(df)

                mycsv = f_.split('.')[0] + '.csv'
                try:
                    with open(os.path.join(excelpath, mycsv), 'a') as f:
                        df.to_csv(f, header=True, sep=',', encoding='cp1252', index=False)
                        f.write(' ')
                        f.write(" ")
                except UnicodeEncodeError:
                    pass
                    
        else:
            failed = 'failed.txt'
            with open(os.path.join(excelpath, failed), 'a') as f:
                f.writelines(c)
                f.writelines('\n')          


# In[ ]:





# In[ ]:




           

