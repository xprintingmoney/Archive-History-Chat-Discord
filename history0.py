import requests
import yaml
import csv
import time

# Membuka file config.yaml dan mengambil channel ID dan token
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
channel_id = config['channel_id']
token = config['token']

headers = {
    'Authorization': token,
}

# Inisialisasi ID pesan terakhir
last_message_id = None

# Membuka file CSV untuk menyimpan pesan
with open('messages.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Username", "Display Name", "Message", "Date"])

    while True:
        params = {'limit': 100}
        if last_message_id is not None:
            params['before'] = last_message_id

        response = requests.get(f'https://discord.com/api/channels/{channel_id}/messages', headers=headers, params=params)

        if response.status_code != 200:
            print(f'Error with status code {response.status_code}: {response.text}')
            break

        messages = response.json()

        if not messages:
            break  # Break the loop if no more messages

        # Menulis pesan ke file CSV
        for message in messages:
            username = message['author']['username']
            display_name = message['member']['nick'] if 'member' in message and 'nick' in message['member'] else ''
            writer.writerow([username, display_name, message['content'], message['timestamp']])

        # Update ID pesan terakhir
        last_message_id = messages[-1]['id']

        # Sleep for a short while to respect rate limits
        time.sleep(1)