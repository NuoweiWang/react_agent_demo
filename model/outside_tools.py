import os, json
import requests

"""
工具函数

- 首先要在 tools 中添加工具的描述信息
- 然后在 tools 中添加工具的具体实现

- https://serper.dev/dashboard
"""

class Tools:
    def __init__(self) -> None:
        self.toolConfig = self._tools()
    
    def _tools(self):
        TOOLS = [
            {
                'name_for_model': 'Search',
                'name_for_human': 'Google Search API',
                'description_for_model': 'Use the Google Search API to fetch data relevant to current events and specific queries.',
                'parameters': [
                    {
                        'name': 'query',
                        'type': 'string',
                        'description': 'The search query to send to Google.',
                        'required': True
                    }
                ]
            }
        ]
        return TOOLS

    def google_search(self, search_query: str):
        url = "https://google.serper.dev/search"

        payload = json.dumps({"q": search_query})
        headers = {
            'X-API-KEY': 'your-key',
            'Content-Type': 'application/json'
        }

        answer = ""
        response = requests.request("POST", url, headers=headers, data=payload).json()
        response = response['organic']
        len_ = 3 if len(response) > 3 else len(response)

        for i in range(0,len_):
            answer += f"{i+1}." + response[i]['snippet'] + "\n"

        return answer





