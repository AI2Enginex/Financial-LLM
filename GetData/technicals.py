import numpy as np
# Allows for further data manipulation and analysis
import pandas as pd
from langchain_core.documents import Document
from datetime import datetime, timedelta
import json

import yfinance as yf  # Reads stock data



def daily_return(dataframe=None, timeframe=None, feature=None):
    """
    Calculate the daily return of a feature based on a specified timeframe.

    This function computes the percentage change of the specified feature over the specified timeframe.

    Parameters:
    dataframe (pandas.DataFrame): DataFrame containing the data.
    timeframe (int): Number of periods to compute the daily return.
    feature1 (str): Name of the new feature where the daily return will be stored.
    feature2 (str): Name of the feature to calculate the daily return from.

    Returns:
    pandas.DataFrame: DataFrame with the daily return values appended under a new column.

    If an error occurs during calculation, return the error message.
    """
    try:
        # Calculate the percentage change of the specified feature over the specified timeframe
        dataframe['daily_return'] = dataframe[feature].pct_change(timeframe)
        return dataframe
    except Exception as e:
        # If an error occurs during calculation, return the error message
        return e

def cumalitive_return(df,feature):
    """

    Cumulative return represents the aggregate growth of an investment over a specified period,
    reflecting both capital appreciation and reinvested income. It is calculated by multiplying
    the individual periodic returns and adding 1, then taking the cumulative product of these values.
    The resulting figure indicates the overall performance of the investment from its starting point
    to the end of the period. Higher cumulative returns signify greater profitability, while negative
    cumulative returns indicate losses.
    """
    try:
        # Calculate cumulative returns using cumprod() function
        df["cum_return"] = (1 + df[feature]).cumprod()
        return df
    except Exception as e:
        # If an error occurs during calculation, return the error message
        return e

  
def average_return(df=None,feature=None,days=None):
    """
    Annualized return measures the average rate of return per year, adjusted for compounding.
    It is calculated by taking the mean return over the period, then multiplying by the number
    of trading days in a year (e.g., 252 for daily data). The result is expressed as a percentage.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the data.
    start (str): Start date of the date range (format: 'YYYY-MM-DD').
    end (str): End date of the date range (format: 'YYYY-MM-DD').
    feature (str): Name of the feature to calculate the return from.

    Returns:
    float: Annualized return percentage.

    If an error occurs during calculation, return the error message.
    """
    try:
        # Calculate the mean return over the period and annualize it (assuming 252 trading days in a year)
        return (((1 + df[feature].mean()) ** days)-1) * 100
    except Exception as e:
        # If an error occurs during calculation, return the error message
        return e
            
class ReadData:
    """
    A class to read stock and market data from Yahoo Finance using the yfinance library.

    Attributes:
    ----------
    start : str
        The start date for the data retrieval in 'YYYY-MM-DD' format.
    end : str
        The end date for the data retrieval in 'YYYY-MM-DD' format.

    Methods:
    --------
    market_dataframe(ticker=None):
        Downloads market index data (like NSE, BSE) for the given date range.
        
    read_dataframe(ticker=None):
        Downloads stock data (e.g., TCS) for the given date range.
    """
    
    def __init__(self, start=None, end=None):
        """
        Initializes the ReadData class with the specified start and end dates.

        Parameters:
        -----------
        start : str
            The start date for downloading data (in 'YYYY-MM-DD' format).
        end : str
            The end date for downloading data (in 'YYYY-MM-DD' format).
        """
        self.start = start
        self.end = end

    def market_dataframe(self, ticker=None):
        """
        Downloads market index data from Yahoo Finance for the specified market index ticker.

        Parameters:
        -----------
        ticker : str
            The ticker symbol of the market index (e.g., 'NSE' or 'BSE').

        Returns:
        --------
        DataFrame
            A Pandas DataFrame with market index data for the specified date range.
        """
        try:
            # Return the market index dataframe
            return yf.download("^" + ticker, start=self.start, end=self.end).reset_index()
        except Exception as e:
            return e

    def read_dataframe(self, ticker=None):
        """
        Downloads stock data from Yahoo Finance for the specified stock ticker.

        Parameters:
        -----------
        ticker : str
            The ticker symbol of the stock (e.g., 'TCS').

        Returns:
        --------
        DataFrame
            A Pandas DataFrame with stock data for the specified date range.
        """
        try:
            df = yf.download(ticker + ".NS", start=self.start, end=self.end)

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]

            return df.reset_index()
        except Exception as e:
            return e


