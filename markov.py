from collections import Counter, defaultdict
from random import randrange, choice, uniform
from math import exp

def sample(probabilities):
  totals = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
  n = uniform(0, totals[-1])
  for i, total in enumerate(totals):
      if n <= total:
          return i

# def c_vis(rounds):
#   p = []
#   for i in xrange(rounds):
#     p += [(0.85*exp(-i/10))+.15]
#   return p

# :: Int (round) -> Bool (C or not C)
def choose_c(round):
  p = (0.85*exp(-round/10))+.15
  if sample([p, 1 - p]) == 0:
    return True
  else:
    return False

# (corpus :: [Words]), maxN -> (nestedDict :: {bigrams, trigrams, ...})
def ngramsFromCorpus(corpus, maxN):
  # if nothing yet on the first level, makes new defaultdict (default value 0)
  nestedDict = defaultdict(lambda: defaultdict(int)) # int() === lambda: 0
  # for bigrams, trigrams, etc through maxN-grams
  for n in range(3, maxN + 1, 2):
    # for all words in corpus, count++ in nestedDict[wordsn-1] = {wordn: count} 
    for i in range(0,len(corpus)-n+1,2):
      indexNextWord = i + n - 1 #for n == 1, returns [] 
      searchWords = ' '.join(corpus[i : indexNextWord])
      nextWord = corpus[indexNextWord]
      nestedDict[searchWords][nextWord] += 1
  return nestedDict

# dictToPartialSums :: countDict -> wordcountTuples
def dictToPartialSums(d):
  lst = []
  partialSum = 0
  for k, v in d.iteritems():
    partialSum += v
    lst += [(k, partialSum)]
  return lst

# nestedDictToTuples :: nestedDict -> {String : wordcountTuples}  
## needs dictToPartialSums()
def nestedDictToTuples(d):
  d_tuples = {}
  for k, v in d.iteritems():
    d_tuples[k] = dictToPartialSums(v)
  return d_tuples


# sampleWords :: wordcountTuples -> word 
def sampleWords(wordcountTuples):
  rand = randrange(wordcountTuples[-1][1])
  for i in range(len(wordcountTuples)): 
    if rand < wordcountTuples[i][1]:
      chosenWord = wordcountTuples[i][0]
      break
  return chosenWord

# (n :: Int), (chain :: [Word]), ngrams -> Word
def sampleNgrams(n, chain, ngrams):
  rounds = len(chain)/2
  priorWords = ' '.join(chain[-n+1:]) # take last n-1 words to end of chain
  if priorWords in ngrams:
    return [sampleWords(ngrams[priorWords])]
  elif n > 0: 
      return sampleNgrams(n - 1, chain, ngrams)
  else:
      if choose_c(rounds):
        return ['C']
      else:
        return ['D']

def makeNgrams(my_moves, their_moves, corpus):
  ngrams = {}
  rounds = len(their_moves)
  ngrams = nestedDictToTuples(ngramsFromCorpus(corpus, 5))
  return ngrams

def markov(my_moves, their_moves):
  rounds = len(their_moves)
  corpus = [x for t in zip(their_moves, my_moves) for x in t]
  ngrams = makeNgrams(my_moves, their_moves, corpus)
  #print ngrams
  n = sample([0.3,0.7])+2 
  #print n
  nextMove = sampleNgrams(n, corpus, ngrams)
  return nextMove[0]

def get_move(my_moves, their_moves):
  rounds = len(their_moves)
  if choose_c(rounds):
    return 'C'
  else: 
    return markov(my_moves, their_moves)
