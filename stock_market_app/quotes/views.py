from django.shortcuts import render

def home(request):
  # iexcloud key: pk_29b131419c054b429aa9bf1f49b93cf6
  import requests
  import json
  
  api_request = requests.get(
    "https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_29b131419c054b429aa9bf1f49b93cf6"
  )

  try:
    api = json.loads(api_request.content)
  except Exception as e:
    api = "Error..."

  return render(request, 'home.html', {'api': api})


def about(request):
  return render(request, 'about.html', {})
