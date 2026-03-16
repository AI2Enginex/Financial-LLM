import yfinance as yf
from langchain_core.documents import Document
from datetime import datetime

def get_date_time(value: str):

    try:
        published_dt = datetime.fromisoformat(value.replace("Z", "+00:00"))

        date = published_dt.date()
        time = published_dt.time()

        return str(date), str(time)
    
    except Exception as e:
        return e

class FetchNews:

    def __init__(self, ticker: str):

        self.ticker=ticker

    def fetch_news(self):
        """
        Fetch news metadata from Yahoo Finance
        """
        try:
            ticker = yf.Ticker(self.ticker)
            news = ticker.news

            if not news:
                return []

            return news

        except Exception as e:
            print(f"Error fetching Yahoo Finance news: {e}")
            return []

        
class YahooFinanceNewsScraper(FetchNews):

    def __init__(self, ticker):
        super().__init__(ticker)
       

    def get_news_documents(self):

        documents = []

        news_list = self.fetch_news()

        for news in news_list:

            try:

                content = news.get("content", {})

                title = content.get("title")
                summary = content.get("summary")
                publisher = content.get("provider", {}).get("displayName")
                url = content.get("canonicalUrl", {}).get("url")
                published = content.get("pubDate")

                date, time = get_date_time(value=published)

                if not summary:
                    continue

                page_content = f"""
                                    Title: {title}, Summary: {summary}
                                    """

                doc = Document(
                    page_content=page_content.strip(),
                    metadata={
                        "source": url,
                        "publisher": publisher,
                        "ticker": self.ticker,
                        "date": date,
                        "time": time,
                        "type": "news"
                    }
                )

                documents.append(doc)
            except Exception as e:
                print(f"Error processing article: {e}")
        return documents
    
if __name__ == "__main__":

    news_scraper = YahooFinanceNewsScraper("INFY" + ".NS")

    news_documents = news_scraper.get_news_documents()

    print(news_documents)

    print(len(news_documents))