# api key = AIzaSyDs5mHfyDCSZQKpU93eY9IS2MjezMGK6i0
from googleapiclient.discovery import build
pl_teste = "PL_k85dQbxntI9WoJlCINzBw0595MlbkAX"


def get_yt_playlist_items(playlist_id, api_key="AIzaSyDs5mHfyDCSZQKpU93eY9IS2MjezMGK6i0"):
    lista_items = []
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_items = youtube.playlistItems().list(playlistId=playlist_id, part="snippet", maxResults=50).execute()
    for item in playlist_items['items']:
        lista_items.append(item['snippet']['title'])
    return lista_items


if __name__ == "__main__":
    print(get_yt_playlist_items(pl_teste))
