
from flask import Flask, request
import requests
import json
import discord
import tensorflow as tf
from stable_diffusion import ImageGen

app = Flask(__name__)

@app.route("/", methods=['POST'])
def listener():
    data = request.get_json()
    discord_channel_id = data['channel_id']
    username = data['username']
    text = f"Hey {username}! Please enter your name to play a game of tic-tac-toe against the AI!"
    discord_bot_url = f"https://discordapp.com/api/channels/{discord_channel_id}/messages"
    payload = {
        "content": text
    }
    headers = {
        "Authorization": "bot-toke",
        "Content-Type": "application/json"
    }
    requests.post(discord_bot_url, data=json.dumps(payload), headers=headers)
    # Play tic-tac-toe AI against AI
    game = tf.tictactoe.Game()
    player1 = tf.tictactoe.AiPlayer()
    player2 = tf.tictactoe.AiPlayer()
    game.play([player1, player2])
    winner = game.winner()
    # Generate image of winner using stable diffusion
    image = ImageGen(winner).generate()
    discord_bot_url = f"https://discordapp.com/api/channels/{discord_channel_id}/messages"
    payload = {
        "content": "The winner is...",
        "file": image
    }
    requests.post(discord_bot_url, data=json.dumps(payload), headers=headers)
    return '', 200

if __name__ == "__main__":
    app.run()
