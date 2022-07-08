from time import sleep
import requests
import pandas as pd

import numpy as np
from django.conf.urls.static import static
from django.conf import settings
from sqlalchemy import create_engine
from .models import Company, Stock_price, Company_Fundamentals, Company_alternative_data

API_KEY = "f3dee427bc96ae3b4f877450a0412ec1"




def get_company_data_func(ticker):
    print("Getting data for " + ticker)

    # Save to database

    # Basic Data
    url = ("https://financialmodelingprep.com/api/v3/profile/"+ticker+"?apikey="+API_KEY)
    data = requests.get(url).json()[0]

    url = ("https://financialmodelingprep.com/api/v3/stock-price-change/"+ticker+"?apikey="+API_KEY)
    data_price_change = requests.get(url).json()[0]
     
    updated_values = {
                    "price" : data["price"],
                    "beta" : data["beta"],
                    "volume_average" : data["volAvg"],
                    "last_dividend" : data["lastDiv"],
                    "low" : data["range"].split("-")[0],
                    "high" : data["range"].split("-")[1],
                    "change" : data["changes"],
                    "name" : data["companyName"],
                    "currency" : data["currency"],
                    "isin" : data["isin"],
                    "cusip" : data["cusip"],
                    "exchange" : data["exchange"],
                    "exchange_sort" : data["exchangeShortName"],
                    "sector" : data["sector"],
                    "industry" : data["industry"],
                    "website" : data["website"],
                    "description" : data["description"],
                    "ceo" : data["ceo"],
                    "country" : data["country"],
                    "city" : data["city"],
                    "number_of_employees" : data["fullTimeEmployees"],
                    "phone" : data["phone"],
                    "address" : data["address"],
                    "state" : data["state"],
                    "zip_code" : data["zip"],
                    "dcf" : data["dcf"],
                    "logo_url" : data["image"],
                    "ipo_date" : data["ipoDate"],
                    "cik" : data["cik"],
                    "enterprise_value" : 0,
                    "market_cap" : data["mktCap"],
                    "insider_ownership" : 0,
                    "institutional_ownership" : 0,
                    "is_default_image" : data["defaultImage"],
                    "is_etf" : data["isEtf"],
                    "is_actively_traded" : data["isActivelyTrading"],
                    "is_adr" : data["isAdr"],
                    "is_fund" : data["isFund"],
                    "change_1d" : data_price_change["1D"],
                    "change_5d" : data_price_change["5D"],
                    "change_1m" : data_price_change["1M"],
                    "change_3m" : data_price_change["3M"],
                    "change_6m" : data_price_change["6M"],
                    "change_ytd" : data_price_change["ytd"],
                    "change_1y" : data_price_change["1Y"],
                    "change_3y" : data_price_change["3Y"],
                    "change_5y" : data_price_change["5Y"],
                    "change_10y" : data_price_change["10Y"],
                    "change_max" : data_price_change["max"],
                    }

    Company.objects.update_or_create(ticker = data["symbol"], defaults = updated_values)
    

    # Fundamental Data
    # Income Statement
    url = ("https://financialmodelingprep.com/api/v3/income-statement/"+ticker+"?apikey="+API_KEY)
    data_income = requests.get(url).json()
    # Balance Sheet
    url = ("https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+ticker+"?apikey="+API_KEY)
    data_balance = requests.get(url).json()
    # Cash Flow
    url = ("https://financialmodelingprep.com/api/v3/cash-flow-statement/"+ticker+"?apikey="+API_KEY)
    data_cashflow = requests.get(url).json()

    for elem_i in data_income:

        # Get corresponding balance sheet and cash flow data
        for elem_balance in data_balance:
            if elem_i["date"] == elem_balance["date"]:
                elem_b = elem_balance

        for elem_cashflow in data_cashflow:
            if elem_i["date"] == elem_cashflow["date"]:
                elem_c = elem_cashflow
                        
        updated_values = {
            "company" : Company.objects.get(ticker=ticker),
            "year" : elem_i["calendarYear"],
            "date_col" : elem_i["date"],
            "currency" : elem_i["reportedCurrency"],
            "revenue" : elem_i["revenue"],
            "cogs" : elem_i["costOfRevenue"],
            "gross_profit" : elem_i["grossProfit"],
            "gross_profit_margin" : elem_i["grossProfitRatio"],
            "research_and_development_exp" : elem_i["researchAndDevelopmentExpenses"],
            "general_and_administrative_exp" : elem_i["generalAndAdministrativeExpenses"],
            "selling_and_marketing_exp" : elem_i["sellingAndMarketingExpenses"], 
            "selling_general_and_admin_exp" : elem_i["sellingGeneralAndAdministrativeExpenses"],
            "other_expenses" : elem_i["otherExpenses"],
            "operating_expenses" : elem_i["operatingExpenses"],
            "cogs_and_expenses" : elem_i["costAndExpenses"],
            "interest_income" : elem_i["interestIncome"],
            "interest_expense" : elem_i["interestExpense"],
            "depreciation_and_amortization" : elem_i["depreciationAndAmortization"],
            "ebitda" : elem_i["ebitda"],
            "ebitda_margin" : elem_i["ebitdaratio"], 
            "ebit" : elem_i["operatingIncome"],
            "ebit_margin" : elem_i["operatingIncomeRatio"], 
            "total_other_income_expenses" : elem_i["totalOtherIncomeExpensesNet"],
            "income_before_tax" : elem_i["incomeBeforeTax"],
            "income_before_tax_margin" : elem_i["incomeBeforeTaxRatio"], 
            "income_tax_expense" : elem_i["incomeTaxExpense"],
            "net_income" : elem_i["netIncome"],
            "net_income_margin" : elem_i["netIncomeRatio"],
            "eps" : elem_i["eps"],
            "eps_diluted" : elem_i["epsdiluted"],
            "weighted_average_shares" : elem_i["weightedAverageShsOut"],
            "weighted_average_shares_diluted" : elem_i["weightedAverageShsOutDil"], 
            
            "cash_and_cash_equivalents" : elem_b["cashAndCashEquivalents"],
            "short_term_investments" : elem_b["shortTermInvestments"], 
            "cash_and_short_term_investments" : elem_b["cashAndShortTermInvestments"], 
            "net_receivables" : elem_b["netReceivables"], 
            "inventory_balance_sheet" : elem_b["inventory"], 
            "other_current_assets" : elem_b["otherCurrentAssets"], 
            "total_current_assets" : elem_b["totalCurrentAssets"], 
            "pp_and_e" : elem_b["propertyPlantEquipmentNet"], 
            "goodwill" : elem_b["goodwill"], 
            "intangible_assets" : elem_b["intangibleAssets"], 
            "goodwill_and_intangible_assets" : elem_b["goodwillAndIntangibleAssets"], 
            "long_term_investments" : elem_b["longTermInvestments"], 
            "tax_assets" : elem_b["taxAssets"], 
            "other_non_current_assets" : elem_b["otherNonCurrentAssets"], 
            "total_non_current_assets" : elem_b["totalNonCurrentAssets"], 
            "other_assets" : elem_b["otherAssets"], 
            "total_assets" : elem_b["totalAssets"], 
            "accounts_payable_balance_sheet" : elem_b["accountPayables"], 
            "short_term_debt" : elem_b["shortTermDebt"], 
            "tax_payable" : elem_b["taxPayables"], 
            "deferred_revenue_current" : elem_b["deferredRevenue"], 
            "other_current_liabilities" : elem_b["otherCurrentLiabilities"], 
            "total_current_liabilities" : elem_b["totalCurrentLiabilities"], 
            "long_term_debt" : elem_b["longTermDebt"], 
            "deferred_revenue_non_current" : elem_b["deferredRevenueNonCurrent"], 
            "deferred_tax_liabilities_non_current" : elem_b["deferredTaxLiabilitiesNonCurrent"], 
            "other_non_current_liabilities" : elem_b["otherNonCurrentLiabilities"], 
            "total_non_current_liabilities" : elem_b["totalNonCurrentLiabilities"], 
            "other_liabilities" : elem_b["otherLiabilities"], 
            "capital_lease_obligations" : elem_b["capitalLeaseObligations"], 
            "total_liabilities" : elem_b["totalLiabilities"], 
            "preferred_stock" : elem_b["preferredStock"], 
            "common_stock" : elem_b["commonStock"], 
            "retained_earnings" : elem_b["retainedEarnings"], 
            "accumulated_other_comprehensive_income_loss" : elem_b["accumulatedOtherComprehensiveIncomeLoss"], 
            "other_total_stockholders_equity" : elem_b["othertotalStockholdersEquity"], 
            "total_stockholders_equity" : elem_b["totalStockholdersEquity"], 
            "total_liabilities_and_stockholders_equity" : elem_b["totalLiabilitiesAndStockholdersEquity"], 
            "minority_interest" : elem_b["minorityInterest"], 
            "total_equity" : elem_b["totalEquity"], 
            "total_liabilities_and_equity" : elem_b["totalLiabilitiesAndTotalEquity"], 
            "total_investments" : elem_b["totalInvestments"], 
            "total_debt" : elem_b["totalDebt"], 
            "net_debt" : elem_b["netDebt"], 

            "net_income_cash_flow" : elem_c["netIncome"],
            "depreciation_and_amortization_cash_flow" : elem_c["depreciationAndAmortization"], 
            "deferred_income_tax" : elem_c["deferredIncomeTax"], 
            "stock_based_compensation" : elem_c["stockBasedCompensation"], 
            "change_in_working_capital" : elem_c["changeInWorkingCapital"], 
            "accounts_receivables_cash_flow" : elem_c["accountsReceivables"], 
            "inventory_cash_flow" : elem_c["inventory"], 
            "accounts_payable_cash_flow" : elem_c["accountsPayables"], 
            "other_working_capital" : elem_c["otherWorkingCapital"], 
            "other_non_cash_items" : elem_c["otherNonCashItems"], 
            "net_cash_provided_by_operating_activities" : elem_c["netCashProvidedByOperatingActivities"], 
            "investments_in_PP_and_E" : elem_c["investmentsInPropertyPlantAndEquipment"], 
            "aquisitions_net" : elem_c["acquisitionsNet"], 
            "purchase_of_investments" : elem_c["purchasesOfInvestments"], 
            "sales_maturities_of_investments" : elem_c["salesMaturitiesOfInvestments"], 
            "other_investing_activities" : elem_c["otherInvestingActivites"], 
            "net_cash_used_for_investing_activities" : elem_c["netCashUsedForInvestingActivites"], 
            "debt_repayment" : elem_c["debtRepayment"], 
            "common_stock_issued" : elem_c["commonStockIssued"], 
            "common_stock_repurchased" : elem_c["commonStockRepurchased"], 
            "dividens_paid" : elem_c["dividendsPaid"], 
            "other_financing_activities" : elem_c["otherFinancingActivites"], 
            "net_cash_used_for_financing_activities" : elem_c["netCashUsedProvidedByFinancingActivities"], 
            "effects_of_forex_changes_on_cash" : elem_c["effectOfForexChangesOnCash"], 
            "net_change_in_cash" : elem_c["netChangeInCash"], 
            "cash_at_the_end_of_period" : elem_c["cashAtEndOfPeriod"], 
            "cash_at_the_beginning_of_period" : elem_c["cashAtBeginningOfPeriod"], 
            "operating_cash_flow" : elem_c["operatingCashFlow"], 
            "capex" : elem_c["capitalExpenditure"], 
            "free_cash_flow" : elem_c["freeCashFlow"],
            
        }   

        Company_Fundamentals.objects.update_or_create(id = ticker + "_" + elem_i["calendarYear"], defaults = updated_values)
            

    # TODO: UPDATE NET DEBT & SHARES OUTSTANDING to use quarterly data

   

    # Fill the missing data on the basic info
    company_object = Company.objects.get(ticker=ticker)
    company_fundamentals_object = Company_Fundamentals.objects.filter(company_id=ticker).order_by('year')[0]

    company_object.enterprise_value = company_object.market_cap + company_fundamentals_object.net_debt


    company_object.save()

    return


