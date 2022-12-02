from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Stock
from .forms import StockForm

def home(request):
  import requests
  import json
  
  # If user searches for a ticker in the navbar or clicks on the table
  if request.method == 'POST':
    ticker = request.POST['ticker']
    
    iexcloud_key = 'pk_29b131419c054b429aa9bf1f49b93cf6'
    
    api_request = requests.get(
      "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=" + iexcloud_key + ""
    )

    try:
      api = json.loads(api_request.content)
    except Exception as e:
      api = "Error..."
      
    return render(request, 'home.html', {'api': api})
    
  else: 
    companies_data = []
    
    with open("C:/Development/projects/mine/django_stock/stock_market_app/quotes/static/tickers.txt") as tickers_file:
      for line in tickers_file:
        line_parts = line.split(',')
        
        company_ticker = line_parts[0]
        company_name = line_parts[1]
        company_industry = line_parts[2]
        
        company_data = {"ticker": company_ticker, "name": company_name, "industry": company_industry}
        companies_data.append(company_data)
      
    return render(request, 'home.html', {'companies_data': companies_data})

  
def about(request):
  return render(request, 'about.html', {})


def add_stock(request):
  import requests
  import json
  
  iexcloud_key = 'pk_29b131419c054b429aa9bf1f49b93cf6'
  
  if request.method == 'POST':
    form = StockForm(request.POST or None)
    
    if form.is_valid():
      form.save()
      messages.success(request, ("Stock has been added!"))
      return redirect('add_stock')
    
  else:
    ticker = Stock.objects.all()
    output = []
    
    for ticker_item in ticker:
      api_request = requests.get(
        "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=" + iexcloud_key + ""
      )

      try:
        api = json.loads(api_request.content)
        output.append(api)
      except Exception as e:
        api = "Error..."
    
    return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete_stock(request):
  ticker = Stock.objects.all()
  return render(request, 'delete_stock.html', {'ticker': ticker})
  

def delete(request, stock_id):
  item = Stock.objects.get(pk=stock_id)
  item.delete()
  messages.success(request, ("Stock has been deleted!"))
  return redirect(delete_stock)
  