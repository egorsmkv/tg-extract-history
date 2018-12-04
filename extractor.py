import os
import logging
import csv

from click import command, option

from telethon import TelegramClient, events, sync
from telethon.tl.types import Channel, PeerChannel
from telethon.tl.patched import Message

FILENAME = './last_offset'


def set_last_offset(value):
    with open(FILENAME, 'w') as handle:
        handle.write(value)


def get_last_offset():
    if not os.path.exists(FILENAME):
        return 0
    with open(FILENAME, 'r') as handle:
        val = handle.read()
        if not val:
            return 0
        return int(val)


@command()
@option('--debug', type=bool, default=True, help='Enable logging')
@option('--filename', default='history.csv', help='Filename where the extractor writes the group log')
@option('--group', help='Group for extraction', required=True)
@option('--offset-id', type=int, default=0, help='Offset message ID')
@option('--save-offset', type=bool, default=False, help='Enable saving offset value into a file')
@option('--reset-downloading', type=bool, default=False, help='It takes an offset value from the file and append new messages into specified file.')
@option('--api-id', required=True)
@option('--api-hash', required=True)
def run(debug, filename, group, offset_id, save_offset, reset_downloading, api_id, api_hash):
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    client = TelegramClient('extraction', api_id, api_hash)
    client.start()

    try:
        raw = client.get_entity(group)
        if not isinstance(raw, Channel):
            exit('It is not a group')
        if not raw.megagroup:
            exit('It is not a megagroup')
    except ValueError as e:
        exit(e)

    channel = client.get_entity(PeerChannel(raw.id))

    mode = 'w'
    if reset_downloading:
        mode = 'a'
        offset_value = get_last_offset()
    else:
        offset_value = offset_id

    with open(filename, mode=mode) as handle:
        writer = csv.writer(handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not reset_downloading:
            writer.writerow(['User ID', 'Message ID', 'Date', 'Message'])

        for item in client.iter_messages(channel.id, offset_id=offset_value):
            # ignore messages that are not directly users' messages
            if not isinstance(item, Message):
                continue

            strdate = item.date.strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
            writer.writerow([item.from_id, item.id, strdate, item.message])

            if reset_downloading:
                set_last_offset(str(item.id))


if __name__ == '__main__':
    run()
