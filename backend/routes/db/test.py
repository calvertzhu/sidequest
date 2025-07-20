import requests

url = "https://www.eventbrite.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "code": "TCVQFCGCUYJ5UNM3EM76",  # your received code
    "client_id": "GU35G22VTHWYR4I4SV",
    "client_secret": "3VPEIHLQ5VWUP54JNWZCDFN2Z7VCICQGPO7RIMJQEO72XLFPQV",  # get from Eventbrite dashboard
    "redirect_uri": "http://127.0.0.1:5000/callback"
}

response = requests.post(url, data=data)
print(response.json())
