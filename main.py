from flask import Flask, render_template, url_for, request, redirect, jsonify
import Spotify
import json

playlist = ""

app = Flask(__name__)


spotify = Spotify.apiTest()


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():

    return render_template("home.html", values=spotify.show_playslits())
    

@app.route("/add", methods=["POST", "GET"])
def add():
    
    global playlist

    if playlist == "":
        playlist = request.form["playName"]
    
    else:
    
        if request.method == "POST":

            try:
                playlist = request.form["playName"]
            
            except KeyError: 
    
                musica = request.form.get("musica")
                artista = request.form.get("artista")
                

                if request.form["SubmitButton"] == "Adicionar":
                    spotify.add_songs_spotify(musica, artista, playlist)

            return render_template("add.html", passed_songs = spotify.show_songs(playlist), current=spotify.get_all())
   
    return render_template("add.html", passed_songs = spotify.show_songs(playlist), id_playlist=playlist, current=spotify.get_all())


@app.route("/volume", methods=["POST", "GET"])
def alter_volume():
   
    if request.method == "POST":
        volume = request.form["volume"]
        spotify.volume(volume)
    
    return volume


@app.route("/play", methods=["POST", "GET"])
def play():

    try:
        uri_musica = request.form["variavel"]
        print(uri_musica)
        spotify.play("", "", uri_musica)
        return redirect(url_for("add"))
    except KeyError:
        spotify.play("", "")        
        return redirect(url_for("add"))


@app.route("/pause", methods=["POST"])
def pause():

    if request.method == "POST":
        spotify.pause()
        return redirect(url_for("add"))

@app.route("/search", methods=["POST", "GET"])
def search():

    pesquisa = request.form["pesquisa"]
    musica = spotify.search_anything(pesquisa)
    return render_template("home.html", values=spotify.show_playslits(), actual=musica)

@app.route("/remove", methods=["POST", "GET"])
def remove():

    musica = request.form.get("variavel")
    playlist = request.form["variavelPlay"]
    spotify.delete_songs(musica, playlist)
    
    return redirect(url_for("add"))


if __name__ == "__main__":
    app.run(debug=True)


