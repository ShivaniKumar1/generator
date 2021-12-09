import os
from client import Client

def main():
    client = Client(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), os.getenv("SPOTIFY_USER_ID"))

    # Last played songs
    songs = int(input("How many songs do you want to see?"))
    last_played = client.prev(songs)
    print(f"\nHere are the last {songs} songs you listened to on Spotify:")
    for index, track in enumerate(last_played):
        print(f"{index + 1} - {track}")

    # Tracks to use to generate playlist
    num = input("\nEnter a list of up to 5 songs you want to use to generate your playlist. Use indexes separated by a space please! Enter:")
    num = num.split()
    seed_tracks = [last_played[int(num)-1] for index in num]

    # Recommended songs
    rec_songs = client.recommend(seed_tracks)

    # Get playlist name and create a playlist
    name = input("\nWhat's the playlist name?")
    playlist = client.create(name)
    print(f"\nPlaylist '{name} was create successfully.")

    # Populate playlist
    client.add(playlist, rec_songs)
    print(f"\nRecommended tracks add to playlist '{name}''.")

    if __name__ == "__main__":
        main()