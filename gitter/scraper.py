import math
import requests


class GitterScraper:
    def __init__(self, api_token, room_id):
        self.api_token = api_token
        self.room_id = room_id
        self.base_url = "https://api.gitter.im/v1"

    def get_messages(self, limit=100, total_messages=1000):
        all_messages = []
        count = 0
        acc_last_response_length = 0
        have_more_messages = True
        
        while (count <= math.ceil(total_messages / limit)) and have_more_messages:
            response = requests.get(
                f"{self.base_url}/rooms/{self.room_id}/chatMessages",
                headers={"Authorization": f"Bearer {self.api_token}"},
                params={"limit": limit, "skip": acc_last_response_length},
            ).json()
            acc_last_response_length += len(response)
            all_messages.extend(response)
            if len(response) < 100 or len(response) == 0:
                have_more_messages = False
            count += 1
        return all_messages

    def get_user_rooms(self):
        return requests.get(
            f"{self.base_url}/rooms",
            headers={"Authorization": f"Bearer {self.api_token}"},
        ).json()

