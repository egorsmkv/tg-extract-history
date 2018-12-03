import logging
import csv

from config import *

from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChannel
from telethon.tl.patched import Message


logging.basicConfig(level=logging.DEBUG)

client = TelegramClient('extraction', API_ID, API_HASH)
client.start()

try:
    raw = client.get_entity(GROUP_URL)
except ValueError as e:
    print(e)
    exit(1)

group = client.get_entity(PeerChannel(raw.id))

with open('data/history.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['User ID', 'Message ID', 'Date', 'Message'])

    for message in client.iter_messages(group.id):
        # игнорируем сообщения, которые не являются непосредственно пользовательскими сообщениями
        if not isinstance(message, Message):
            continue

        strdate = message.date.strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

        writer.writerow([message.from_id, message.id, strdate, message.message])
