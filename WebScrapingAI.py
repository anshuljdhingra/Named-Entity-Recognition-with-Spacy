
# coding: utf-8

# In[5]:


import urllib
import urllib.request
import urllib.parse
#import tldextract
import re
from bs4 import BeautifulSoup
import string
import json
#from urlparse import urljoin


#=== Read Excel Sheet =========
import xlrd

#=== Write to CSV file ===
import csv

#==Os library baig used to delete a file
import os

urlResultSheetPath="" #=r"C:\Users\gaurav.anand\Downloads\Web Scraping AI\Website_Extraction_results.csv"
urlSheetPath=""
contentFilePath=""
data=""

def read_configuration():
    global urlResultSheetPath
    global urlSheetPath
    global contentFilePath
    global data
    with open('Configuration.json') as json_data_file:
        data = json.load(json_data_file)        
        
    print("Input Website List File Path : "+ data["input"]["Input_WebSite_list"])
    #urlSheetPath=data["input"]["Input_WebSite_list"]
        
    print("Output result file is : "+data["output"]["Extration_Result_File_Path"])
    #urlResultSheetPath=data["output"]["Extration_Result_File_Path"]
        
        
    print("Output Content exyraction path is : "+data["output"]["Extrated_Content_File_Path"])
    #contentFilePath=data["output"]["Extrated_Content_File_Path"]  

def delete_extraction_result_File():
    #global urlResultSheetPath
    
    urlResultSheetPath=data["output"]["Extration_Result_File_Path"]
    if os.path.exists(urlResultSheetPath):
        os.remove(urlResultSheetPath)
        print("Result File deleted : " + urlResultSheetPath)
    
#zero based Index and Column
def read_excel_sheet(sheetIndex, rowNum, colNum):
    #global urlSheetPath
    #urlSheetPath=r"C:\Users\gaurav.anand\OneDrive - NIIT Technologies 1\Automation COC\SVN\WebScraping\WebScraping\Websites for Charles.xlsx"
    #urlSheetPath=r"C:\Users\gaurav.anand\OneDrive - NIIT Technologies 1\Automation COC\SVN\WebScraping\WebScraping\Websites-Single.xlsx"
    urlSheetPath=data["input"]["Input_WebSite_list"]
    Web_Sites=[] #Holds thr tickets

    
    # To open Workbook 
    wb = xlrd.open_workbook(urlSheetPath) 
    sheet = wb.sheet_by_index(sheetIndex) 

    print("Number of Web Sites :",sheet.nrows)

    for i in range(rowNum,sheet.nrows):
        Web_Sites.append(sheet.cell_value(i, colNum))
       # print(sheet.cell_value(i, 0),' ',sheet.cell_value(i, 3))
    
    return Web_Sites

