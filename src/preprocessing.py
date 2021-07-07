## Functions to help parsing data
import io, base64

def parse_coordinates(message):
  lon = message['location']['longitude']; lat = message['location']['latitude']

  if message['edit_date']:
    time = message['edit_date']
  else:
    time = message['date']

  data = [lon, lat, time]
  return data

def fetch_profile_photo(user_id, bot):
  photoData = bot.get_user_profile_photos(user_id)
  fileId = photoData.photos[0][0].file_id
  imageData = bot.get_file(fileId).download_as_bytearray()

  b64image = base64.b64encode(imageData)

  return b64image

def parse_userdata(message, bot):

  #coordinates = parse_coordinates(message)
  b64photo = fetch_profile_photo(message['from_user']['id'], bot)

  data = {
      "uid": message['from_user']['id'],
      "username": message['from_user']['username'],
      "details":{
        "name": {
            "first": message['from_user']['first_name'],
            "last": message['from_user']['last_name']
          },
          "photo": b64photo
        },
      "route": []
      }

  return data
