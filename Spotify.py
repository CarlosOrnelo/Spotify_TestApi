import json
import requests
import urllib
import random
import time
from json.decoder import JSONDecodeError

spotify_token = ''
spotify_user_id = ''


class apiTest:

    def __init__(self):
        self.user_id = spotify_user_id
        self.token = spotify_token
        self.playslit_name = "Teste"
        self.headers = {"Accept": "application/json" ,"Content-Type": "application/json" ,"Authorization": "Bearer {}".format(spotify_token)}

    def search_spotify(self, musica, artista):

        self.songs = musica
        self.artists = artista


        query = f"https://api.spotify.com/v1/search?q=track%3A{self.songs}%20artist%3A{self.artists}&type=track"

        try:
            response = requests.get(query, headers=self.headers)

            data = response.json()

            print(data["tracks"]["items"][0]["uri"])
            return data["tracks"]["items"][0]["uri"]
        
        except IndexError:

            return print("Música não encontrada!")



    def create_playlist_spotify(self):
        
        query_verify = f"https://api.spotify.com/v1/me/playlists"

        response_play = requests.get(query_verify, headers=self.headers)

        for i in enumerate(response_play.json()["items"]):
            if i[1]["name"] == self.playslit_name :
                return i[1]["id"]

        
        request_body = json.dumps({
            "name": self.playslit_name,
            "description": "",
            "public": "True"})

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"


        response = requests.post(query, data=request_body, headers=self.headers)
        
        response_join = response.json()
        return response_join["id"]
    
    def show_playslits(self):

        playlists = {}

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)       
        response = requests.get(query, headers=self.headers)
        for i in response.json()["items"]:
            playlists[i["name"]] = (i["uri"], i["images"][0]["url"], i["id"])
        

        
        return playlists

    
    def add_songs_spotify(self, musica, artista, playlist_id):

        uris = [self.search_spotify(musica, artista)]
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        request_data = json.dumps({"uris": uris})
        response = requests.post(query, data=request_data,headers=self.headers)

    
    def show_songs(self, *args):

        if len(args) > 0:
            self.id = args[0]
        
        musicas = {}

        query = f"https://api.spotify.com/v1/playlists/{self.id}/tracks" 
        
        response_format = requests.get(query, headers=self.headers)
        
        for i in response_format.json()["items"]:
            musicas[i["track"]["name"]] = (i["track"]["artists"][0]["name"], i["track"]["album"]["images"][2]["url"], i["track"]["uri"], self.id)
        

        return musicas
    
    def delete_songs(self, musica, playlist_id):
        
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        uri = musica

        param = {"tracks":[{"uri": uri}]}
        response = requests.delete(query, headers=self.headers, data=json.dumps(param))
        print(response.json())
    
    def play(self, musica, artista, *args):
        
        query = "https://api.spotify.com/v1/me/player/play"


        if len(args) != 0:
            request_body = {"uris": args}
            response_play = requests.put(query, data=json.dumps(request_body), headers=self.headers)
            print(response_play)


        elif musica == "" and artista == "":
            response_play = requests.put(query, headers=self.headers)

            print(response_play.json)

        else:
        
            request_body = {"uris": [self.search_spotify(musica, artista)]}
            response_play = requests.put(query, data=json.dumps(request_body), headers=self.headers)
            print(response_play)

    
    def pause(self):

        query = "https://api.spotify.com/v1/me/player/pause"
        response_pause = requests.put(query, headers=self.headers)
        print(response_pause)
    
    def volume(self, vol):

        query = "https://api.spotify.com/v1/me/player/volume?volume_percent={}".format(vol)
        response_volume = requests.put(query, headers=self.headers)
        print(response_volume)
    
    def next_song(self):
        
        query = "https://api.spotify.com/v1/me/player/next"
        requests.post(query, headers=self.headers)

    def previous_song(self):
        
        query = "https://api.spotify.com/v1/me/player/previous"
        requests.post(query, headers=self.headers)

    def playlist_items(self, id_play):
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(id_play)
        response = requests.get(query, headers=self.headers)

        # Quantidade de músicas da playslit
        quantidade = len(response.json()["items"])

        # uri da primeira música
        uri = response.json()["items"][random.randint(0, quantidade-1)]["track"]["uri"]
       
        self.play("", "", uri)

    def get_current(self):

        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query, headers=self.headers)
        current = response.json()
        retorno = {"inicio": 0, "progresso": current["progress_ms"], "duração": current["item"]["duration_ms"], "nome": current["item"]["name"], 
        "album": current["item"]["artists"][0]["name"], "artista": current["item"]["album"]["name"], "pausada": current["actions"]["disallows"]}


        if retorno["progresso"] < retorno["duração"]:
           
            response = requests.get(query, headers=self.headers)
            current = response.json()
            retorno = {"inicio": 0, "progresso": current["progress_ms"], "duração": current["item"]["duration_ms"], "nome": current["item"]["name"], 
            "artista": current["item"]["artists"][0]["name"], "album": current["item"]["album"]["name"], "pausada": current["actions"]["disallows"],
            "imagem": current["item"]["album"]["images"][2]["url"]}

            return retorno
    
    def get_all(self):

        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(query, headers=self.headers)
        
        try:
            current = response.json()
            retorno = {"volume": current["device"]["volume_percent"], "inicio": 0, "progresso": current["progress_ms"], "duração": current["item"]["duration_ms"],
                    "musica": current["item"]["name"], "album": current["item"]["album"]["name"], "artista": current["item"]["artists"][0]["name"],
                    "imagem": current["item"]["album"]["images"][2]["url"], "status": current["actions"]["disallows"]}
            
            return retorno

        except ValueError:
            return None
    
    def search_anything(self, song):

        if song == "":
            pass
        else:
 
            resultado = {}
            self.song = song
            query = f"https://api.spotify.com/v1/search?q={self.song}&type=track&limit=5"
            response = requests.get(query, headers=self.headers)
            conteudo = response.json()
            for i, j in zip(conteudo["tracks"]["items"], range(len(conteudo["tracks"]["items"]))):
                resultado[j] = {"musica": i["name"], "artista": i["artists"][0]["name"], "imagem": i["album"]["images"][2]["url"], "album": i["album"]["name"], "uri": i["uri"]}

            return resultado

teste = apiTest()