def Addto_extrction_result_sheet(url,status,parentDomainUrl,error=None):
    
    mydata=[]
    #global urlResultSheetPath
    urlResultSheetPath=data["output"]["Extration_Result_File_Path"]    
    myFile = open(urlResultSheetPath, 'a') 
    with myFile:
        writer = csv.writer(myFile,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([parentDomainUrl,url,status,error])
        
    

#Removes all the special charachers in string/Website URL
def strip_url(url):
    return re.sub('\W+','', url)
    
def write_Website_text(webText,url):
    global contentFilePath
    print("Writing file for "+ url + " to Disk ")
    filename= strip_url(url)
    #contentFilePath=r"C:\Users\gaurav.anand\OneDrive - NIIT Technologies 1\Automation COC\SVN\WebScraping\WebScraping"
    contentFilePath=data["output"]["Extrated_Content_File_Path"]
    contentFilePath+="\\"+filename +".txt" 
    
    #webSiteTextFile = open(contentFilePath,"w",encoding="utf-8")
    webSiteTextFile = open(contentFilePath,"w",encoding="utf-8")
    webSiteTextFile.write(webText)  
    print("Web Site Content for " + url +" has been written to Disk File")
    webSiteTextFile.close()




#Hint List of Sublinks
hintUrlLinks=[]
#hintUrlLinks.append("about us")
#hintUrlLinks.append("about-us")
hintUrlLinks.append("about")
hintUrlLinks.append("team")
hintUrlLinks.append("leadership")
hintUrlLinks.append("contact")
hintUrlLinks.append("people")
hintUrlLinks.append("story")
hintUrlLinks.append("professional")
#hintUrlLinks.append("our resources")
hintUrlLinks.append("biography")
hintUrlLinks.append("adviser")


#List of Website Sublinks
websiteSubLinks=[]

#Checks if webste is relevant for content scraping
def isRelevantSubsite(subsiteUrl, hrefText):
    isRelevantSubsite=None
    
    if(subsiteUrl.endswith(".pdf")):
        print("URL Excluded : "+ subsiteUrl)
        
    else:
        matches = (x for x in hintUrlLinks if x.lower() in hrefText.lower() or x.lower() in subsiteUrl.lower())
        
        for x in matches:
            isRelevantSubsite=True
            print("===>>>>>>>    =====<<<<<<")
            print("\n" +" Subsite : " +subsiteUrl +" is relevant for scraping for keyword : " +  str(x))
            print("===>>>>>>>    =====<<<<<<")
    
    return isRelevantSubsite

def addRelevantSubsitetoList(domainUrl,subsiteURL):
    
    global  websiteSubLinks
    
    #print('Pre --->Subsite being Added to List for extraction : '+ subsiteURL)
    if  subsiteURL.find("http")==-1:
        if subsiteURL[0]!=r"/":
            subsiteURL="/"+subsiteURL
        subsiteURL=domainUrl+subsiteURL
    subsiteURL=subsiteURL.replace(" ","")
   
    #print('-->Subsite being Added to List for extraction : '+ subsiteURL)
    if subsiteURL not in websiteSubLinks:
        websiteSubLinks.append(subsiteURL)
        #print('Subsite Added to List for extraction : '+ subsiteURL)
    
def remove_NewLine_Characters_fromWebText(webText):
    webText=webText.replace('\n',' ').replace('\r','')
    return webText
    
def is_ExcludeLine(lineString):
    isBlackListed=False
    #print(" =>>> Line Strinig before Black Listing : " + lineString)
    blacklist = [".html","©","facebook","youtube","twitter","instagram","linkedin"]
    for obj in blacklist:
       
        if obj in lineString:
            #print("Black List Object : " + obj)
            isBlackListed=True
                
    return isBlackListed

def make_string_replacements(webText):
    # Python program to extract emails From 
    # the String By Regular Expression. 


    # \S matches any non-whitespace character 
    # @ for as in the Email 
    # + for Repeats a character one or more times 
    lst = re.findall('\S+@\S+', webText)

    # Printing of List 
    print(lst) 
    emailExtlist = [".com"]
    for email in lst:
        index=webText.index(email)
        print("Email " + email + " found at index" + str(index))
        if index>-1:
            emailExtIndex=email.index(".com")
            emailNew=email
            if emailExtIndex>-1:
                
                emailNew=emailNew.replace(".com",".com ",1)
                print("Replacing "+ "emailExtlist[0]"+ " with " + emailNew)
            webText=webText.replace(email,emailNew,1)
            
            print("inside email replacement loop")


        #print("The new string is : "+ webText)
    return webText


def invoke_url(url):
       
        hdr = {'User-Agent': 'Mozilla/5.0'}
        
        print("Opening URL now : " + url)
        
        
        #proxy_support = urllib.request.ProxyHandler({"http": "http://gaurav.anand:steelrigminton@28@172.18.50.192:80",  "https": "http://gaurav.anand:steelrigminton@28@172.18.50.192:80"})
        #opener = urllib.request.build_opener(proxy_support)

        #urllib.request.install_opener(opener)

        
        
        req=urllib.request.Request(url,headers=hdr)
        #thePage=urllib.request.urlopen(url)
        #thePage=urllib.request.urlopen(url, data=bytes(json.dumps(hdr), encoding="utf-8"))
        thePage=urllib.request.urlopen(req)
        
        print('Successfully Opened Url')
        return thePage

def extract_content_from_frames(soup,parentDomainUrl,isSubsite):
    
    webText=""
    print("Checking for Frames")
    
    
    for frame in soup.select("frameset frame"):
        print("Identified Frame.Attempting to joing Frame Url")
        
        
        httpIndex= parentDomainUrl.find("http")
        if httpIndex== -1:
            parentDomainUrl="http://"+parentDomainUrl
            
        print("Parent Url : " + parentDomainUrl)
        frame_url = urllib.parse.urljoin(parentDomainUrl, frame["src"])
        print("Joined Frame url : " + frame_url)
        #frame_url=frame["src"]

        response=invoke_url(frame_url)
        frame_soup = BeautifulSoup(response, 'html.parser') 
        
        for element in frame_soup.findAll():

            print("Element Text is : " + element.text)
            webText +=element.text
        
    #print(webText)    
    return webText
    

    
def extract_website_content(url,parentDomainUrl,isSubsite=False):
    if not isSubsite:
        websiteSubLinks.clear()
   
    httpIndex= url.find("http")
    print("Http Index in URL " + url + " is : " + str(httpIndex))
    if httpIndex== -1:
        print("Prefixing URL with Http")
        url="http://"+url
    
        
    print("Extracting Page URL  : " + url) 
    print("Is Subsite : " + str(isSubsite)) 
    
    try:
        
        
        thePage=invoke_url(url)
        
        soup=BeautifulSoup(thePage,"html.parser")
        #soup=BeautifulSoup(thePage,"lxml")
        
        #print(soup)

        #blacklist = ["script", "style","img","link" ]
        blacklist = ["script", "style","img" ]
        [s.extract() for s in soup(blacklist)] # remove tags in Blacklist

        webText=""

        
        
        for link in soup.findAll():
            #print(link.get('href'))
            #print(link.text)

            #webText +=link.name
            #webText+="\n"
            if not is_ExcludeLine(link.text):
                webText +=link.text
                        
            
            if link.name=="a": # add Leadership/Contect list check
                webText +=" : "
                #webText+=str(link.get('href'))
                href=str(link.get('href'))
                if not is_ExcludeLine(href): #href.find(".html")==-1: 
                    webText+=href

                if not isSubsite and isRelevantSubsite(str(link.get('href')),link.text):
                      addRelevantSubsitetoList(url,str(link.get('href')))

            
            webText+="\n"
            #webText +="======="
            #webText+="\n"

        #Adding content from frames
        webText+=extract_content_from_frames(soup,parentDomainUrl,isSubsite)
        
        print ("   ")
        print ("   ")
        print ("====================")
        print (" Printing Webtext  ")
        print ("====================")
        #print (webText)
        
        #print("begin-- adding Email surfix and prefix with space")
        #webText=make_string_replacements(webText) # prefix and surfix an email id with space
        #print("End-- adding Email surfix and prefix with space")
        write_Website_text(webText,url)
        Addto_extrction_result_sheet(url,"Success",parentDomainUrl)

    
    except Exception as e:
        print('Error in last operation : ', str(e) )
        
        Addto_extrction_result_sheet(url,"Fail",parentDomainUrl,str(e))
        pass
        
           



def execute_content_extraction_engine():
   
    global urlArr
    global websiteSubLinks
    
    url_list=[]
    
    read_configuration()
    
    #Delete Extraction Result Sheet
    delete_extraction_result_File()
    
    #Read all 80K domain names from Excel Sheet
    url_list=read_excel_sheet(0,1,0)
    
    #Extract Contant for Main Site
    for urlSite in url_list:
        extract_website_content(urlSite,urlSite,False)
        #Extract Contant for Subsite
        for urlSubSite in websiteSubLinks:
            extract_website_content(urlSubSite,urlSite,True)
    
    
    print(websiteSubLinks)

execute_content_extraction_engine()

