import random
import time
import requests


headers = {

    'Content-Type': 'application/json',
    'Referer': 'https://bot.dragonz.land/',
}


def load_credentials():

    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return [  ]
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return [  ]

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'


def getme(query):
    url = 'https://bot.dragonz.land/api/me'
    headers['X-Init-Data'] = query

    response = requests.get(url, headers=headers)
    try:
        response_codes_done = range(200, 211)
        response_code_failed = range(500, 530)
        response_code_notfound = range(400, 410)
        
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_failed:
            print(response.text)
            return None
        elif response.status_code in response_code_notfound:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None
    
def feed(query, feed):
    url = 'https://bot.dragonz.land/api/me/feed'
    headers['X-Init-Data'] = query
    payload = {'feedCount' : feed}
    response = requests.post(url, headers=headers, json=payload)
    print(response)
    try:
        response_codes_done = range(200, 211)
        response_code_failed = range(500, 530)
        response_code_notfound = range(400, 410)
        
        if response.status_code in response_codes_done:
            return "DONE"
        elif response.status_code in response_code_failed:
            print(response.text)
            return None
        elif response.status_code in response_code_notfound:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def main():
    while True:
        queries = load_credentials()
        for index, query in enumerate(queries):
            useragent = getuseragent(index)
            headers['User-Agent'] = useragent
            print(f"========= Account {index+1} =========")
            data_getme = getme(query)
            if data_getme is not None:
                first_name = data_getme.get('firstName')
                last_name = data_getme.get('lastName')
                energy = data_getme.get('energy')
                print(f"Name : {first_name} {last_name} | Energy : {energy}")
                while True:
                    time.sleep(2)
                    feeds = random.randint(100, 200)
                    if energy < feeds:
                        feeds = energy
                    data_feed = feed(query, feeds)
                    if data_feed is not None:
                        print(f"Feeds {feeds} Clicks")
                        energy -= feeds
                    if energy <= 10:
                        break
            else:
                print(f'Error getting data')
        break


main()