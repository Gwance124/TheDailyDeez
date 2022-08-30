from pyphonetics import RefinedSoundex


#Returns a list of deez-type words ending in a specific suffix
def deezinator(dict, ending):
  result = []
  counter = 0
  for word in dict:
    counter += 1
    if counter % 100 == 0:
      print(f"Checking words with: '{ending}' ending. Checking word {counter} out of {len(dict)}", flush=True, end="\r")
    
    if word[-len(ending):] == ending:
      if word[0:-len(ending)] in dict:
        result.append(word)
  print("")
  return result

  
#Returns a list of deez-type words ending in a specific suffix
def deezSoundinator(dict, soundsLike):
  rs = RefinedSoundex()
  result = []
  counter = 0
  for word in dict:
    counter += 1
    if counter % 100 == 0:
      print(f"Checking words that sound like: {soundsLike}. Checking word {counter} out of {len(dict)}", flush=True, end="\r")

    try:
      if rs.distance(soundsLike, word) == 0:
        result.append(word)
    except:
      continue

  print("")
  return result

if __name__ == "__main__":
  ENDING_ARR = ["on", "ma", "ese", "dice", "in", "ee", "eves", "lips"]
  SIMILAR_WORD_SEARCH = ["putting", "eating", "sucking", "licking", "taking", "loving", "choking", "these"]
  
  fin = open("./engmixBIG.txt", encoding="utf8")
  wordArr = set()
  for line in fin:
    wordArr.add((line.strip().lower()))
  fin.close()

  allEndingArray = []
  for ending in ENDING_ARR:
    allEndingArray.append(deezinator(wordArr, ending))

  allSimilarWordArray = []
  for word in SIMILAR_WORD_SEARCH:
    allSimilarWordArray.append(deezSoundinator(wordArr, word))
  
  fout = open("deezWithSpaces.txt", "w")

  count = 0

  for arr in range(len(allEndingArray)):
    fout.write(f"\n{ENDING_ARR[arr]}: \n\n")
    for word in allEndingArray[arr]:
      fout.write(word + "\n")
      count += 1

  fout.write("\n--------Similar Word Section--------\n\n")
  
  for arr in range(len(allSimilarWordArray)):
    fout.write(f"\n{SIMILAR_WORD_SEARCH[arr]}: \n\n")
    for word in allSimilarWordArray[arr]:
      fout.write(word + "\n")
      count += 1
      
  fout.close()

  print(f"Congratulations! You have found {count} variations of deez nuts jokes. Have fun.")
