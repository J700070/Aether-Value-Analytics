from time import sleep
import requests
import pandas as pd
import numpy as np
from django.conf.urls.static import static
from django.conf import settings
from sqlalchemy import create_engine, over
from .models import Company, Stock_price, Company_Fundamentals



def get_growth(df):
    temp_df = df.copy()
    res_df = df.copy()

    # Replace commas with nothing
    temp_df = temp_df.applymap(lambda x: x.replace(',', ''))

    # Convert to float
    temp_df = temp_df.apply(pd.to_numeric, errors='coerce')

    res_df["Δ 1Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-2]) - 1
    res_df["Δ 2Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-3]) - 1
    res_df["Δ 3Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-4]) - 1
    res_df["Δ 4Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-5]) - 1
    # temp_df["5 Year"] = (temp_df.iloc[:,-1].astype(float) / temp_df.iloc[:,-8].astype(float)) - 1
    # temp_df["10 Year"] = (temp_df.iloc[:,-1].astype(float) / temp_df.iloc[:,-12].astype(float)) - 1
    return res_df

def get_cagr_growth(df):
    temp_df = df.copy()
    res_df = df.copy()

    # Replace commas with nothing
    temp_df = temp_df.applymap(lambda x: x.replace(',', ''))

    # Convert to float
    temp_df = temp_df.apply(pd.to_numeric, errors='coerce')

    res_df["CAGR 1Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-2])**(1/1) - 1
    res_df["CAGR 2Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-3])**(1/2) - 1
    res_df["CAGR 3Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-4])**(1/3) - 1
    res_df["CAGR 4Y"] = (temp_df.iloc[:,-1] / temp_df.iloc[:,-5])**(1/4) - 1

    return res_df



def get_stock_fundamentals(ticker):
    main_df = pd.DataFrame()
    growth_df = pd.DataFrame()

    # Get the stock fundamentals from the DB
    fundamental_list = pd.DataFrame(list(Company_Fundamentals.objects.filter(company_id=ticker).order_by('-date_col').all().values()))
    
    if fundamental_list.empty:
        print("No fundamentals found for " + ticker)
        return None

    # Dataframe formatting
    fundamental_list.set_index('year', inplace=True)
    fundamental_list.rename_axis(None, axis=0, inplace=True)
    fundamental_list.drop(['company_id', "id", "date_col","currency","datetime_added","datetime_updated"], axis=1, inplace=True)

    fundamental_list = fundamental_list.sort_index(ascending=True)

    # Convert to millions
    total_columns = fundamental_list.columns.tolist()
    not_to_convert = ["gross_profit_margin", "ebitda_margin","ebit_margin", "income_before_tax_margin","net_income_margin",
    "eps","eps_diluted"]
    share_columns = ["weighted_average_shares", "weighted_average_shares_diluted"]
    to_convert = list(set(total_columns) - set(not_to_convert) - set(share_columns))

    fundamental_list[to_convert + share_columns] = fundamental_list[to_convert + share_columns].apply(lambda x: x/1000000)


    # Format the thousands separator

    fundamental_list[to_convert]= fundamental_list[to_convert].applymap('{:,.2f}'.format)
    fundamental_list[share_columns]= fundamental_list[share_columns].applymap('{:,.2f}'.format)

    # Ratio formatting
    margin_cols = [ col for col in total_columns if "margin" in col]
    margin_cols.append("eps")
    margin_cols.append("eps_diluted")
    fundamental_list[margin_cols] = fundamental_list[margin_cols].applymap(lambda x: '{:,.2f}'.format(float(x)))

    # Transpose
    main_df = fundamental_list.T

    # Naming
    main_df.index  = ["Revenue", "Cost of Revenue", "Gross Profit", "Gross Profit Margin (%)", 
    "Research & Development Exp.","General & Administrative Exp.", "Selling & Marketing Exp.","Selling, General & Administrative Exp.","Other Exp.",
    "Operating Exp.", "CoR & Exp.", "Interest Income", "Interest Expense","Depreciation & Amortization", "EBITDA", 
    "EBITDA Margin (%)", "Operating Income","Operating Margin (%)","Total Other Income Exp.","Income Before Tax",
     "Income Before Tax Margin (%)", "Income Tax Expense","Net Income","Net Income Margin (%)","EPS","EPS Diluted",
     "W. A. Number of Shares", "W. A. Number of Diluted Shares", "Cash & Cash Equivalents","Short-Term Investments",
     "Cash & Short-Term Investments", "Net Receivables", "Inventory (Balance Sheet)", "Other Current Assets", "Total Current Assets",
     "Property, Plant & Equipment", "Goodwill", "Intangible Assets", "Goodwill & Intangible Assets", "Long-Term Investments", "Tax Assets",
     "Other Non-Current Assets","Total Non-Current Assets", "Other Assets", "Total Assets", "Accounts Payable (Balance Sheet)",
     "Short-Term Debt","Tax Payable","Deferred Revenue Current", "Other Current Liabilities", "Total Current Liabilities","Long-Term Debt",
     "Deferred Revenue Non-Current","Deferred Tax Liabilities Non-Current", "Other Non-Current Liabilities", "Total Non-Current Liabilities", "Other Liabilities",
     "Capital Lease Obligations", "Total Liabilities", "Preferred Stock", "Common Stock", "Retained Earnings","Accum. Other Compr. Income Loss",
     "Other Total Stockholders Equity","Total Stockholders Equity", "Total Liabilities & Stockholders Equity", "Minority Interest", "Total Equity",
     "Total Liabilities & Equity", "Total Investments", "Total Debt", "Net Debt", "Net Income (Cash Flow)", "Deprec. & Amort. (Cash Flow)",
     "Deferred Income Tax", "Stock Based Compensation", "Change in Working Capital","Accounts Receivables (Cash Flow)",
     "Inventory (Cash Flow)", "Accounts Payable (Cash Flow)", "Other Working Capital", "Other Non-Cash Items", "Net Cash Prov. by Op. Activities",
     "Investments in PP&E", "Aquisitions Net", "Purchase of Investments", "Sales/Maturities of Investments",
     "Other Investing Activities", "Net Cash Used for Investing Activities", "Debt Repayment", "Common Stock Issued", "Common Stock Repurchased",
     "Dividends Paid", "Other Financing Activities", "Net Cash Used for Financing Activities", "Effect of Exch. Rate Changes on Cash",
     "Net Change in Cash", "Cash at the End of the Period", "Cash at the Beginning of the Period", "Operating Cash Flow",
     "CapEx", "Free Cash Flow"]

    # Get the growth dataframe
    main_with_growth = get_growth(main_df)
    main_with_cagr_growth = get_cagr_growth(main_df)

    growth_df = main_with_growth.iloc[:,-4:]
    cagr_growth_df = main_with_cagr_growth.iloc[:,-4:]
    
    
    # Format the growth dataframe as a percentage
    growth_df = growth_df.applymap(lambda x: '{:,.1f}'.format(float(x)*100) + '%')
    cagr_growth_df = cagr_growth_df.applymap(lambda x: '{:,.1f}'.format(float(x)*100) + '%')

    # Temp until complete api access
    num = 0
    for col in main_df:
        if num <= 2:
            main_df[str(col)+" E"] = main_df[col]
            num+=1

    # Divide the df for the tabs
    is_df = main_df.iloc[:28,:]
    bs_df= main_df.iloc[28:-30,:]
    fcf_df = main_df.iloc[-30:,:]

    is_growth_df = growth_df.iloc[:28,:]
    bs_growth_df = growth_df.iloc[28:-30,:]
    fcf_growth_df = growth_df.iloc[-30:,:]

    is_cagr_growth_df = cagr_growth_df.iloc[:28,:]
    bs_cagr_growth_df = cagr_growth_df.iloc[28:-30,:]
    fcf_cagr_growth_df = cagr_growth_df.iloc[-30:,:]

    # main_df with ratios
    # ======================================================================
    main_with_ratios = main_df.T.copy()
    # Replace commas with nothing
    main_with_ratios = main_with_ratios.applymap(lambda x: x.replace(',', ''))
    # Convert to float
    main_with_ratios = main_with_ratios.apply(pd.to_numeric, errors='coerce')
    main_with_ratios["Book Value"] = main_with_ratios["Total Assets"] - main_with_ratios["Total Liabilities"] - main_with_ratios["Goodwill & Intangible Assets"] - main_with_ratios["Total Liabilities"]

    # Overview
    # =======================================================================
    temp_main_df = main_df.T
    # Replace commas with nothing
    temp_main_df = temp_main_df.applymap(lambda x: x.replace(',', ''))
    # Convert to float
    temp_main_df = temp_main_df.apply(pd.to_numeric, errors='coerce')

    index = main_df.columns.to_list()
    
    
    overview_df = pd.DataFrame(index=index)
    overview_df["Total Assets"] = temp_main_df["Total Assets"]
    overview_df["Book Value"] = main_with_ratios["Book Value"]
    overview_df["Revenue"] = temp_main_df["Revenue"]
    overview_df["Gross Profit"] = temp_main_df["Gross Profit"]
    overview_df["EBITDA"] = temp_main_df["EBITDA"]
    overview_df["Operating Income"] = temp_main_df["Operating Income"]
    overview_df["Net Income"] = temp_main_df["Net Income"]
    overview_df["Free Cash Flow"] = temp_main_df["Free Cash Flow"]

    overview_df["Total Assets per Share"] = temp_main_df["Total Assets"] / temp_main_df["W. A. Number of Shares"]
    overview_df["Book Value per Share"] = overview_df["Book Value"]/temp_main_df["W. A. Number of Shares"]
    overview_df["Revenue per Share"] =  overview_df["Revenue"] / temp_main_df["W. A. Number of Shares"]
    overview_df["Gross Profit per Share"] =  overview_df["Gross Profit"] / temp_main_df["W. A. Number of Shares"]
    overview_df["EBITDA per Share"] =  overview_df["EBITDA"] / temp_main_df["W. A. Number of Shares"]
    overview_df["Operating Income per Share"] =  overview_df["Operating Income"] / temp_main_df["W. A. Number of Shares"]
    overview_df["EPS"] = temp_main_df["EPS"]
    overview_df["Free Cash Flow per Share"] =  overview_df["Free Cash Flow"] / temp_main_df["W. A. Number of Shares"]
    

    overview_df = overview_df.T

    return main_df, growth_df, is_df, bs_df, fcf_df, is_growth_df, bs_growth_df, fcf_growth_df, is_cagr_growth_df, bs_cagr_growth_df, fcf_cagr_growth_df, overview_df