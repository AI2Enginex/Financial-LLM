import yfinance as yf


class FinancialRatios:

    def __init__(self, ticker_name: str):

        self.stock = yf.Ticker(ticker_name)
        self.info = self.stock.info
        
    def get_indian_stock_ratios(self):

        try:
            ratios = {}

            # ---------- Market Metrics ----------
            ratios["Market Cap"] = self.info.get("marketCap")
            ratios["Current Price"] = self.info.get("currentPrice")
            ratios["52W High"] = self.info.get("fiftyTwoWeekHigh")
            ratios["52W Low"] = self.info.get("fiftyTwoWeekLow")

            # ---------- Valuation ----------
            ratios["PE Ratio"] = self.info.get("trailingPE")
            ratios["Forward PE"] = self.info.get("forwardPE")
            ratios["Price to Book"] = self.info.get("priceToBook")

            # ---------- Profitability ----------
            ratios["ROE"] = self.info.get("returnOnEquity")
            ratios["ROA"] = self.info.get("returnOnAssets")
            ratios["Operating Margin"] = self.info.get("operatingMargins")
            ratios["Net Profit Margin"] = self.info.get("profitMargins")

            # ---------- Liquidity ----------
            ratios["Current Ratio"] = self.info.get("currentRatio")
            ratios["Quick Ratio"] = self.info.get("quickRatio")

            # ---------- Leverage ----------
            ratios["Debt to Equity"] = self.info.get("debtToEquity")

            # ---------- Cash Flow ----------
            ratios["Operating Cash Flow"] = self.info.get("operatingCashflow")
            ratios["Free Cash Flow"] = self.info.get("freeCashflow")

            # ---------- Growth ----------
            ratios["Revenue Growth"] = self.info.get("revenueGrowth")
            ratios["Earnings Growth"] = self.info.get("earningsGrowth")

            # ---------- Dividend ----------
            ratios["Dividend Yield"] = self.info.get("dividendYield")

            return {

                "statement": 'ratios',
                "data": ratios
            }
        
        except Exception as e:
            return e

# Example: Indian stock

if __name__ == "__main__":

    finance = FinancialRatios(ticker_name="TCS" + ".NS")
    data = finance.get_indian_stock_ratios()
    print(data)