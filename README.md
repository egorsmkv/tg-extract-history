With this project you can download all messages from a Telegram's group and save them into a CSV file.

#### Installing

Before running commands you must install **pipenv** (for example, like this: `pip3 install pipenv`).
pipenv will create a Python's virtual environment and downloaded all dependencies.

```shell
git clone https://github.com/egorsmkv/tg-extract-history
cd tg-extract-history
pipenv install
pipenv shell
```

#### Obtain API_ID and API_HASH credentials

You can obtain them at this website - https://my.telegram.org/

#### Usage

> **Note**: at the first run, you must enter a phone number and code that will be send to the Telegram application.

Available parameters of the CLI:

```shell
$ python extractor.py --help

Usage: extractor.py [OPTIONS]

Options:
  --debug BOOLEAN        Enable logging
  --filename TEXT        Filename where the extractor writes the group log
  --group TEXT           Group for extraction  [required]
  --offset-id INTEGER    Offset message ID
  --save-offset BOOLEAN  Enable saving offset value into a file
  --api-id TEXT          [required]
  --api-hash TEXT        [required]
  --help                 Show this message and exit.
```

Download all messages from the group about Python:

```shell
$ python extractor.py --api-id 00001 --api-hash xxxxyyyzzz --group Python --filename python_group.csv
```
