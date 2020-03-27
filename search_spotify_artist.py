import os
import sys
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials
lista_teste = ['Sicko Mode', 'ButterFly Effect', "God's Plan"]


def pesquisa_musica_spotify(musicas):
    musicas_encontradas = []
    username = sys.argv[0]
    dict_playlists = []
    id_musicas = []
    try:
        id_client = "1d9037116098431eaf72e340c49fcad5"
        secret_client = "ecbe9e2acdee4270997940bcebbfba7b"
        redirect = "https://google.com.br"
        token = util.prompt_for_user_token(
            username,
            client_id=id_client,
            client_secret=secret_client,
            redirect_uri=redirect,
            scope="playlist-modify-public"
        )
    except:
        token = util.prompt_for_user_token(username)
        return Exception("Erro no processamento, operação cancelada")
    try:
        spotify = spotipy.Spotify(auth=token)
        current_user = spotify.current_user()
    except:
        return Exception("Erro na validação do token, tente novamente")

    try:
        for item in musicas:
            busca = spotify.search(q=item, limit=1, type="track", offset=0)
            musicas_encontradas.append(busca)
            id_musicas.append(busca['items'][0]['id'])
        with open("jsonteste.json", mode="w") as arquivo:
            arquivo.write(json.dumps(musicas_encontradas, indent=4, sort_keys=True))
            arquivo.close()
    except:
        return Exception("Erro na importação das músicas")

    print(f"Olá {current_user['display_name']} bem vindo ao Botify!")
    while True:
        operacao = input(
            ">>>Deseja criar uma nova playlist ou adicionar as músicas em uma playlist existente? \n"
            ">>>Digite 'n' para criar uma nova ou 'e' para usar uma já existente. Para cancelar o processo digite \n"
        ).strip().lower()
        if operacao not in ('e', 'x', 'n'):
            print(f'{operacao} não é uma operação válida')
        else:
            if operacao == 'x':
                print('cancelando processo... \n Processo cancelado!')
                exit()
            if operacao == 'n':
                print('>>> Criando nova playlist')
                nome = input('>>>Digite o nome da nova playlist ').strip()
                descricao = input('>>>Digite a descricao da nova playlist ')
                spotify.user_playlist_create(user=current_user['id'], name=nome, description=descricao, public=True)
            lista_playlist = spotify.current_user_playlists(limit=50, offset=0)
            for playlist in lista_playlist['items']:
                dict_playlists.append({"nome": playlist['name'], "id": playlist['id']})
            i = 0
            for usuario_playlist in dict_playlists:
                print(f"{usuario_playlist['nome']} - {i} ")
                i += 1
            while True:
                playlist_index = int(input(">>> Digite o número da playlist para adicionar as músicas\n"))
                if playlist_index not in range(len(dict_playlists)):
                    print('Código inválido')
                else:
                    playlist_selecionada = dict_playlists[playlist_index]
                    break
            print(f">>> playlist selecionada: {playlist_selecionada['nome']} \n"
                  f">>> Inserindo músicas...")
            try:
                spotify.user_playlist_add_tracks(
                    user=current_user['id'],
                    playlist_id=playlist_selecionada['id'],
                    tracks=id_musicas
                )
            except:
                return Exception('Erro na inserção de músicas, abortando processo')
            return musicas_encontradas


if __name__ == '__main__':
    (pesquisa_musica_spotify(lista_teste))
