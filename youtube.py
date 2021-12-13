from typing import Any
from js2py.base import This
from js2py.translators.friendly_nodes import BREAK_LABEL
import requests
import json
from enum import Enum

audio_itag_by_rating = [251, 140, 250, 249, 139]
video_itag_by_rating = [278, 160, 242, 133, 243, 134, 244, 135, 247, 136, 248, 137, 17, 18, 22]

class YouTubeSource():
    def __init__(self, video_id):
        self.video_id = str(video_id).split('v=')[1] if 'v=' in video_id else video_id # Seperate video_id from http link if it is one
        self.video_link = 'https://www.youtube.com/watch?v=' + self.video_id # Create standard youtube link

    def __is_valid_format(self, format):
        return True if 'contentLength' in format and int(format['contentLength']) <= 50000000 else False
            
    def __get_best_media_format(self): # Check for audio formats before falling back to video
        for itag in audio_itag_by_rating:
            if itag in self.valid_media_formats:
                return itag

        for itag in video_itag_by_rating:
            if itag in self.valid_media_formats:
                return itag                
        return None

    def __extract_media_format_data(self, json_raw):
        json_parsed = json.loads(json_raw)
        video_details = json_parsed['videoDetails']

        self.video_title = video_details['title']
        self.video_length = video_details['lengthSeconds']

        self.valid_media_formats = {}
        self.valid_format_count = 0
        streaming_data = json_parsed['streamingData']
        formats = streaming_data['formats'] if 'formats' in streaming_data else None
        adaptive_formats = streaming_data['adaptiveFormats'] if 'adaptiveFormats' in streaming_data else None
        
        if formats != None:
            for format in formats:
                if self.__is_valid_format(format) == True:
                    self.valid_media_formats[format['itag']] = { 'url' : format['url'], 'content_length' : format['contentLength'] }
                    self.valid_format_count += 1
        
        if adaptive_formats != None:
            for format in adaptive_formats:
                if self.__is_valid_format(format) == True:
                    self.valid_media_formats[format['itag']] = { 'url' : format['url'], 'content_length' : format['contentLength'] }
                    self.valid_format_count += 1
        
    def __request_video_data(self):
        url = 'https://youtubei.googleapis.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
        json_obj = {
        "videoId": self.video_id,
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
        #print('__request_video_data response: ' + str(req.status_code))
        return [True, req.text] if req.status_code == 200 else [False, '']

    def extract_video_data(self):
        [request_success, video_data_raw] = self.__request_video_data()
        if request_success == True:
            self.__extract_media_format_data(video_data_raw)
            return True
        else:
            return False

    def get_best_stream_link(self):
        if self.extract_video_data() == True:
            itag = self.__get_best_media_format()
            if itag != None:
                return self.valid_media_formats[itag]['url']
            else:
                return None


# Hardcoded itag values
'''
itag_def = {
    249 : { 'media_format' : 'audio',
            'media_container' : 'webm',
            'audio_codec' : 'opus',
            'audio_quality' : 'AUDIO_QUALITY_LOW'            
    },
    250 : { 'media_format' : 'audio',
            'media_container' : 'webm',
            'audio_codec' : 'opus',
            'audio_quality' : 'AUDIO_QUALITY_LOW'            
    },
    251 : { 'media_format' : 'audio',
            'media_container' : 'webm',
            'audio_codec' : 'opus',
            'audio_quality' : 'AUDIO_QUALITY_MEDIUM'
    }
}
'''

