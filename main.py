import os
import openai
import socket
import logging
import random
import tkinter as tk
from playsound import playsound
from gtts import gTTS
from emoji import demojize
from random import seed, choice
from string import ascii_letters
from apikeys import openai_key

try:
    os.remove("tts.mp3")
except:
    print('no file to remove')

# OpenAI
openai.organization = "org-Zd4jsfu09jt8giLVCEc1a5XA"
openai.api_key = openai_key
openai.Model.list()

# Twitch chat implementation
token = "oauth:j77bo13weq4z67t0zra3n95bex96nj"
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'verysireagle'
channel = '#sireagle1'

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

# Finals
ADJRANGE = 3

# Responses
def is_negative(chatmsg):
    resp = openai.Completion.create(
        model = "text-davinci-003",
        prompt = f"Yes or no, is the following chat message negative or contains negative words? {chatmsg}?",
        max_tokens = 10,
        temperature = 0.5,
    )
    print(str.lower(resp['choices'][0]['text']))
    return 'y' in str.lower(resp['choices'][0]['text'])

adjectives = []
# Import adjectives from data.txt
with open("data.txt", "r") as f:
    adjectives += [line.strip('\n') for line in f.readlines()]

# Send request to OPENAI
def openAiRequest(promptmsg):
    resp = openai.Completion.create(
        model = "text-davinci-003",
        prompt = promptmsg,
        max_tokens = 120,
        temperature = 0.9,
    )
    return f"{resp['choices'][0]['text']}"

# Generate adjectives
def genpromt(maxadjs, chatmsg):
    prompt_adjs = ""
    if(is_negative(chatmsg)): 
        prompt_adjs += "very very angry, "
        maxadjs -= 1
        if(random.randint(1,10) > 8): 
            prompt_adjs += "rambling, "
            maxadjs -= 1
        else: prompt_adjs += "short, slandering"
    else: prompt_adjs += "short, "
    rand_adjs = random.sample(range(0,len(adjectives)), random.randint(1, maxadjs))
    for adjnum in rand_adjs:
        prompt_adjs += " " +adjectives[adjnum] + ","
    return f" Write a {prompt_adjs}, irritated response from the twitch streamer and god gamer \
                                    named Forsen to the following comment: {chatmsg}?"

# Play TTS
def play_tts(text):
    output = gTTS(text=text, lang="en", tld="co.in")
    output.save(f"tts.mp3")
    playsound("tts.mp3")
    os.remove("tts.mp3")

# Create response for ai
def ai_response_tts(chatmsg):
    prompt = genpromt(ADJRANGE, chatmsg)
    request_response = openAiRequest(prompt).strip('"')
    print(f"Response: {request_response}")
    play_tts(f"{chatmsg}? {request_response}")

#Run
def main():
    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            msg = ""
            try: msg = resp.split(f"{channel} :")[1]
            except: print("Message to short")
            print(msg)
            if(len(msg) > 5 and len(msg) < 70): ai_response_tts(msg)

main()