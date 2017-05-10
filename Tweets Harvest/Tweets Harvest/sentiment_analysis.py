'''
@author: Team12

Declaration: This classifier is an improved version based on the following sources

http://www.360doc.com/content/16/0725/19/15165994_578332920.shtml
https://github.com/abromberg/sentiment_analysis_python/blob/master/sentiment_analysis.py
http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/

'''
import re, math, itertools, string
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords

stops = stopwords.words('english')


# predict unlabeled data
def predict(classifier, sentence):
    words = re.findall(r"[\w']+|[.,!?;]", sentence.rstrip())
    words = finding_best_words(words, bestWords)
    return classifier.classify(words)


# train a classifier using the best features selected
def ta_classifier():
    global bestWords
    featureScore = scores()
    bestWords = best_words(featureScore)
    cl = basicClassifier(bestWords)
    return cl


def scores():
    posWords = []
    negWords = []
    with open('pos.txt', 'r') as posSentences:
        for i in posSentences:
            posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            posWord = list(set(posWord).difference(set(stops)))
            posWord = list(set(posWord).difference(set(string.punctuation)))
            posWords.append(posWord)
    with open('neg.txt', 'r') as negSentences:
        for i in negSentences:
            negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            negWord = list(set(negWord).difference(set(stops)))
            negWord = list(set(negWord).difference(set(string.punctuation)))
            negWords.append(negWord)
    posWords = list(itertools.chain(*posWords))
    negWords = list(itertools.chain(*negWords))

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()
    for word in posWords:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in negWords:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1

    # finds the number of positive and negative words, as well as the total number of words
    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    # builds dictionary of word scores based on chi-squared test
    featureScore = {}
    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        featureScore[word] = pos_score + neg_score

    return featureScore


def best_words(word_scores):
    bestWords = []
    best_vals = sorted(word_scores.items(), key=lambda w: w[1], reverse=True)[:10000]
    for i in best_vals:
        bestWords.append(i[0])
    return bestWords


def bag_of_words(words):
    return dict([(word, True) for word in words])


def finding_best_words(words, bestWords):
    return dict([(word, True) for word in words if word in bestWords])


def bigram_words(words, score_fn, n):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bigrams


def basicClassifier(bestWords):
    posFeatures = []
    negFeatures = []
    posBigrams = []
    negBigrams = []
    posBigramsList = []
    negBigramsList = []

    with open('pos.txt', 'r') as posText:
        for i in posText:
            posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())

            # remove stop words and punctuation
            posWord = list(set(posWord).difference(set(stops)))
            posWord = list(set(posWord).difference(set(string.punctuation)))

            posBigrams.append(posWord)
            posWord = [finding_best_words(posWord, bestWords), 'pos']
            posFeatures.append(posWord)

        # extract the most informative 1000 positive bigrams
        posBigrams = list(itertools.chain(*posBigrams))
        posBigrams = bigram_words(posBigrams, score_fn=BigramAssocMeasures.chi_sq, n=1000)

        # add the bigrams into the best words set
        for bigram in posBigrams:
            s = bigram[0] + " " + bigram[1]
            bestWords.append(s)
            posBigramsList.append([s])

        posBigramsList = list(itertools.chain(*posBigramsList))
        posFeatures.append([bag_of_words(posBigramsList), 'pos'])

    with open('neg.txt', 'r') as negText:
        for i in negText:
            negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())

            negWord = list(set(negWord).difference(set(stops)))
            negWord = list(set(negWord).difference(set(string.punctuation)))

            negBigrams.append(negWord)
            negWord = [finding_best_words(negWord, bestWords), 'neg']
            negFeatures.append(negWord)

        # extract the most informative 1000 positive bigrams
        negBigrams = list(itertools.chain(*negBigrams))
        negBigrams = bigram_words(negBigrams, score_fn=BigramAssocMeasures.chi_sq, n=1000)

        # add the bigrams into the best words set
        for bigram in negBigrams:
            s = bigram[0] + " " + bigram[1]
            bestWords.append(s)
            negBigramsList.append([s])

        negBigramsList = list(itertools.chain(*negBigramsList))
        negFeatures.append([bag_of_words(negBigramsList), 'neg'])

    posCutoff = int(math.floor(len(posFeatures) * 1 / 4))
    negCutoff = int(math.floor(len(negFeatures) * 1 / 4))
    testFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
    trainFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]

    # record the best features in case that someone need to check them out
    fp = open('best_words.txt', 'w')
    fp.write(str(bestWords))
    fp.close

    cl = NaiveBayesClassifier.train(trainFeatures)
    print(nltk.classify.util.accuracy(cl, testFeatures))

    return cl


def main():
    featureScore = scores()

    bestWords = best_words(featureScore)

    basicClassifier(bestWords)


if __name__ == '__main__':
    main()