import PIL
from PIL import Image
import io

import requests

from googleapiclient.discovery import build
import authinfo

# Maximum content size to fetch - VGA 24 bit + overhead
MAXIMUM_CONTENT_SIZE = int(640*480*3*1.10)

def isSmallContent(url):
    header = requests.head(url, allow_redirects=True).headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        print("content-type: {}".format(content_type))
        return False
    content_length = int(header.get('content-length') or MAXIMUM_CONTENT_SIZE+1)
    if content_length > MAXIMUM_CONTENT_SIZE:
        print("content-length: {}".format(content_length))
        return False
    return True

def display(image_stream):
    image = Image.open(image_stream)
    image = image.resize((640, 480))

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey=authinfo.developer_key)

  res = service.cse().list(
      q='pretty bird movie',
      searchType = "image",
      cx=authinfo.ctx
    ).execute()

  if not 'items' in res:
      print("No result !!\nres is: {}".format(res))
  else:
      for item in res['items']:
          image_url = item['link']
          if not image_url or not isSmallContent(image_url):
            print("Skipping {}".format(item['link'].encode('utf-8')))
            continue
          print("Fetching {} from {}".format(item['title'].encode('utf-8'), item['link'].encode('utf-8')))
          image_stream = requests.get(image_url, stream=True, allow_redirects=True).raw
          display(image_stream)
main()
