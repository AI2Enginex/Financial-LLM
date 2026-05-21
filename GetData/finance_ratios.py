import yfinance as yf


class FinancialRatios:

    def __init__(self, ticker_name: str):

        self.stock = yf.Ticker(ticker_name)
        self.info = self.stock.info
        
    def get_indian_stock_ratios(self):

        try:
            ratios = {}

            # ---------- Market Metrics ----------
            # ---------- Basic Market Data ----------
            # Market Cap: Total value of the company in the stock market
            # = Share Price × Total Shares
            # Analysis:
            # - Helps classify company size (Large-cap, Mid-cap, Small-cap)
            # - Large-cap → stable, lower risk
            # - Small-cap → high growth potential but risky
            ratios["Market Cap"] = self.info.get("marketCap")

            # Current Price: Latest traded price of the stock
            # Analysis:
            # - Used as reference for valuation & technical levels
            # - Compare with intrinsic value → undervalued / overvalued
            ratios["Current Price"] = self.info.get("currentPrice")

            # 52 Week High: Highest price in last 1 year
            # Analysis:
            # - Near high → bullish sentiment / momentum
            # - Far below → potential undervaluation OR weak trend
            ratios["52W High"] = self.info.get("fiftyTwoWeekHigh")

            # 52 Week Low: Lowest price in last 1 year
            # Analysis:
            # - Near low → bearish sentiment or value buying opportunity
            # - Used to assess volatility range
            ratios["52W Low"] = self.info.get("fiftyTwoWeekLow")


            # ---------- Valuation ----------
            # PE Ratio: Price to Earnings Ratio
            # = Price / Earnings per share
            # Analysis:
            # - High PE → growth expectations OR overvalued
            # - Low PE → undervalued OR weak business
            # - Compare with industry average for better insight
            ratios["PE Ratio"] = self.info.get("trailingPE")

            # Forward PE: Future expected PE based on projected earnings
            # Analysis:
            # - Lower than current PE → expected earnings growth
            # - Higher → earnings may decline
            ratios["Forward PE"] = self.info.get("forwardPE")

            # Price to Book (P/B): Price / Book Value
            # Analysis:
            # - < 1 → potentially undervalued (or distressed)
            # - > 3 → premium valuation
            # - Useful for banks, asset-heavy companies
            ratios["Price to Book"] = self.info.get("priceToBook")


            # ---------- Profitability ----------
            # ROE (Return on Equity): Profit generated from shareholder capital
            # Analysis:
            # - High ROE (>15-20%) → efficient management
            # - Very high ROE → check for high debt influence
            ratios["ROE"] = self.info.get("returnOnEquity")

            # ROA (Return on Assets): Profit generated from total assets
            # Analysis:
            # - Indicates asset efficiency
            # - Higher is better; low ROA → inefficient asset use
            ratios["ROA"] = self.info.get("returnOnAssets")

            # Operating Margin: Operating profit as % of revenue
            # Analysis:
            # - Shows core business strength
            # - High margin → pricing power / efficiency
            # - Falling margin → cost pressure
            ratios["Operating Margin"] = self.info.get("operatingMargins")

            # Net Profit Margin: Final profit after all expenses
            # Analysis:
            # - Indicates overall profitability
            # - Compare across competitors
            ratios["Net Profit Margin"] = self.info.get("profitMargins")


            # ---------- Liquidity ----------
            # Current Ratio: Current Assets / Current Liabilities
            # Analysis:
            # - >1 → company can meet short-term obligations
            # - Too high → inefficient capital usage
            ratios["Current Ratio"] = self.info.get("currentRatio")

            # Quick Ratio: (Cash + Receivables) / Current Liabilities
            # Analysis:
            # - More strict liquidity measure
            # - <1 → potential liquidity risk
            ratios["Quick Ratio"] = self.info.get("quickRatio")


            # ---------- Leverage ----------
            # Debt to Equity: Total Debt / Shareholder Equity
            # Analysis:
            # - High ratio → high financial risk
            # - Low ratio → conservative capital structure
            # - Industry-dependent (banks naturally higher)
            ratios["Debt to Equity"] = self.info.get("debtToEquity")


            # ---------- Cash Flow ----------
            # Operating Cash Flow: Cash generated from operations
            # Analysis:
            # - Positive & growing → healthy business
            # - Negative → red flag (even if profits exist)
            ratios["Operating Cash Flow"] = self.info.get("operatingCashflow")

            # Free Cash Flow: Cash left after capital expenditure
            # Analysis:
            # - Positive FCF → company can reinvest, pay dividends
            # - Negative FCF → heavy investments or financial stress
            ratios["Free Cash Flow"] = self.info.get("freeCashflow")


            # ---------- Growth ----------
            # Revenue Growth: Growth in sales
            # Analysis:
            # - Indicates business expansion
            # - Consistent growth → strong demand
            ratios["Revenue Growth"] = self.info.get("revenueGrowth")

            # Earnings Growth: Growth in profit
            # Analysis:
            # - More important than revenue growth
            # - High earnings growth → improving efficiency
            ratios["Earnings Growth"] = self.info.get("earningsGrowth")


            # ---------- Dividend ----------
            # Dividend Yield: Dividend / Price
            # Analysis:
            # - High yield → income-generating stock
            # - Very high yield → possible distress (dividend trap)
            # - Preferred by long-term & conservative investors
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