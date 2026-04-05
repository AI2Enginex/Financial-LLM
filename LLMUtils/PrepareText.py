from GetData.statements_processor import FinancialStatementProcesser
from GetData.financial_data import FetchFinancialData
from LLMUtils.VectoreStore import Vectors
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv


load_dotenv()
index_name = os.getenv("INDEX_NAME")
pinecone_api = os.getenv("PINECONE_API")

def create_timeframe():

    try:
        enddate = datetime.today()
        startdate = enddate - relativedelta(years=1)

        startdate_str = startdate.strftime('%Y-%m-%d')
        enddate_str = enddate.strftime('%Y-%m-%d')

        return startdate_str, enddate_str

    except Exception as e:
        return e
    


# Class for Fetching and Processing all the Statements and Technicals
class FinancialPipeline:

    def __init__(self, company_name):
        self.company_name = company_name
        self.financial_statements = []
        self.financial_ratios = {}
        self.documents = []
    
    # Method to fecth and process the Financial Statements
    def fetch_data(self):
        try:
            finance_data = FetchFinancialData(company_name=self.company_name)

            self.financial_statements = finance_data.get_financial_statements() or []
            self.financial_ratios = finance_data.get_financial_ratios() or {}

        except Exception as e:
            print(f"Error fetching financial data: {e}")
            self.financial_statements = []
            self.financial_ratios = {}
    
    # Method to combine all the Statements and Technicals into a one single Document.
    def process_documents(self, start: str, end: str, ma_days: int):
        try:
            processor = FinancialStatementProcesser(
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
    
    # Method to return processed documents
    def run(self, start: str, end: str, ma_days: int):
        try:
            self.fetch_data()
            self.process_documents(start=start, end=end, ma_days=ma_days)
            return self.documents

        except Exception as e:
            print(f"Pipeline failed: {e}")
            return []
        

# Class for Generating the Embeddings for the Combined Documents and storing them on the Pinecone Index
class GenerateVectorsEmbeddings(FinancialPipeline):

    def __init__(self, company_name: str,startdate: str,enddate: str,movingaverage: int, config=None):

        self.config = config
        self.startdate = startdate
        self.enddate = enddate
        self.movingaverage = movingaverage
        super().__init__(company_name)
    
    # Fetch the Combined data
    def read_combined_data(self):

        try:

            pipeline = FinancialPipeline(company_name=self.company_name)

            final_documents = pipeline.run(
               
                start=self.startdate,
                end=self.enddate,
                ma_days=self.movingaverage
                )
            
            print("final documents :", final_documents)
            return final_documents

        except Exception as e:
            print(f"Fatal error: {e}")

    # Method to generate embeddings and upsert them to the pinecone index
    def create_text_vectors(self,id: int, batch: int):

        Vectors.initialize(config=self.config)

        vectors = Vectors.generate_vectors_from_documents(
            chunks=self.read_combined_data(),user_id=id, batch_size=batch, ticker=self.company_name
        )

        if vectors:
            print("Vector store successfully created")
        else:
            print("Vector store creation failed.")

        return vectors

# Responsible for ingesting data into The VectoreStore and retrieving data from the Pinecone index.
class PineconeManager:


    def __init__(self, config=None):


        try:
            self.pc = Pinecone(api_key=pinecone_api)
            self.index_name = index_name
            self.index = self.pc.Index(index_name)
            self.config = config
            self.embedding_model = Vectors.initialize(config=self.config)

        except Exception as e:
            print(f"[Pinecone] Init error: {e}")
    
    # loading the Pinecone VectorStore
    def load_vector_store(self):

        try:
            return PineconeVectorStore(
                index=self.index,
                embedding=self.embedding_model,
                namespace="__default__"
            )
        except Exception as e:
            print(f"[Pinecone] Error loading vector store: {e}")
            return None
        
    # Method to read the current Date
    def _get_today(self):
        return datetime.today().strftime('%Y-%m-%d')

    # Method for building a query vector
    def _build_query_vector(self, ticker: str):
        return self.embedding_model.embed_query(f"{ticker}")

    # Method for Validating the data Freshness. New Values are Scraped
    # after a week from the last Scraped Date.
    def _check_data_freshness(self, user_id: int, ticker: str):

        try:

            today = self._get_today()
            today = datetime.strptime(today, "%Y-%m-%d").date()

            results = self.index.query(
                vector=self._build_query_vector(ticker),
                top_k=3,
                include_metadata=True,
                filter={
                    "user_id": str(user_id),
                    "ticker": ticker
                }
            )

            if not results.get("matches"):
                return False  # no data → must ingest

            for match in results["matches"]:
                last_date_str = match["metadata"].get("last_scraped_date")

                if last_date_str:
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()

                    # check 7-day condition
                    days_diff = (today - last_date).days
                    print("Days Remaining : ",days_diff)
                    if days_diff < 7:
                        return True  # still valid

            return False  # stale → ingest


        except Exception as e:
            print(f"[Freshness Check Error]: {e}")
            return False
    
    # Method to ingest data into the pinecone vectorstore 
    def _ingest_data(self, ticker: str, user_id: int, batchsize: int):
        start, end = create_timeframe()

        print(f"Start Date : {start} and End Date : {end}")

        g = GenerateVectorsEmbeddings(
            company_name=ticker,
            startdate=start,
            enddate=end,
            movingaverage=10,
            config=self.config
        )

        g.create_text_vectors(id=user_id, batch=batchsize)

    # Method for Returning the retriever. Filtered with intended user id and ticker
    def _get_retriever(self, vector_store, user_id: int, ticker: str, k: int):
        return vector_store.as_retriever(
            search_kwargs={
                "k": k,
                "filter": {
                    "user_id": str(user_id),
                    "ticker": ticker
                }
            }
        )

    # Main method to Fetch the Embeddings from the Vectorstore.
    # Always Ingest first if the Conditions do not satisfy else Retrieve
    def fetch_embeddings(self, ticker_name: str, userid: int, batchsize: int, k: int):

        try:
            vector_store = self.load_vector_store()

            is_fresh = self._check_data_freshness(userid, ticker_name)

            print("status : ", is_fresh)
            print("today : ", self._get_today())

            if is_fresh:
                print("Using existing data")
                return self._get_retriever(vector_store, userid, ticker_name, k)

            print("Ingesting new data...")

            self._ingest_data(ticker_name, userid, batchsize)

            return self._get_retriever(vector_store, userid, ticker_name, k)

        except Exception as e:
            print(f"Error retrieving the Embeddings {e}")
            return e



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

    g = PineconeManager(config=config)
    data = g.fetch_embeddings(ticker_name='RELIANCE',userid=20, batchsize=10,k=1000)
    print(data)