import ../authinfo
def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey=authinfo.developer_key

  res = service.cse().list(
      q='tuna`',
      cx=authinfo.ctx
    ).execute()
  pprint.pprint(res)
