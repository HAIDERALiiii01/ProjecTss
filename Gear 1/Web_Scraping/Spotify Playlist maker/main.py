import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64

client_id = "your spotify id here"
client_secret = "your spoitfy secret here"
redirect_url = "https://example.com/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_url,
    scope="ugc-image-upload playlist-modify-private"
))

user_id = sp.current_user()["id"]  # type: ignore

def playlist_maker():
    playlist = sp.user_playlist_create(
        user=user_id,
        name="BEsT of 2021",
        public=False,
    )
    print("Playlist created!")
    print("Name:", playlist["name"]) # type: ignore
    print("ID:", playlist["id"]) # type: ignore
    print("URL:", playlist["external_urls"]["spotify"]) # type: ignore

    return playlist["id"] # type: ignore

def image_upload():
    with open("2021.jpeg", "rb") as f:
        image = base64.b64encode(f.read())
    sp.playlist_upload_cover_image(playlist_id, image)
    print("Cover updated")

# Read songs from file
# Read songs from file (now includes artists)
songs = []
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        song = line.strip()
        if song:
            songs.append(song)

# Search and add to playlist
def uri_finder():
    uri_list = []
    for s in songs:
        print(f"Searching: {s}")
        results = sp.search(q=s, type="track", limit=1)
        tracks = results["tracks"]["items"] # type: ignore
        if tracks:
            uri = tracks[0]["uri"]
            uri_list.append(uri)
            sp.playlist_add_items(playlist_id, [uri])
            print(f"✅ Added: {s}")
        else:
            print(f"❌ Not found: {s}")
    
    with open("uri.txt", "w", encoding="utf-8") as f:
        for u in uri_list:
            f.write(f"{u}\n")

playlist_id = playlist_maker()
image_upload()
uri_finder()

