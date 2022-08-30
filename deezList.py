import time
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1010379358743040102)
    oldListOfWords = set()
    alreadyListedDeezRead = open('alreadyListedDeez.txt', 'r')
    for word in alreadyListedDeezRead:
        oldListOfWords.add(word.strip())
    alreadyListedDeezRead.close()
    wordNum = len(oldListOfWords) + 1
    while True:
        newListOfWords = open('allWords.txt', 'r')
        alreadyListedDeezAppend = open('alreadyListedDeez.txt', 'a')
        for word in newListOfWords:
            if word.strip() not in oldListOfWords:
                oldListOfWords.add(word.strip())
                alreadyListedDeezAppend.write(word.strip() + '\n')
                await channel.send(f'{wordNum}. {word.strip()}')
                wordNum += 1
        alreadyListedDeezAppend.close()
        newListOfWords.close()
        time.sleep(30)

client.run('TOKEN')
