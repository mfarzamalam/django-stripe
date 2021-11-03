import requests
url = "https://mfarzamalam.cafe24api.com/api/v2/products?brand_code=B000000A&price_min=1000"
payload = '''grant_type=refresh_token&refresh_token={refresh_token}'''
headers = {
    'Authorization': "Basic {base64_encode({client_id}:{client_secret})}",
    'Content-Type': "application/x-www-form-urlencoded"
    }
response = requests.request("GET", url)
print(response.text)
