"""
Objective: This program uses an API provided by the National Plan and Provider Enumeration System
(NPPES) to get data on "Organization Name","Address", "Tel-no" and "Category" for various health
facilities in Pittsburgh listed in the National Provider Identifier (NPI) registry. It then uses 
string matching to match the categories defined in the registry data to simpler, user-friendly keywords
defined by us. 

The final output of this program is a csv file that has hospital name, address, phone number, categories 
and matched keywords.

Packages required:
    a. requests 
    b. json
    c. pandas
    d. re

    

"""
# Using NPPES API


def hospital_list():
    
    import requests
    import json
    import pandas as pd
    import re

    headers = {'Content-Type': 'application/json'}
    
    count = 0
    
    # Limit on the number of records that can be queried through API
    count_max = 5
     
   
    rows = []
    
    # Restricting the number of API queries in order to limit data set to 992 hospitals
    # The registry has many more facilities listed
    
    while  count <= 400:
    
        if count< count_max:
                 
            url = 'https://npiregistry.cms.hhs.gov/api/?version=2.0&enumeration_type=NPI-2&taxonomy_description=&first_name=&last_name=&organization_name=&address_purpose=PRIMARY&city=pittsburgh&state=&postal_code=&country_code=&limit=200&'+'skip='+ str(count*200) +'&pretty=on&version=2.0'
            
            response = requests.get(url, headers = headers)
    
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
            
           
            
            for i in data["results"]:
                
                organization = i["basic"]["organization_name"]
                 
                address = " ".join([
                i["addresses"][0]["address_1"],
                i["addresses"][0]["address_2"],
                i["addresses"][0]["city"],
                i["addresses"][0]["country_name"],
                i["addresses"][0]["postal_code"],
                i["addresses"][0]["state"]
                ])
                telephone = i["addresses"][0]["telephone_number"]
                for j in i["taxonomies"]:
                    if j["primary"] == True:
                        category = j["desc"]   
                rows.append([organization,address, telephone, category])
            
            
            count += 1
        
        elif count>= count_max:
            
            url = 'https://npiregistry.cms.hhs.gov/api/?version=2.0&enumeration_type=NPI-2&taxonomy_description=&first_name=&last_name=&organization_name=&address_purpose=PRIMARY&city=pittsburgh&state=&postal_code=&country_code=&limit=200&'+'skip='+ str(1000)+'&pretty=on&version=2.0'
    
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
            
                       
            
            for i in data["results"]:
                
                organization = i["basic"]["organization_name"]
                 
                address = " ".join([
                i["addresses"][0]["address_1"],
                i["addresses"][0]["address_2"],
                i["addresses"][0]["city"],
                i["addresses"][0]["country_name"],
                i["addresses"][0]["postal_code"],
                i["addresses"][0]["state"]
                ])
                telephone = i["addresses"][0]["telephone_number"]
                for j in i["taxonomies"]:
                    if j["primary"] == True:
                        category = j["desc"]   
                rows.append([organization,address, telephone, category])
                
                        
            count += 1
            
    hospital_data = pd.DataFrame(rows,columns = ["Organization Name", "Address", "Tel-no", "Category"])
    
    hospital_data.drop_duplicates(inplace=True)
    
    # String Matching
    
    """Step 1: Identifying the categories:
    
    1. Surgery: surge
    2. Dental Care: Dent|prostho
    3. Mental Health and Rehabilitation: mental|psch|rehab|counsel 
    4. Pharmacies: Pharma 
    5. Eye and Ear Care: Hear|eye|opt|Audio|Ophthal 
    6. Preventive Care: Preventive 
    7. Women & Reproductive Care: Gynec
    8. Radiology: Radio|Image|Diagnos|Lab|Pathology
    9. chil|pedia: Pediatrician
    10.chiro:Chiropractitioner
    11.home:Homecare Service
    12.derma: Dermatologist
    13.General medical facility: nursing facilities|general hospitals|family|community|welfare
    14.Specialised Internal Medical Care: Internal 
    15.Podiatrist: Podiatrist
    16.Orthopaedics: Prosthetics|Ortho
    17.Anesthesia Specialist: Anesthesiology
    18.Physical Therapists: Physical Therapy|Acup|Therapist
    19.Allergy: Allergy|Immun
    20.Medical Equipments and Devices: Equipment|Supplies
    21.Foster care: Foster
    22.Emergency and Ambulance: Ambulance|Emergency|urgent
    23.Local Education Agency: Education
    24.Renal Disease Treatment: renal
    25.Otolaryngology
    26.Assisted Living Facility:assisted
    27.Center Ambulatory Surgical:ambulatory
    28.Center Federally Qualified Health Center: federal
    29.urology: urology
   
    STEP 2: Look for categories that match each of these keywords"""    
    
    
    categories = hospital_data[["Category"]].drop_duplicates()
    
    keywords = ["surge", r"^Dent|prostho", "mental|psych|rehab|counsel","Pharma",\
            "Hear|eye|opt|Audio|Ophthal", "Preventive", "Gynec",\
                "Radio|Image|Diagnos|lab|pathology", "chil|pedia", "chiro", "home",\
                    "derma", "nursing facility|General|family|community|welfare|nursing",\
                        "internal", "Podiatrist", "Prosthetics|Ortho",\
                            "Anesthesiology", "Physical Therapy|Acup|Therapist",\
                                "Allergy|Immun", "Equipment|Supplies",\
                                    "Foster", "Ambulance|Emergency|Urgent", "Education",\
                                        "Renal", "Otolaryngology", "assisted", "ambulatory",\
                                            "federal", r"^urology"]
    mapping = {}
    
    
    
    for k in keywords:
        for i in categories["Category"]:
            if re.search(k, i, flags = re.IGNORECASE) != None:
                print(k + ' : ' + i)
                if i in mapping.keys() and k not in mapping[i]:
                    mapping[i].append(k)
                if i not in mapping.keys():
                    mapping[i] = [k]

    # Final categories visible to users
    final_cat = {'surge' : 'Surgery',  r"^Dent|prostho" : 'Dental Care',\
            'mental|psych|rehab|counsel' : 'Mental Health and Rehabilitation',\
                'Pharma':'Pharmacy','Hear|eye|opt|Audio|Ophthal': 'Eye and Ear Care',\
                    'Preventive': 'Preventive Care', \
                        'Gynec': 'Women & Reproductive Care',\
                            'Radio|Image|Diagnos|lab|pathology': 'Radiology', 'chil|pedia':'Pediatrician',\
                                'chiro':'Chiropractitioner', 'home':'Homecare Service',\
                                    'derma':'Dermatologist',
                                    'nursing facility|General|family|community|welfare|nursing':'General medical facility',\
                                        'internal':'Specialised Internal Medical Care',\
                                            'Podiatrist':'Podiatrist','Prosthetics|Ortho':'Orthopaedics',\
                                                'Anesthesiology':'Anesthesia Specialist',\
                                                    'Physical Therapy|Acup|Therapist':'Physical Therapy',\
                                                        'Allergy|Immun':'Allergy',\
                                                            'Equipment|Supplies':'Equipment and Supplies',\
                                                                'Foster':'Foster Care',\
                                                                    'Ambulance|Emergency|Urgent':'Ambulance and Emergency Service',\
                                                                        'Education':'Local Education Agency',\
                                                                            'Renal':'Renal Disease Treatment',\
                                                                                'Otolaryngology':'Otolaryngology',\
                                                                                    'assisted':'Assisted Living Facility',\
                                                                                        'ambulatory':'Center Ambulatory Surgical',\
                                                                                            'federal':'Center Federally Qualified Health Center',\
                                                                                                r'^urology':'urology'}
        
    
    for i in mapping.keys():
        a = hospital_data["Category"] == i
        hospital_data.loc[a,"Keywords"] = ",".join([final_cat[mapping[i][j]] \
                                                    for j in range(len(mapping[i]))])
    
            
    hospital_data["Keywords_1"] = hospital_data["Keywords"].str.split(',', expand=True)[0]
    hospital_data["Keywords_2"] = hospital_data["Keywords"].str.split(',', expand=True)[1]
    hospital_data.to_csv('hospital_list_with_keywords.csv', index = False)

   

if __name__ == "__main__":
    hospital_list()




