import requests
import yaml
import csv

# Membuka file config.yaml dan mengambil channel ID dan token
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
channel_id = config['channel_id']
token = config['token']

headers = {
    'Authorization': token,
}

response = requests.get(f'https://discord.com/api/channels/{channel_id}/messages', headers=headers, params={'limit': 100})

if response.status_code != 200:
    print(f'Error with status code {response.status_code}: {response.text}')
else:
    messages = response.json()

    # Membuka file CSV untuk menyimpan pesan
    with open('messages.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Author", "Message", "Date"])

        # Menulis pesan ke file CSV
        for message in messages:
            writer.writerow([message['author']['username'], message['content'], message['timestamp']])