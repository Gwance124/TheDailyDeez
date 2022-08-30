from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
import discord
import asyncio
import random
import datetime
from pytz import timezone
import warnings

client = discord.Client()

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  asyncio.create_task(loopStart())
  

currentSearchMessage = None
currentSendMessage = None
lugungumSearchMessage = None
currentDeez = None
@client.event
async def on_message(message):
  global currentDeez
  if message.author == client.user:
    return

  if message.content.startswith('$deezadd'):
    await message.channel.send('you said: ' + message.content[9:])
    wordsRead = open('allWords.txt', 'r')
    wordsAppend = open('allWords.txt', 'a')

    words = set()
    for word in wordsRead:
      words.add(word.strip())

    if message.content[9:].strip() not in words:
      wordsAppend.write(message.content[9:] + '\n')
      await message.channel.send(message.content[9:] + ' added to the deez list!')
    else:
      await message.channel.send('Duplicate! Try another word!')

    wordsRead.close()
    wordsAppend.close()
    return

  if message.content == '$deezskip' and message.channel.id == 1008543791294185555:
    currentDeez = None
    await run()
    return

  if message.content == '$deez':
    await message.channel.send('nuts!')
    return

  global currentSearchMessage
  global currentSendMessage
  global lugungumSearchMessage
  if currentSearchMessage is not None and message.reference is not None and message.reference.message_id == currentSearchMessage.id:
    lugungumSearchMessage = currentSearchMessage
    currentSearchMessage = None
    currentSendMessage = message.clean_content
  if lugungumSearchMessage is not None and message.reference is not None and message.reference.message_id == lugungumSearchMessage.id:
    currentSendMessage = message.clean_content

async def sendAskMessage(dClient, deez):
  channel = await dClient.fetch_channel(1008543791294185555)
  message = await channel.send(content=f"Today's deez is: {deez.strip()}. Reply to this message to specify a sentence. Otherwise the generic will be used.")
  global currentSearchMessage
  currentSearchMessage = message

def getRandomDeez(prevUsedWordsPath, allPossibleWordsPath):
  prevFile = open(prevUsedWordsPath, "r")
  allFile = open(allPossibleWordsPath, "r")

  prevWords = set()
  for word in prevFile:
    prevWords.add(word.strip())

  possWords = []
  for word in allFile:
    if word.strip() not in prevWords:
      possWords.append(word.strip())

  allFile.close()
  prevFile.close()

  randomDeez = possWords[random.randint(0, len(possWords)-1)]

  prevFile = open(prevUsedWordsPath, "a")
  prevFile.write(randomDeez + "\n")
  prevFile.close()

  return randomDeez

def postToInsta(deez):
  warnings.filterwarnings("ignore", category=DeprecationWarning) 
  W, H = (1080, 1080)
  msg = deez
  fnt = ImageFont.truetype('./arial.ttf', 80)
  deezImg = Image.new('RGB', (W, H), color=(255, 255, 255))
  draw = ImageDraw.Draw(deezImg)
  w, h = draw.textsize(msg, font=fnt)
  draw.text(((W - w) / 2, (H - h) / 2), msg, font=fnt, fill="black")
  deezImg.save('todayDeez.jpg')
  imgA = Image.open("todayDeez.jpg")
  imgB = Image.open("crumpled.jpeg").convert(imgA.mode)
  img = Image.blend(imgA, imgB, 0.2)
  img.save('todayDeez.jpg')

  today = datetime.date.today()
  cl = Client()
  cl.login(username="the.daily.deez", password="deeznuts124")
  cl.photo_upload("todayDeez.jpg", today.strftime("%m/%d/%Y"))

async def run():
  global currentDeez
  global currentSearchMessage
  global currentSendMessage
  if currentDeez is not None and currentSearchMessage is None:
    currentSendMessage = currentSendMessage.replace("\\n", "\n")
    postToInsta(currentSendMessage)
  elif currentDeez is not None:
    postToInsta(f"Do you know {currentDeez.strip()}?\n{currentDeez.strip()} deez nuts.")
  currentDeez = getRandomDeez("./prevWords.txt", "./allWords.txt")

  global client
  await sendAskMessage(client, currentDeez)

async def loopStart():
  # do a first run
  await run()

  # pick first futureRun date (today if it is before the specified time)
  now = datetime.datetime.now(timezone('US/Eastern'))
  if (now.replace(hour=16, minute=59, second=0) - now).total_seconds() >= 0:
    futureDelta = now + datetime.timedelta(days = 0)
    print("First run later today!")
  else:
    futureDelta = now + datetime.timedelta(days = 1)

  futureRun = futureDelta.replace(hour=17, minute=00, second=0)

  # do that shit
  while True:
    now = datetime.datetime.now(timezone('US/Eastern'))
    if (futureRun - now).total_seconds() <= 0:
      futureRun = futureRun + datetime.timedelta(days = 1)
      await run()

    # 5 second granularity between loop runs because im paranoid that lower will cause issues
    await asyncio.sleep(5)


if __name__ == "__main__":
  client.run('MTAwODU0Mjk4NjQ2MTc3Mzk0NQ.Gqqnr0.3M4SvEu6BffnNNZeWzjagxyth3J3oWKwQVxBbM')



