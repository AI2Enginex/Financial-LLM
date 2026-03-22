from GetData.statements_processor import FinancialStatementProcessor
from GetData.financial_data import FetchFinancialData
from LLMUtils.VectoreStore import Vectors


class FinancialPipeline:

    def __init__(self, company_name):
        self.company_name = company_name
        self.financial_statements = []
        self.financial_ratios = {}
        self.documents = []

    def fetch_data(self):
        try:
            finance_data = FetchFinancialData(company_name=self.company_name)

            self.financial_statements = finance_data.get_financial_statements() or []
            self.financial_ratios = finance_data.get_financial_ratios() or {}

        except Exception as e:
            print(f"Error fetching financial data: {e}")
            self.financial_statements = []
            self.financial_ratios = {}

    def process_documents(self, start: str, end: str, ma_days: int):
        try:
            processor = FinancialStatementProcessor(
                self.company_name,
                self.financial_statements,
                self.financial_ratios
            )

            self.documents = processor.convert_all(
                start=start,
                end=end,
                ma_days=ma_days
            )

        except Exception as e:
            print(f"Error processing documents: {e}")
            self.documents = []

    def run(self, start: str, end: str, ma_days: int):
        try:
            self.fetch_data()
            self.process_documents(start=start, end=end, ma_days=ma_days)
            return self.documents

        except Exception as e:
            print(f"Pipeline failed: {e}")
            return []
        

class GenerateVectorsEmbeddings(FinancialPipeline):

    def __init__(self, company_name: str,startdate: str,enddate: str,movingaverage: int, config=None):

        self.config = config
        self.startdate = startdate
        self.enddate = enddate
        self.movingaverage = movingaverage
        super().__init__(company_name)

    def read_combined_data(self):

        try:

            pipeline = FinancialPipeline(company_name=self.company_name)

            final_documents = pipeline.run(
               
                start=self.startdate,
                end=self.enddate,
                ma_days=self.movingaverage
                )

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

    from LLMUtils.LLMConfigs import GeminiConfig, api_key
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

    g = GenerateVectorsEmbeddings(company_name='TCS',startdate='2025-01-01',enddate='2026-01-01',movingaverage=10,config=config)
    data = g.create_text_vectors()
    print(data)