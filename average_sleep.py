"""
Objective: This program shows the user that given his/her income, how different he/she is from 
           the average sleeping hours
           

Dataset used: sleep_data.csv
Dataset source: American Time Use Survey of 2020 (https://www.bls.gov/tus/datafiles-2020.htm)

Dataset description: The user survey provides nationally representative estimates of how, where, 
and with whom Americans spend their time. It is the only federal survey providing data on the 
full range of non-market activities, from childcare to volunteering.

Packages required:
    a. pandas 
    b. seaborn
    c. matplotlib

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def sleep_compare():
    #Importing the dataset (must exist in directory)
    full_list = pd.read_csv('sleep_data.csv')
    full_list['sleep_hrs'] = full_list['t010101']/60    #t010101 is the variable for sleep time in mins
    
    #User input
    
    #Age
    check_1 = 0
    while check_1 ==0:
        try:
            user_age = int(input('Enter your age: '))
            if not 5 <= user_age <= 70:
                print('Please choose an integer age between 5 and 70')
            else:
                check_1 =1
        except:
            print('Please choose an integer age between 5 and 70')
    
    #Gender
    check_2 = 0
    while check_2 ==0:
        try:
            user_gender = int(input('Enter your gender (1 for male and 2 for female): '))
            if user_gender not in [1,2]:
                print('Please choose 1 or 2')
            else:
                check_2 =1
        except:
            print('Please choose 1 or 2')
    
    #Income
    check_3 = 0
    while check_3 ==0:
        try:
            user_income = int(input('Enter your annual income (enter 0 if not working): '))
            if not 0 <= user_income <= 280000:
                print('Please choose an integer income between 0 and 280000')
            else:
                check_3 =1
        except:
            print('Please choose an integer income between 0 and 280000')
    
    #Sleep hours
    check_4 = 0
    while check_4 ==0:
        try:
            user_sleep = int(input('Enter your average daily sleeping time (in hours): '))
            if not 0 <= user_sleep <= 20:
                print('Please choose an integer sleep hrs between 0 and 20')
            else:
                check_4 =1
        except:
            print('Please choose an integer sleep hours between 0 and 20')
    
    
    #Filtering the dataframe for regression plot
    
    #Same gender as user
    filtered_list = full_list.loc[full_list['TESEX'] == user_gender]
    
    #Age range of +-5 user's age
    filtered_list = filtered_list.loc[filtered_list['TEAGE'] <= user_age + 5]
    filtered_list = filtered_list.loc[full_list['TEAGE'] >=user_age - 5 ]
    
    #Mean sleep
    mean_sleep = filtered_list['sleep_hrs'].mean()
    
    if user_income == 0:
        working =0
    if user_income >0:
        working =1
    
    #Keeping data points of the same employment status as user
    #Employment variable in the dataset is TRERNWA
    
    if working==1:
        filtered_list = filtered_list.loc[filtered_list['TRERNWA'] !=-1]                                                   
    if working==0:
        filtered_list = filtered_list.loc[filtered_list['TRERNWA'] ==-1]                                                   
    
    
    
    def plotter():
        plt.title('Average Income X Sleep')

        plt.scatter([user_income],[user_sleep], color= 'red')
    
        sns.regplot(x = filtered_list['TRERNWA'],y = filtered_list['sleep_hrs'] ,data = filtered_list, 
                    scatter=False)
        plt.xlabel('Annual income')
        plt.ylabel('Sleep hours')

        plt.savefig('sleep_hours_comparison.pdf')
        
        plt.show()

    if working ==1:    
        plotter()
    if working ==0:
        print('{} {}   {} {}'.format('your sleep:',user_sleep,'average sleep:',mean_sleep))
        
        
        
        
        
        