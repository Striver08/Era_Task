import requests
from bs4 import BeautifulSoup
import json
import click
import lxml

@click.group()
def cli():

    '''
#        -------------------------------------------------------------------------
#        It is a Command line tool which gives details of the user after entering 
#        their Driving License No. and their respective date of birth
#        -------------------------------------------------------------------------
#    '''
#    pass




#num = str(input("Enter your license no."))
#dob = str(input("Enter your date of birth (dd-mm-yyyy)"))


@cli.command()
@click.option('--num', prompt = 'Enter your license no.', help  = 'Enter your license no. here')
@click.option('--dob', prompt = 'Enter your date of birth(dd-mm-yyyy)', help = 'Enter your date of birth here')
def info(num,dob):
    '''
        --------------------------------------------------------------------      
        This is a CLI application which gives details of a user 
        when their respective DL no. and DOB is entered
        --------------------------------------------------------------------
    '''
    if num.islower():       #This is the function to check whether the DL no. is in uppercase or not,
        num = num.upper()   #if it is not then it converts to uppercase.

    if " " not in num:
        num =  num[:-11] + " " +num[-11:]       #This function adds space after the Alphanumeric code so that proper input is added.
        click.echo(num)                         #example- UP1420200016154 --> UP14 20200016154


    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    form_data = {
        'javax.faces.partial.ajax': 'true',     #This is the form data which is to be input
        'javax.faces.source': 'form_rcdl:j_idt46',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
        'form_rcdl:j_idt46': 'form_rcdl:j_idt46',
        'form_rcdl': 'form_rcdl',
        'form_rcdl:tf_dlNO': num,   #The "num" & "dob" are the two variables which are taken as input from the user.
        'form_rcdl:tf_dob_input': dob
        
    }

    with requests.Session() as s:
        url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
        r = s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, features= 'lxml')
        form_data['javax.faces.ViewState'] = soup.find('input', attrs = {'name': 'javax.faces.ViewState'})['value'] #This find the value of "javax.faces.Viewstate" from the html code as it changes everytime we refreshes the page.
        #print(soup)
        r = s.post(url, data = form_data, headers = headers)
        soup1 = BeautifulSoup(r.content, features= 'lxml')
        #print(soup1)

        table = soup1.find('table', attrs = {"class": 'table'}) #Scraping the details from 1st table and storing as in variable "table"
        #print(table.text)
        table1 = soup1.find('table',attrs = { "class" : "data-table"})  #Scraping the details from 2nd table and storing as in variable "table1"
        #print(table1.text)
        table2 = soup1.find('table', attrs = {'role':'grid'})   #Scraping the details from 3rd table and storing as in variable "table3"
        #print(table2.text)

    dictionary = {}
    arr = []

    try:                                            #This is exception handling, 
        for info in table.findAll('td'):            #If the details are given wrong, 
            #print(info.text)                       #then definitely the content in the variable table,table1 and table2 would be Null
            arr.append(info.text)                   #Therefore, it won't be appended in the array and hence it will give the error
        for i in range(0,len(arr),2):               #That's why exception handling is used.
            for j in arr:
                dictionary[arr[i]] = arr[i+1]  
        arr.clear()
        for info in table1.findAll('td'):           #Here,The text is appended in the array and then added to dictionary for all the 3 tables.
            #print(info.text)
            arr.append(info.text)
        for i in range(0,len(arr),3):
            for j in arr:
                dictionary[arr[i]] = [arr[i+1], arr[i+2]]
        arr.clear()        
        for info in table2.findAll('td'):
            #print(info.text)
            arr.append(info.text)
        for i in range(0,len(arr),3):
            for j in arr:
                dictionary[arr[i]] = [arr[i+1], arr[i+2]]
    except:
        print("Make sure DL no. and DOB are correct")       #If error occurs, It prints this message.
        
    with open('data.json', 'w+') as file:       #The dictionary is exported to the JSON file.
        json.dump(dictionary,file)

    with open('data.json', 'r+') as file:        #The dictionary is imported from the JSON file.
        data = json.load(file)

    print(data)

def get_captcha():
    pass

if __name__ == '__main__':
    info()

