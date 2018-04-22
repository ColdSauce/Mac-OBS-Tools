import requests
import time
from PIL import Image, ImageDraw, ImageFont

origin = 'https://open.spotify.com'
headers = {'Origin': origin}

font = ImageFont.truetype('/Library/Fonts/Verdana Bold.ttf', 16)

oauth_endpoint = origin + '/token'

localhost = 'http://127.0.0.1:'
spotify_port = ''
oauth = ''
csrf = ''


# Determine what port the local spotify server is listening on
def identify_spotify_port():
    global spotify_port
    port = 4379
    response_code = 0
    version_endpoint = '/service/version.json'

    while response_code != requests.codes.ok:
        port += 1
        if port > 4400:  # Not actually sure what port range Spotify uses
            print("Could not communicate with local Spotify server\n")
            raise SystemExit

        spotify_local = localhost + str(port) + version_endpoint

        try:
            response = requests.get(spotify_local, timeout=0.001)
            response_code = response.status_code
        except requests.exceptions.Timeout:
            response_code = 0
        except requests.exceptions.ConnectionError:
            response_code = 0

    spotify_port += str(port)


# Grab oauth token from spotify
def get_oauth_token():
    global oauth
    oauth_response = requests.get(oauth_endpoint)
    json = oauth_response.json()
    oauth += json['t']


# Grab CSRF token from local spotify server
def get_csrf_token():
    global csrf
    spotify_local = localhost + spotify_port
    params = ('/simplecsrf/token.json?cors=&ref=https%3A%2F%2Fopen.spotify.com'
              '%2Fembed%3Furi%3Dspotify%3Aalbum%3A1DFixLWuPkv3KT3TnV35m3')
    csrf_endpoint = spotify_local + params
    csrf_response = requests.get(csrf_endpoint, headers=headers)

    json = csrf_response.json()

    csrf = json['token']


# Query server for details about currently playing track
# Returns song title, album, and artist
def get_current_play():
    global oauth, csrf
    spotify_local = localhost + spotify_port
    params = '/remote/status.json?oauth=' + oauth + '&csrf=' + csrf
    status_endpoint = spotify_local + params
    status_response = requests.get(status_endpoint, headers=headers)

    json = status_response.json()

    song = 'Song: ' + json['track']['track_resource']['name']
    artist = 'Artist: ' + json['track']['artist_resource']['name']
    album = 'Album: ' + json['track']['album_resource']['name']

    play = [song, album, artist]

    return play


# Draws a gray banner every 1 second containing
# the currently playing song's details
def draw_banner():
    global font, banner

    while True:
        play = get_current_play()

        char_length = max([len(play[0]), len(play[1]), len(play[2])])
        
        b_height = 100
        b_width = 11*char_length

        banner = Image.new('RGB', (b_width, b_height), color='gray')
        draw = ImageDraw.Draw(banner)

        track_info = (play[0] + '\n' +
                      play[1] + '\n' + play[2])
        w, h = draw.textsize(track_info, font=font)
        text_x = (b_width - w) / 2
        text_y = (b_height - h) / 2

        draw.text((text_x, text_y),
                  track_info,
                  font=font,
                  fill=(255, 255, 255))
        banner.save('currently_playing.png')
        time.sleep(1)


if __name__ == '__main__':
    identify_spotify_port()
    get_oauth_token()
    get_csrf_token()

    draw_banner()
