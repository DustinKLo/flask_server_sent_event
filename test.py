import sys
import requests
from sseclient import SSEClient


headers = {
  'Connection': 'keep-alive',
  'Cache-Control': 'no-cache',
  'accept': 'text/event-stream'
}

r = requests.get('http://localhost:5000/stream', headers=headers, stream=True)
client = SSEClient(r)

for event in client.events():
    print(event.data)
