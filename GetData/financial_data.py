from GetData.financial_statements import FetchData

from GetData.yahoo_finance_ratios import FinancialRatios

class FetchFinancialData:
    def __init__(self, company_name: str):
        
        self.company = company_name
        # We initialize the data fetchers here, once we have the name
        self.data_provider = FetchData(company_name=self.company)
        self.ratio_calculator = FinancialRatios(ticker_name=self.company + ".NS")

    def get_financial_statements(self):
        """
        Retrieves the financial statements and returns the processed data.
        """
        try:
            
            statements = self.data_provider.main() 
            return statements
        except Exception as e:
            return f"Error retrieving data for {self.company}: {e}"
    
    def get_financial_ratios(self):
        """
        Retrieves the financial statements and returns the processed data.
        """
        try:
            
            ratios = self.ratio_calculator.get_indian_stock_ratios()
            return ratios
        except Exception as e:
            return f"Error retrieving data for {self.company}: {e}"

# Usage
if __name__ == "__main__":
    finance_data = FetchFinancialData("TCS")
    statements=finance_data.get_financial_statements()
    ratios=finance_data.get_financial_ratios()

    print("Financial Statements : ")
    print(statements)

    print("Financial Ratios : ")
    print(ratios)