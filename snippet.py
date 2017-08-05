import requests

from googleapiclient.discovery import build
import authinfo

def isContent(url):
    header = requests.head(url, allow_redirects=True).headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        print("content-type: {}".format(content_type))
        return False
    return True

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
          if not image_url or not isContent(image_url):
            print("Skipping {}".format(item['link'].encode('utf-8')))
            continue
          print("Fetching {} from {}".format(item['title'].encode('utf-8'), item['link'].encode('utf-8')))
          image = requests.get(image_url, allow_redirects=True)
main()
