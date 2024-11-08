import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import datetime as dt




class Scraper:
    def __init__(self, URL = "https://fiis.com.br/rendimentos/?ticker="):
        self.URL = URL

    def initialize(self):
        self.dr = webdriver.Chrome()
        self.dr.implicitly_wait(3)
        self.dr.get(self.URL)
        self.content = BeautifulSoup(self.dr.page_source, "lxml")
        self.dr.quit()

    def scrape_data(self):
        FII_list = self.content.findAll("div",attrs={"class":"accordion-body"})
        new_FII_list = []

        for FII in FII_list:
            table = FII.findAll("div", attrs={"class":"yieldChart__table__bloco yieldChart__table__bloco--rendimento"})
            for row in table:
                FII_name = FII['data-accordion-body']
                temp_dict = {"Nome" : FII_name}
                
                FII_row_data = row.findAll("div", attrs={"class":"table__linha"})
                
                temp_dict["Data"] = FII_row_data[1].text.strip()
                temp_dict["Pagamento"] = FII_row_data[2].text.strip()
                temp_dict["Cotação"] = FII_row_data[3].text.strip()
                temp_dict["Yield"] = FII_row_data[4].text.strip()
                temp_dict["Rendimento"] = FII_row_data[5].text.strip()

                new_FII_list.append(temp_dict)

        output = pd.DataFrame.from_dict(new_FII_list)
        output.to_csv("raw.csv")

    def treat_data(self):
        df = pd.read_csv("raw.csv", index_col=0)

        fixed_format = {'\\%' : '',
                        'R\\$' : '',
                        '\\.' : '',
                        ',' : '.',
                        ' ' : ''}


        df = df.replace({"Cotação" : fixed_format, 
                "Yield": fixed_format,
                "Rendimento" : fixed_format}, 
                regex =True)
        
        df["Cotação"] = df["Cotação"].apply(pd.to_numeric)
        df["Yield"] = df["Yield"].apply(pd.to_numeric)
        df["Rendimento"] = df["Rendimento"].apply(pd.to_numeric)

        df["Data"] = pd.to_datetime(df["Data"],format="%d.%m.%Y")
        df["Pagamento"] = pd.to_datetime(df["Pagamento"],format="%d.%m.%Y",errors='coerce')

        df.to_csv("treated.csv")

    def get_performance(self, name):
        df = pd.read_csv("treated.csv", index_col=0)
        return df[df["Nome"]==name]["Rendimento"].tolist()
        

