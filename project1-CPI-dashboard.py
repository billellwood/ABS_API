#Import necessary packages
import pandas as pd
import json
import urllib as url
import matplotlib.pyplot as plt
import requests
import os


#GDP data is not available through API, so automating download of latest release file from website

class API_AUS_Economic_Indicators:
    def __init__(self, startPeriod, endPeriod):
        self.startPeriod = startPeriod
        self.endPeriod = endPeriod
        
    def initialise_CPI_API(self):
        self.absAPI = (("http://stat.data.abs.gov.au/sdmx-json/data/CPI/"
                        "3.1.10001.10.Q/all?detail=Full&dimensionAt"
                        "Observation=AllDimensions&startPeriod=" 
                        + self.startPeriod + "&endPeriod=" + self.endPeriod))
                       
    def initialise_LF_API(self):
        self.absAPI = (("http://stat.data.abs.gov.au/sdmx-json/data/LF/"
                        "0.14.3.1599.10.M/all?detail=Full&dimensionAt"
                        "Observation=AllDimensions&startPeriod=" 
                        + self.startPeriod + "&endPeriod=" + self.endPeriod))
    def initialise_current_account_API(self):
        self.absAPI = (("http://stat.data.abs.gov.au/sdmx-json/data/BOP"
                        "/1.100.10.Q/all?detail=Full&dimensionA"
                        "tObservation=AllDimensions&startPeriod="
                        + self.startPeriod + "&endPeriod=" + self.endPeriod))
    def initialise_GDP(self):
        my_directory = "/Users/billellwood/Desktop"
        os.chdir(my_directory)
        self.gdp_url = "https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/sep-2020/5206001_Key_Aggregates.xls"
        r = requests.get(gdp_url, allow_redirects=True)
        open('GDP_excel.xls', 'wb').write(r.content)
    
    
    def collect_from_api(self):
        open_URL = url.request.urlopen(self.absAPI)
        byte_data = open_URL.read()
        string_data = byte_data.decode('utf-8') 
        return json.loads(string_data)
        
    def json_to_dataframe(self, series_name):
        #clean up observations
        data_location = list((self.collect_from_api()['dataSets'][0]['observations']).values())
        clean_data = [i[0] for i in data_location]
        
        #clean up dates
        date_location = (self.collect_from_api()['structure']['dimensions']['observation'][-1]['values'])
        clean_dates = [i['name'] for i in date_location]
        #changing format from 2018-Q3 to SQ18
        clean_dates = [i[0] + 'Q' + i[-2::] for i in clean_dates]
        
        #combine both lists to dataframe
        joined_dict = {'Quarter': clean_dates, series_name: clean_data}
        self.df = pd.DataFrame.from_dict(joined_dict)
        
    def graph_data(self, series_name, title):
        self.df.plot(x = 'Quarter', y = series_name, title =series_name)
        pass
        
#Getting latest release into the environment and the appropriate columns of excel file
my_directory = "/Users/billellwood/Desktop"
os.chdir(my_directory)
gdp_url = "https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/sep-2020/5206001_Key_Aggregates.xls"
r = requests.get(gdp_url, allow_redirects=True)
open('GDP_excel.xls', 'wb').write(r.content)
gdp_data = pd.ExcelFile("GDP_excel.xls")
gdp_data = pd.read_excel(gdp_data, 'Data1', usecols = "BB")
gdp_data.rename( columns={"Gross domestic product: Chain volume measures ;.1":"GDP"}, inplace=True )
gdp_data = gdp_data.drop([0,1,2,3,4,5,6,7,8,9])
gdp_data['date'] = pd.date_range(start='12/1/1959', periods = len(gdp_data), freq='Q')
gdp_data.iloc[200::].plot(x='date', y = 'GDP')
plt.xlabel("Year")

cpi = API_AUS_Economic_Indicators("2005-Q1", "2020-Q2")
cpi.initialise_CPI_API()
cpi.collect_from_api()
cpi.json_to_dataframe("Australian inflation rate")
cpi.graph_data("Australian inflation rate", "Australian inflation rate")
unempl = API_AUS_Economic_Indicators("2010-Q1", "2020-Q2")
unempl.initialise_LF_API()
unempl.collect_from_api()
unempl.json_to_dataframe("Australian unemployment rate")
unempl.graph_data("Australian unemployment rate", "Australian inflation rate")
curr = API_AUS_Economic_Indicators("2010-Q1", "2020-Q2")
curr.initialise_current_account_API()
curr.collect_from_api()
curr.json_to_dataframe("Australian current account")
curr.graph_data("Australian current account", "Australian inflation rate")




