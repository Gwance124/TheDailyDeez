import random

import discord

client = discord.Client()
fileA = open("deez.txt", "r")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    global words
    words = []
    for word in fileA:
        words.append(word.strip())

    fileB = open("allWords.txt", "r")
    fileC = open("deezUnVerified.txt", "r")

    wordsDone = set()
    for word in fileB:
        wordsDone.add(word.strip())
    for word in fileC:
        wordsDone.add(word.strip())

    fileB.close()
    fileC.close()

    for i in reversed(range(len(words))):
        if words[i] in wordsDone:
            words.pop(i)
    random.shuffle(words)

    global channelG
    global lastMsgG
    global wordsIdx
    wordsIdx = 0
    channelG = client.get_channel(1010081117694599218)
    lastMsgG = (await channelG.send(f'Is {words[wordsIdx].strip()} a good deez?')).content
    wordsIdx += 1

@client.event
async def on_message(message):
    global channelG
    global lastMsgG
    global wordsIdx
    if message.author == client.user:
        return

    if message.content.lower() == 'yes' and message.channel.id == 1010081117694599218:
        recentDeez = lastMsgG.split()[1]
        verifiedRead = open('allWords.txt', 'r')
        allWords = open('allWords.txt', 'a')

        ListOfWords = set()
        for word in verifiedRead:
            ListOfWords.add(word.strip())
        if recentDeez not in ListOfWords:
            allWords.write(recentDeez + '\n')
            await message.channel.send(recentDeez + ' added to the deez list!')
        else:
            await message.channel.send('Double Yes You Fucking Donkey!')
            return

        verifiedRead.close()
        allWords.close()

        lastMsgG = (await channelG.send(f'Is {words[wordsIdx].strip()} a good deez?')).content
        wordsIdx += 1
        return

    if message.content.lower() == 'no' and message.channel.id == 1010081117694599218:
        recentDeez = lastMsgG.split()[1]

        unverifiedAppend = open("deezUnVerified.txt", "a")
        unverifiedAppend.write(recentDeez + '\n')
        unverifiedAppend.close()

        lastMsgG = (await channelG.send(f'Is {words[wordsIdx].strip()} a good deez?')).content
        wordsIdx += 1
        return

client.run('MTAwODU0Mjk4NjQ2MTc3Mzk0NQ.Gqqnr0.3M4SvEu6BffnNNZeWzjagxyth3J3oWKwQVxBbM')
fileA.close()
