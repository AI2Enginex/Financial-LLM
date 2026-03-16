from langchain_core.prompts import PromptTemplate

# ========================== PROMPT TEMPLATES ============================

class PromptTemplates:

    @classmethod
    def financial_analysis_prompt(cls):

        prompt = """
        You are a senior equity research analyst with expertise in fundamental analysis, financial statement interpretation, and valuation.

        Your task is to analyze the provided financial data for the company and produce a professional financial analysis report similar to what institutional investment analysts produce.

        Company: {company_name}

        Financial Data:
        {financial_data}

        Instructions:

        Perform a deep financial analysis using the provided data. Your analysis must be objective, data-driven, and structured.

        Follow this structure:

        1. Business Overview
        Provide a brief overview of the company and its likely business model based on the financial data.

        2. Revenue Analysis
        Analyze revenue trends, growth consistency, and any observable patterns.

        3. Profitability Analysis
        Evaluate profitability using metrics such as:
        - Gross Margin
        - Operating Margin
        - Net Margin
        - ROE
        - ROCE

        Explain what the numbers suggest about operational efficiency.

        4. Balance Sheet Strength
        Evaluate the financial position using:
        - Debt levels
        - Debt-to-Equity
        - Current Ratio
        - Asset growth
        - Equity growth

        Assess financial stability and leverage risk.

        5. Cash Flow Analysis
        Analyze operating cash flow, investing cash flow, and financing cash flow.
        Determine whether profits are supported by real cash generation.

        6. Financial Ratios Interpretation
        Interpret the provided ratios including:
        - Profitability ratios
        - Liquidity ratios
        - Leverage ratios
        - Efficiency ratios
        - Valuation ratios (if present)

        Explain what each major ratio indicates about the company's financial health.

        7. Growth Analysis
        Evaluate historical growth across:
        - Revenue
        - Net income
        - Assets
        - Equity

        Comment on growth sustainability.

        8. Red Flags (If Any)
        Highlight potential concerns such as:
        - Rising debt
        - Declining margins
        - Weak cash flow
        - Inconsistent growth
        - Overvaluation signals

        9. Strengths
        Identify key financial strengths of the company.

        10. Weaknesses
        Identify financial weaknesses or risks.

        11. Overall Financial Health
        Provide a clear summary of the company’s financial condition.

        12. Investment Perspective
        Based purely on the financial data:
        - Is the company financially strong?
        - Is growth sustainable?
        - Does the data suggest a quality business?

        Do NOT fabricate missing numbers.
        Base conclusions only on the data provided.

        Write the analysis in a professional tone similar to an equity research report.
        Use clear headings and structured explanations.
        """

        return PromptTemplate(template=prompt.strip(), input_variables=["company_name", "financial_data"])