#Import necessary packages
import pandas as pd
import json
import urllib as url
import matplotlib.pyplot as plt
import requests
import os
import shutil

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


print(gdp_data.head())

gdp_data.iloc[200::].plot(x='date', y = 'GDP')


plt.xlabel("Year")

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
    
      
    
    def collect_from_api(self):
        open_URL = url.request.urlopen(self.link)
        byte_data = open_URL.read()
        string_data = byte_data.decode('utf-8') 
        self.json_data = json.loads(string_data)
        
    def json_to_dataframe(self, series_name):
        #clean up observations
        data_location = list((self.jsondata['dataSets'][0]['observations']).values())
        clean_data = [i[0] for i in data_location]
        
        #clean up dates
        date_location = (self.jsondata['structure']['dimensions']['observation'][-1]['values'])
        clean_dates = [i['name'] for i in date_location]
        #changing format from 2018-Q3 to SQ18
        clean_dates = [i[0] + 'Q' + i[-2::] for i in clean_dates]
        
        #combine both lists to dataframe
        joined_dict = {'Quarter': clean_dates, series_name: clean_data}
        self.df = pd.DataFrame.from_dict(joined_dict)
        
    def graph_data(self, series_name, title):
        AUS_Economic_Indicators.plot(x = 'Quarter', y = series_name, title =series_name)
        
        
        
           
    
    
    









class CPI:
    
    def __init__(self, startPeriod, endPeriod):
        self.startPeriod = startPeriod
        self.endPeriod = endPeriod
        self.link = ("http://stat.data.abs.gov.au/sdmx-json/data/CPI/3.1.10001.10.Q/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod=" + self.startPeriod + "&endPeriod=" + self.endPeriod)
    
    def source_data_from_api(self):
        openurl = url.request.urlopen(self.link)
        dirty_data = openurl.read()
        dirty_data_string = dirty_data.decode('utf-8')
        self.jsondata= json.loads(dirty_data_string)
        return self.jsondata
    
    def json_to_dataframe(self):
        obs = list((self.jsondata['dataSets'][0]['observations']).values())
        clean_data = [i[0] for i in obs]
        dirty_dates = ((self.jsondata['structure']['dimensions']['observation']))
        dirty_dates = dirty_dates[-1]['values']
        clean_dates = [i['name'] for i in dirty_dates]
        clean_dates = [i[0] + 'Q' + i[-2::] for i in clean_dates]
        joined_dict = {'Quarter': clean_dates, 'Year-on-year CPI': clean_data}
        self.df = pd.DataFrame.from_dict(joined_dict)
    
    def graph_data(self):
        Graph = CPI.plot(x = 'Quarter', y = 'Year-on-year CPI',
                         title = 'AUS Inflation')
        plt.ylabel("Year on year inflation")
        
inflation_object = CPI('2018-Q3', '2020-Q3')
inflation_object.source_data_from_api()
inflation_object.json_to_dataframe()


class UnemploymentRate:
    
    def __init__(self, startPeriod, endPeriod):
        self.startPeriod = startPeriod
        self.endPeriod = endPeriod
        self.link = ("http://stat.data.abs.gov.au/sdmx-json/data/LF/0.14.3.1599.10.M/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod="+self.startPeriod+"&endPeriod="+self.endPeriod)
    
    def source_data_from_api(self):
        openurl = url.request.urlopen(self.link)
        dirty_data = openurl.read()
        dirty_data_string = dirty_data.decode('utf-8')
        self.jsondata= json.loads(dirty_data_string)
        return self.jsondata
    
    def json_to_dataframe(self):
        obs = list((self.jsondata['dataSets'][0]['observations']).values())
        clean_data = [i[0] for i in obs]
        dirty_dates = ((self.jsondata['structure']['dimensions']['observation']))
        dirty_dates = dirty_dates[-1]['values']
        clean_dates = [i['name'] for i in dirty_dates]
        clean_dates = [i[0] + 'Q' + i[-2::] for i in clean_dates]
        joined_dict = {'Quarter': clean_dates, 'Year-on-year CPI': clean_data}
        self.df = pd.DataFrame.from_dict(joined_dict)         




###LABOUR FORCE



UR_link = ("http://stat.data.abs.gov.au/sdmx-json/data/LF/0.14.3.1599.10.M/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod=2020-08&endPeriod=2020-11")


UR_webpg = url.request.urlopen(UR_link)
UR_dirty_data = UR_webpg.read()
UR_dirty_data_string = UR_dirty_data.decode('utf-8')
UR_json_ob = json.loads(UR_dirty_data_string)

UR_obs = list((UR_json_ob['dataSets'][0]['observations']).values())
UR_clean_data = [i[0] for i in UR_obs]






