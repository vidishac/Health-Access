"""

Objective: This program scrapes the entire HTML code of a hospital's webpage, converts it to multiple
           string lines, searches each line on 3 specified string patterns to find the extension of 
           the appointment page of that website (hospital/healthcare provider). 
           

Packages required:
    a. requests 
    b. bs4
    c. re

Other things to note:
    a. The limitation of this code is that if an appointment page extension exists but the keyword is
       not one among 'appointment', 'schedule', 'request-a-tour', this code won't be able to catch it. 
    b. Not all hospital websites have an apppointment page extension
    c. The input for this program would be the website that another program (hospital_website_finder_2) 
       returns


"""

import requests
from bs4 import BeautifulSoup
import re


def appt_page(hospital_url):
    
    #If the hospital_website_finder_2 couldn't return a valid website
    if hospital_url == 'website not found':
        return {'appt_link':'page doesn\'t exist','confirmation':0}
    
    else:
        try:
            #Complete the url 
            complete_url = 'http://' + hospital_url
            grab = requests.get(complete_url)       #Go to the webpage
            soup = BeautifulSoup(grab.text, 'html.parser')      #Parse the html code
             
            # opening a file in write mode
            f = open("extension.txt", "w")          
            # traverse paragraphs from soup
            for link in soup.find_all("a"):     #Search along the HTML a tags to find links
               data = link.get('href')          #Get all href links
               if data!=None:
                   f.write(data)                #Write those to the text file
                   f.write("\n")
             
            f.close()
            
            #Define search patterns
            pattern1 = r'appointment'
            pattern2 = r'schedule'
            pattern3 = r'request-a-tour'
            
        
            #extracting the appt extension
            found = 0
            
            #Loop through each line, match against pattern, extract first match
            with open('extension.txt','r') as f:
                    for line in f:
                            if found == 0:
                                if re.search(pattern1,line) != None:
                                    text = line
                                    found+=1
                                elif re.search(pattern2,line) !=None:
                                    text = line
                                    found+=1
                                elif re.search(pattern3,line)!=None:
                                    text = line
                                    found+=1
            
            #Correcting the extensions
            if found == 0:
                appt_link = "page not found"
                website_exists = 0
            
            else:
                
                if text[-1] == '\n':    
                    text = text[:-1]    #Removing newline character if it exists
                text = re.search(r'/.*',text).group(0)      #Getting only the extension part
                       
                appt_link = hospital_url + text       #Manually concatenating it to form a searchable url
                
                
                #Checking if the webpage exists (since we are constructing by adding strings)
                
                try:
                    response = requests.get('http://' + appt_link)
                except:
                    response.status_code =0
                    
                if response.status_code == 200:
                    website_exists =1
                else:
                    website_exists=0
                
                #If website doesn't exist, not passing the constructed string (if any)
                if website_exists == 0:
                    appt_link = 'page not found'
                
            return {'appt_link':appt_link,'confirmation':website_exists}
        except:
            return {'appt_link':'page not found','confirmation':0}
     