class ReturnAnalysis:
    """
    A class to perform various types of return analysis on financial data.

    Attributes:
    -----------
    feature : str
        The feature/column name for which the return analysis is performed (e.g., 'Close', 'Adj Close').

    Methods:
    --------
    daily_return_analysis(data=None, days=None):
        Calculates daily returns for the specified number of days.

    cumalative_return_analysis(data=None, featurename=None):
        Calculates cumulative returns for the specified feature.

    average_return_analysis(data=None, days=None, featurename=None):
        Calculates the average return over a given number of days for the specified feature.
    """

    def __init__(self, feature=None):
        """
        Initializes the ReturnAnalysis class with the specified feature (column name).

        Parameters:
        -----------
        feature : str
            The feature/column name for which return analysis is to be performed (e.g., 'Close', 'Adj Close').
        """
        self.feature = feature

    def daily_return_analysis(self, data=None, days=None):
        """
        Calculates the daily return for the specified number of days.

        Parameters:
        -----------
        data : DataFrame
            The dataframe containing the financial data.
        days : int
            The number of days to use for the daily return calculation (e.g., 1 for daily, 30 for monthly).

        Returns:
        --------
        DataFrame
            A dataframe with daily return values based on the specified timeframe.
        """
        try:
            return daily_return(dataframe=data, timeframe=days, feature=self.feature)
        except Exception as e:
            # Return the exception if an error occurs during calculation
            return e

    def cumalative_return_analysis(self, data=None, featurename=None):
        """
        Calculates the cumulative return for the specified feature over the given period.

        Parameters:
        -----------
        data : DataFrame
            The dataframe containing the financial data.
        featurename : str
            The feature/column name for which cumulative return is to be calculated.

        Returns:
        --------
        DataFrame
            A dataframe with the cumulative return values.
        """
        try:
            return cumalitive_return(df=data, feature=featurename)
        except Exception as e:
            # Return the exception if an error occurs during calculation
            return e

    def average_return_analysis(self, data=None, days=None, featurename=None):
        """
        Calculates the average return over a specified number of days for the given feature.

        Parameters:
        -----------
        data : DataFrame
            The dataframe containing the financial data.
        days : int
            The number of days to calculate the average return.
        featurename : str
            The feature/column name for which the average return is to be calculated.

        Returns:
        --------
        DataFrame
            A dataframe with average return values.
        """
        try:
            return average_return(df=data, feature=featurename, days=days)
        except Exception as e:
            # Return the exception if an error occurs during calculation
            return e



