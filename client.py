import json
import requests

from track import Track
from playlist import Playlist

"""Perform operations using spotify api: https://developer.spotify.com/documentation/web-api/"""
class Client:
    def __init__(self, authorization_token, user_id):
        self.authorization_token = authorization_token
        self.user_id = user_id

    """Get the last couple tracks that the user played"""
    """https://developer.spotify.com/documentation/web-api/reference/#/operations/get-users-top-artists-and-tracks"""
    def prev(self, limit=10):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self.get_api(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
            track in response_json["items"]]
        return tracks
    
    """Track recommendations"""
    def recommend(self, seed_tracks, limit=50):
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed-tracks={seed_tracks_url}&limit={limit}"
        response = self.get_api(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for
            track in response_json["items"]]
        return tracks

    def create(self, name):
        data = json.dumps({
            "name" : name,
            "description" : "Recommended tracks",
            "public" : True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self.post_api(url, data)
        response_json = response.json()

        # Create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def add(self, playlist, tracks):
        tracks_url = [track.create_url() for track in tracks]
        data = json.dumps(track_url)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self.post_api(url, data)
        response_json = response.json()
        return response_json

    def post_api(self, url, data):
        response = requests.post(
            url,
            data = data,
            headers = {
                "Content-Type" : "application/json",
                "Authorization" : f"Bearer {self.authorization_token}"
            }
        )

    def get_api(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type" : "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response