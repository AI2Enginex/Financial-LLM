from GetData.technicals import compute_all_technicals
from langchain_core.documents import Document



# Class for Loading Necessary Variables
class FinancialStatementVariables:

    def __init__(self, company_name, financial_statements, financial_ratios):
        self.company_name = company_name
        self.financial_statements = financial_statements or []
        self.financial_ratios = financial_ratios or {}



# Class for Reading all the Financial Statements and Returns a List of Documents
class ProcessFinancialStatements(FinancialStatementVariables):

    def __init__(self, company_name, financial_statements, financial_ratios):
        super().__init__(company_name, financial_statements, financial_ratios)

    # Function to convert the Financial Statements
    # Data into strings to be passed to the LLM 
    def convert_statements(self):
        
        documents = list()

        try:
            for statement in self.financial_statements:

                statement_name = statement.get("statement", "Unknown Statement")
                data = statement.get("Data", {})

                for period, values in data.items():

                    content = " ".join(
                        f"{key}: {value}" for key, value in values.items()
                    )

                    text = f"{statement_name} for {period}: {content}"  # creating the page_content
                    doc_id = f"{self.company_name}_{statement_name}_{period}".lower().replace(" ", "_")
                    # creating a list of Documents for Financial Statements
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "id": doc_id,
                                "type": "financial_statement",
                                "statement": statement_name,
                                "period": period
                            }
                        )
                    )

        except Exception as e:
            print(f"Error processing financial statements: {e}")

        return documents
    
# Class for Reading all the Financial Ratios and Returns a List of Documents
class ProcessFinancialRatios(ProcessFinancialStatements):

    def __init__(self, company_name, financial_statements, financial_ratios):
        super().__init__(company_name, financial_statements, financial_ratios)


    # Function to convert all the Financial Ratios 
    # into a string to be passed to the LLM
    def convert_ratios(self):
        documents = self.convert_statements()

        try:
            ratio_data = self.financial_ratios.get("data", {})

            for ratio_name, value in ratio_data.items():

                text = f"{ratio_name} for {self.company_name}: {value}" # Generating the string for page_content
                doc_id = f"{self.company_name}_{ratio_name}".lower().replace(" ", "_")
                # appending the text into a list of document for financial ratios
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "id": doc_id,
                            "type": "financial_ratio",
                            
                            "ratio": ratio_name
                        }
                    )
                )

        except Exception as e:
            print(f"Error processing financial ratios: {e}")

        return documents

# Class for Combining the Financial Statements and Technicals. Returns a List of Documents
class FinancialStatementProcesser(ProcessFinancialRatios):

    def __init__(self, company_name, financial_statements, financial_ratios):
        super().__init__(company_name, financial_statements, financial_ratios)

    # Combining all the Technical Data into one single List of Documents
    def convert_all(self, start: str, end: str, ma_days: int):
        try:
            
            processed_docs = self.convert_ratios()
            
            # Computing the technical analysis values
            technical_docs = compute_all_technicals(
                ticker=self.company_name,
                start_str=start,
                end_str=end,
                moving_average_days=ma_days
            )
            
            # Returning a single string of documents
            final_data = processed_docs + technical_docs
            

            return final_data

        except Exception as e:
            print(f"Error combining documents: {e}")
            return []
        
if __name__ == "__main__":

    pass