class VolatilityAnalysis:
    """
    A class to analyze volatility, Value at Risk (VaR), and beta of financial data.

    Attributes:
    -----------
    feature : str
        The feature/column name for which the volatility analysis is performed (e.g., 'Close', 'Adj Close').

    Methods:
    --------
    volatility_std(df=None, days=None):
        Calculates the standard deviation (volatility) based on the specified number of days (e.g., 21 for monthly, 252 for annual).
    
    volatility_VAR(df=None, confidence_level=None):
        Calculates the Value at Risk (VaR) for the specified confidence level.
    
    beta_analysis(df=None, market_df=None):
        Calculates the beta of the stock in comparison to the market data.
    volatility(dataframe=None, bins=None):
        Plotting histogram of the daily returns in order to visualize the volatility
    
    """

    def __init__(self, featurename=None):
        """
        Initializes the VolatilityAnalysis class with the specified feature (column name).

        Parameters:
        -----------
        featurename : str
            The feature/column name for which volatility analysis is to be performed (e.g., using daily_return for 'Close' or 'Adj Close').
        """
        self.feature = featurename

    def volatility_std(self, df=None, days=None):
        """
        Calculates the annualized or monthly volatility (standard deviation) for the specified number of days.

        Parameters:
        -----------
        df : DataFrame
            The dataframe containing the financial data.
        days : int
            The number of days to annualize or convert the volatility (e.g., 252 for annual, 21 for monthly).

        Returns:
        --------
        float
            The volatility (standard deviation) as a percentage.
        """
        try:
            # Calculate the standard deviation of the specified feature
            daily_volatility = df[self.feature].std()
            # Convert daily volatility to either annual or monthly volatility (252 for annual, 21 for monthly)
            volatility = daily_volatility * np.sqrt(days)
            return volatility * 100  # Return as a percentage
        except Exception as e:
            return e

    def volatility_VAR(self, df=None, confidence_level=None):
        """
        Calculates the Value at Risk (VaR) based on the specified confidence level.

        Parameters:
        -----------
        df : DataFrame
            The dataframe containing the financial data.
        confidence_level : float
            The confidence level (e.g., 0.05 for 95% confidence interval).

        Returns:
        --------
        float
            The Value at Risk (VaR) as a percentage.
        """
        try:
            # Sort the returns of the specified feature in ascending order
            sorted_returns = df[self.feature].dropna().sort_values()
            # Find the VaR at the specified percentile
            VaR = np.percentile(sorted_returns, 100 * confidence_level)
            return VaR * 100  # Return as a percentage
        except Exception as e:
            return e

    def beta_analysis(self, df=None, market_df=None):
        """
        Calculates the beta of a stock with respect to the market data.

        Beta measures the stock's volatility relative to the market. A beta greater than 1 means the stock is more volatile than the market, while a beta less than 1 means it is less volatile.

        Parameters:
        -----------
        df : DataFrame
            The dataframe containing the financial data for the stock.
        market_df : DataFrame
            The dataframe containing the financial data for the market (benchmark).

        Returns:
        --------
        float
            The beta of the stock relative to the market.
        """
        try:
            # Calculate the covariance matrix between the stock and market returns
            cov_matrix = np.cov(df[self.feature].dropna(), market_df[self.feature].dropna())
            # Extract the covariance between stock and market
            cov = cov_matrix[0, 1]
            # Calculate the variance of the market returns
            var = np.var(market_df[self.feature].dropna())
            # Calculate beta (covariance divided by variance)
            beta = cov / var
            return beta
        except Exception as e:
            return e



class MovinAverageAnalysis:

    def __init__(self,dataframe=None,featurename=None):
        
        self.dataframe = dataframe
        self.feature = featurename

    def simple_moving_average(self,windowsize=None):
        """
        SMA is a widely used technical indicator that smooths out price data by calculating
        the average of a specified number of past prices. It helps identify trends and reversals
        by filtering out short-term fluctuations.

        Parameters:
        dataframe (pandas.DataFrame): DataFrame containing the data.
        feature (str): Name of the feature to calculate the SMA from.
        windowsize (int): Size of the moving window for the SMA calculation.

        Returns:
        pandas.DataFrame: DataFrame with the SMA values appended under a new column.

        If an error occurs during calculation, return the error message.
        """
        try:
            # Calculate the Simple Moving Average
            self.dataframe['SIMPLE_MA_' +
                    str(windowsize)] = self.dataframe[self.feature].rolling(windowsize).mean()
            return self.dataframe
        except Exception as e:
            # If an error occurs during calculation, return the error message
            return e


    def exponential_moving_average(self,windowsize=None):
        """
        EMA is a type of moving average that places greater weight on more recent data points,
        making it more responsive to recent price changes. It helps identify trends and reversals
        by providing a smoother representation of price movements compared to SMA.

        Parameters:
        dataframe (pandas.DataFrame): DataFrame containing the data.
        feature (str): Name of the feature to calculate the EMA from.
        windowsize (int): Size of the moving window for the EMA calculation.

        Returns:
        pandas.DataFrame: DataFrame with the EMA values appended under a new column.

        If an error occurs during calculation, return the error message.
        """
        try:
            # Calculate the Exponential Moving Average
            self.dataframe['EXPONENTIAL_MA_' + str(windowsize)] = self.dataframe[self.feature].ewm(
                span=windowsize, adjust=False, min_periods=windowsize).mean()
            return self.dataframe
        except Exception as e:
            # If an error occurs during calculation, return the error message
            return e


