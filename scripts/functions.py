import requests

def get_tba_data(url):
    try:
        return requests.get("https://www.thebluealliance.com/api/v3/" + url,
                        {"accept": "application%2Fjson",
                         "X-TBA-Auth-Key": "gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ"}).json()
    except:
        print("oops " + url)
        return get_tba_data(url)