import requests
import json

class YouTubeSearch():
    def __init__(self, search):
        self.search = search

    def __post_search_request(self):
        url = 'https://youtubei.googleapis.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
        json_obj = {
        "query": self.search,
        "context": {
            "client": {
                "hl": "en",
                "gl": "US",
                "clientName": "ANDROID",
                "clientVersion": "16.02"
                }
            }
        }
        req = requests.post(url, json=json_obj)
        #print('__post_search_request response: ' + str(req.status_code))
        return [True, req.text] if req.status_code == 200 else [False, '']
    
    def get_first_result(self):
        [request_success, search_response] = self.__post_search_request()
        if request_success == True:
            json_response = json.loads(search_response)

            result_count = json_response['estimatedResults']

            contents = json_response["contents"]
            sectionListRenderer = contents['sectionListRenderer']
            itemSectionRenderer = sectionListRenderer['contents'][0]['itemSectionRenderer']
            result1 = itemSectionRenderer['contents'][1]['compactVideoRenderer']['videoId']
            return str(result1)
