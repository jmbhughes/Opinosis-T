from OpinosisGraph import *
from tweet import *
import sys, os
if __name__ == "__main__":
    args = sys.argv[1:]
    input_file, = args

    # Load tweets
    tweets = TweetCollection()
    tweets.add_from_file(input_file)

    # Build Opinosis-T input
    sentences = []
    for tweetid in tweets:
        tweet = tweets.collection[tweetid]
        sentence = [WordUnit(term, pos) for term, pos in zip(tweet.clean_text.split(), tweet.pos)] 
        sentences.append(sentence)

    graph = OpinosisGraph(sentences)
