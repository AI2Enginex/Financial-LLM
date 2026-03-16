import requests
from bs4 import BeautifulSoup
import pandas as pd

class GetFinancialRatios:
    
    
    def __init__(self, comapany_name: str):

        self.url = f"https://www.screener.in/company/{comapany_name}/"
        
    def get_growth_metrics(self):

        try:
            headers = {
            "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(self.url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            metrics = {}

            ratios_section = soup.select("#top-ratios li")

            for li in ratios_section:

                name = li.find("span", class_="name")

                value = li.find("span", class_="number")

                if name and value:
                    metrics[name.text.strip()] = value.text.strip()

            return metrics
        except Exception as e:
            return e

    def get_all_financial_data(self):


        try:
            growth = self.get_growth_metrics()

            print("growth : ", growth)

            all_data = {**growth}

            return all_data
        except Exception as e:
            return e

if __name__ == "__main__":

    financial_ratios = GetFinancialRatios(comapany_name='TCS')
    data = financial_ratios.get_all_financial_data()

    df = pd.DataFrame([data])

    print(df)