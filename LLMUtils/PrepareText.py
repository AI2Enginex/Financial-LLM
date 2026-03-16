from GetData.financial_data import FetchFinancialData
from LLMUtils.VectoreStore import Vectors

from langchain_core.documents import Document

class FinancialDocumentProcessor:

    def __init__(self, company_name, financial_statements, financial_ratios):
        self.company_name = company_name
        self.financial_statements = financial_statements
        self.financial_ratios = financial_ratios


    def convert_statements(self):
        documents = []

        try:
            for statement in self.financial_statements:

                statement_name = statement.get("statement", "Unknown Statement")
                data = statement.get("Data", {})

                for period, values in data.items():

                    text = f"{statement_name} for {period}: "

                    for key, value in values.items():
                        text += f"{key}: {value} "

                    doc = Document(
                        page_content=text.strip(),
                        metadata={
                            "company": self.company_name,
                            "statement": statement_name,
                            "period": period
                        }
                    )

                    documents.append(doc)

        except Exception as e:
            print(f"Error processing financial statements: {e}")

        return documents


    def convert_ratios(self):
        documents = []

        try:
            ratio_data = self.financial_ratios.get("data", {})

            for ratio_name, value in ratio_data.items():

                text = f"{ratio_name} for {self.company_name}: {value}"

                doc = Document(
                    page_content=text,
                    metadata={
                        "company": self.company_name,
                        "statement": "Financial Ratio",
                        "ratio": ratio_name
                    }
                )

                documents.append(doc)

        except Exception as e:
            print(f"Error processing financial ratios: {e}")

        return documents


    def convert_all(self):

        try:
            statement_docs = self.convert_statements()
            ratio_docs = self.convert_ratios()

            return statement_docs + ratio_docs

        except Exception as e:
            print(f"Error combining documents: {e}")
            return []
    
class FinancialPipeline:

    def __init__(self, company_name):
        self.company_name = company_name
        self.financial_statements = None
        self.financial_ratios = None
        self.documents = None


    def fetch_data(self):

        try:
            finance_data = FetchFinancialData(company_name=self.company_name)

            self.financial_statements = finance_data.get_financial_statements()
            self.financial_ratios = finance_data.get_financial_ratios()

        except Exception as e:
            print(f"Error fetching financial data: {e}")
            self.financial_statements = []
            self.financial_ratios = {}


    def process_documents(self):

        try:
            processor = FinancialDocumentProcessor(
                self.company_name,
                self.financial_statements,
                self.financial_ratios
            )

            self.documents = processor.convert_all()

        except Exception as e:
            print(f"Error processing documents: {e}")
            self.documents = []


    def run(self):

        try:
            self.fetch_data()
            self.process_documents()
            return self.documents

        except Exception as e:
            print(f"Pipeline failed: {e}")
            return []
        


class GenerateVectorsEmbeddings(FinancialPipeline):

    def __init__(self, company_name, config=None):

        self.config = config
        super().__init__(company_name)

    def read_combined_data(self):

        try:

            pipeline = FinancialPipeline(company_name=self.company_name)

            final_documents = pipeline.run()

            return final_documents

        except Exception as e:
            print(f"Fatal error: {e}")


    def create_text_vectors(self):

        Vectors.initialize(config=self.config)

        vectors = Vectors.generate_vectors_from_documents(
            chunks=self.read_combined_data()
        )

        if vectors:
            print("Vector store successfully created")
        else:
            print("Vector store creation failed.")

        return vectors


if __name__ == "__main__":

    from LLMUtils.LLMConfigs import ChatGoogleGENAI, GeminiConfig, api_key
    config = GeminiConfig(
        chat_model_name="gemini-3-flash-preview",
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
        temperature=0,
        top_p=0.8,
        top_k=32,
        max_output_tokens=3000,
        generation_max_tokens=8192,
        api_key=api_key
    )

    g = GenerateVectorsEmbeddings(company_name='TCS',config=config)
    data = g.create_text_vectors()
    print(data)