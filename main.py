#%%
import copy
import json
from urllib import response
import pandas as pd
from gitter.messages import clear_messages
from gitter.scraper import GitterScraper

scraper = GitterScraper(
    "62fe76c279230fbd70415c924fef5d1b26f1aec7", "555f74e315522ed4b3e0ce42"
)
messages = scraper.get_messages(5, 5)

# print(json.dumps(messages, indent=4, sort_keys=True))

# print(json.dumps(clear_messages(messages), indent=4, sort_keys=True))

df = pd.DataFrame(messages)
print(df.head())
