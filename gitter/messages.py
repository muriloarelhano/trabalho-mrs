from copy import copy
from bs4 import BeautifulSoup

def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script', 'a', 'code']):
        data.decompose()
  
    return ' '.join(soup.stripped_strings)

def process_messages(messages):
    copy_messages = copy(messages)
    for idx, message in enumerate(copy_messages):
        try:
            # Remove "\" from original message, this is a gitter problem
            message["html"] = message["html"].replace('\\', "")
            # Remove all tags for get only pure text
            messages[idx]["html"] = remove_tags(message["html"])
            for key in list(message):
                if type(message[key]) == dict or type(message[key]) == list:
                    del messages[idx][key]
        except:
            print('Erro com campo HTML no gitter: ', message)
            break
        
    return messages