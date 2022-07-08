from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from babel.numbers import get_currency_symbol
from .models import Company, Stock_price
from .forms import CompanyForm
from .data_collection import *
from .data_formatter import *



# Create your views here.
def index(request):
    form = CompanyForm(request.POST)
    if "ticker" in form.data:
        ticker = form.data['ticker'].upper()
        #  Redirect to the company page
        return redirect("company", company_id=ticker)

    context = {'form': form}
    return render(request, 'AV_Analytics/index.html', context)

def data_collection(request, message=None):
    form = CompanyForm(request.POST)
    context = {'form': form, 'message': message}
    return render(request, 'AV_Analytics/data_collection.html', context)

def data_analysis(request):
    return HttpResponse("Hello, world. You're at Aether Value's data analysis.")

def company(request, company_id):
    # Try to get it from the database
    try:
        company = Company.objects.get(ticker=company_id)
    except Company.DoesNotExist:
        # Try to get the data from the API
        get_company_data_func(company_id)

        # Try to get it from the database again
        company = get_object_or_404(Company,pk=company_id)

    # Add aditional data to the company
    cof = {}
    cof['change_percentage'] = round((company.change / company.price)*100,2)
    cof['dcf_diff'] = round(((company.dcf / company.price)-1)*100,2)
    cof['currency_symbol'] = get_currency_symbol(company.currency,locale='en_US')
    cof["volume_average"] = round(company.volume_average/1000000,2)
    cof["market_cap"] = round(company.market_cap/1000000000,2)
    cof["enterprise_value"] = round(company.enterprise_value/1000000000,2)
    cof["number_of_employees"] = "{:,}".format(company.number_of_employees)

    # Get the stock fundamentals
    fundamentals_main, fundamentals_growth,  is_df, bs_df, fcf_df, is_growth_df, bs_growth_df, fcf_growth_df, is_cagr_growth_df, bs_cagr_growth_df, fcf_cagr_growth_df,overview_df = get_stock_fundamentals(company_id)

    fundamentals_main = fundamentals_main.to_html(classes='text-sm')
    is_df = is_df.to_html(classes='w-full text-sm')
    bs_df = bs_df.to_html(classes='w-full text-sm')
    fcf_df = fcf_df.to_html(classes='w-full text-sm')

    fundamentals_growth = fundamentals_growth.to_html(classes='text-sm', index=False)
    is_growth_df = is_growth_df.to_html(classes='w-full text-sm', index=False)
    bs_growth_df = bs_growth_df.to_html(classes='w-full text-sm', index=False)
    fcf_growth_df = fcf_growth_df.to_html(classes='w-full text-sm', index=False)

    is_cagr_growth_df = is_cagr_growth_df.to_html(classes='w-full text-sm', index=False)
    bs_cagr_growth_df = bs_cagr_growth_df.to_html(classes='w-full text-sm', index=False)
    fcf_cagr_growth_df = fcf_cagr_growth_df.to_html(classes='w-full text-sm', index=False)

    overview_df = overview_df.to_html(classes='w-full text-sm')


    context = {'company': company,"cof": cof ,'fundamentals_main': fundamentals_main, 'fundamentals_growth': fundamentals_growth, 'is_df': is_df, 'bs_df': bs_df, 'fcf_df': fcf_df, 'is_growth_df': is_growth_df, 'bs_growth_df': bs_growth_df, 'fcf_growth_df': fcf_growth_df, 'is_cagr_growth_df': is_cagr_growth_df, 'bs_cagr_growth_df': bs_cagr_growth_df, 'fcf_cagr_growth_df': fcf_cagr_growth_df, 'overview_df': overview_df}
    return render(request, 'AV_Analytics/company.html', context)
   



def get_company_data(request):
    form = CompanyForm(request.POST)
    print(form)
    ticker = form.data['ticker'].upper()

    # Execute the query
    get_company_data_func(ticker)

    message = "Successfully collected ticker data."
    return redirect("data_collection", message)


def search(request):
    if 'ticker' in request.GET:
        ticker = request.GET['ticker'].upper()
    else:
        ticker = "None_found"

    return redirect("company", company_id=ticker)