# Class for Creating Dcouments for Technicals 
class TechnicalsDocumentBuilder:
    
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size  # creating a group of 10 dates to be 
                                      # placed together in a single document
    
    # Clean the Data before processing 
    def _clean_dataframe(self, df: pd.DataFrame):
        try:
            df = df.copy()
            df = df.fillna("N/A")
            df.index = df.index.astype(str)
            return df
        except Exception as e:
            print(f"Error while processing DataFrame: {str(e)}")
    

    # Splitting data into chunks for efficient processing
    def _chunk_dataframe(self, df: pd.DataFrame):
        try:
            chunks = list()
            for i in range(0, len(df), self.chunk_size):
                chunks.append(df.iloc[i:i + self.chunk_size])
            return chunks
        except Exception as e:
            print(f"Error while Creating DataFrame Chunks: {str(e)}")

    
    # Creating Documents for Technicals and Metrics
    def create_documents(self, df, metrics: dict, ticker: str):
        try:
            documents = list()

            df = self._clean_dataframe(df)
            chunks = self._chunk_dataframe(df)

            # Time-series documents
            for i, chunk in enumerate(chunks):
                content = json.dumps(chunk.to_dict(orient="index"), indent=2)

                documents.append(
                    Document(
                        page_content=content.replace("\n","").replace("   ","").strip(),
                        metadata={
                            "type": "time_series",
                            "ticker": ticker,
                            "chunk_id": i,
                            "rows": len(chunk)
                        }
                    )
                )

            # Metrics document
            safe_metrics = {
                "avg_return": round(metrics.get("avg_return", 0), 2),
                "volatility": round(metrics.get("volatility", 0), 2),
                "VaR": round(metrics.get("VaR", 0), 2),
                "beta": round(metrics.get("beta", 0), 2)
                if isinstance(metrics.get("beta"), (int, float)) else "N/A"
            }

            metrics_content = f"""
                Average Return: {safe_metrics['avg_return']}
                ,Volatility: {safe_metrics['volatility']}
                ,Value at Risk (VaR): {safe_metrics['VaR']}
                Beta: {safe_metrics['beta']}
                """

            documents.append(
                Document(
                    page_content=metrics_content.strip().replace("\n","").replace("   ",""),
                    metadata={
                        "type": "metrics",
                        "ticker": ticker
                    }
                )
            )

            return documents
        except Exception as e:
             print(f"Error while Creating Documents: {str(e)}")


# Main Executer function
# returns a list of documents for Technicals and metrics
def compute_all_technicals(ticker: str, start_str: str, end_str: str, moving_average_days: int):
        
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")

        total_days = (end_date - start_date).days
        print("total days : ",  total_days)
        reader = ReadData(start=start_str, end=end_str)
        df = reader.read_dataframe(ticker=ticker)

        # Returns
        ret = ReturnAnalysis(feature="Close")
        df = ret.daily_return_analysis(df, 1)
        df = ret.cumalative_return_analysis(df, "daily_return")
        avg_return = ret.average_return_analysis(df, total_days, "daily_return")

        # Volatility
        vol = VolatilityAnalysis(featurename="daily_return")
        volatility = vol.volatility_std(df, total_days)
        var = vol.volatility_VAR(df, 0.05)

        # Market data (beta)
        market_df = reader.market_dataframe("NSEI")
        market_df = ret.daily_return_analysis(market_df, 1)

        try:
            beta = vol.beta_analysis(df, market_df)
        except Exception:
            beta = None

        # Moving averages
        ma = MovinAverageAnalysis(df, "Close")
        df = ma.simple_moving_average(moving_average_days)
        df = ma.exponential_moving_average(moving_average_days)

        df = df.set_index("Date")

        # Round values
        df = df.round(2)

        # Build documents
        builder = TechnicalsDocumentBuilder(chunk_size=10)

        documents = builder.create_documents(
            df=df,
            metrics={
                "avg_return": avg_return,
                "volatility": volatility,
                "VaR": var,
                "beta": beta
            },
            ticker=ticker
        )

        return documents



if __name__ == "__main__":
    
    # Run
    docs = compute_all_technicals(ticker="INFY",start_str='2024-01-01',end_str='2026-01-01',moving_average_days=10)

    print(docs)