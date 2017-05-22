import json
from dateutil import parser as dateparser
from random import randint

class Tweet:
    ''' A container for a processed tweet

        Extracts information from the json input
    '''
    def __init__(self, json_tweet):
        self.clean_text = json_tweet['text']
        self.raw_text = json_tweet['unmodified_text']
        self.category = json_tweet['label']
        if 'is_quote_status' in json_tweet:
            self.is_quote = json_tweet['is_quote_status']
            self.reply_id = json_tweet['in_reply_to_status_id']
            self.reply_user = json_tweet['in_reply_to_user_id']
        self.conf = [float(num) for num in json_tweet['conf'].split()]
        if 'id' in json_tweet:
            self.idnum = json_tweet['id']
        else:
            self.idnum = randint(0, 10**50)
        if 'date' in json_tweet:
            self.date = dateparser.parse(json_tweet['date'])
        else:
            self.date = dateparser.parse(json_tweet['created_at'])
        self.pos = json_tweet['pos'].split()
        self.length = len(self.clean_text.split())

    def word_freq(self, search_word):
        return sum([1 for word in self.clean_text.split() if search_word == word])

class TweetCollection:
    ''' A list type container for tweets that stores auxiliary processed information for summarization

        words            --- a list of all words in the dictionary
        collection       --- a mapping of tweet ID to the tweet datastructure 
        word_frequencies --- a mapping from a word to the frequency of the word
        word_count       --- number of words in the collection
    '''

    def __init__(self, tweets=[]):
        ''' Creates a blank collection 
            If twweets is specified, a list of tweets in Tweet type those are added 
        '''
        self.collection = dict()
        self.words = []
        self.word_frequencies = dict()
        self.word_locations = dict()
        self.word_count = 0
        for tweet in tweets:
            self.add_tweet(tweet)

    def __iter__(self):
        return self.collection.__iter__()

    def add_tweet(self, tweet):
        ''' Add a tweet to the colelction '''

        #Build the frequency chart for word frequency
        for word in tweet.clean_text.split():
            self.word_count += 1
            if word in self.word_frequencies:
                self.word_frequencies[word] += 1
                self.word_locations[word] += [tweet.idnum]
            else:
                self.word_frequencies[word] = 1
                self.word_locations[word] = [tweet.idnum]
                self.words.append(word)
        self.collection[tweet.idnum] = tweet

        
    def word_probability(self, word):
        ''' Returns the probability of a word in the collection 
    
            Defined as count(word) / number of words in the collection
        '''
        if word in self.words:
            return self.word_frequencies[word] / self.word_count
        else:
            return 0

    def tweet_probability(self, tweet_id, word_probabilities = None):
        ''' Return the probability of some tweet based on the word probabilities 
       
            If no word_probabilities dict is provided, it uses the word_probability 
            method. 

            Tweet probability is the product of the probabilities of the words
        '''
        tweet = self.collection[tweet_id]
        probability = 1
        if word_probabilities: #if a dict of word probabilities is given
            for word in tweet.clean_text.split():
                probability *= word_probabilities[word]
        else: #no word probabilities given, so calculate on the fly
            for word in tweet.clean_text.split():
                probability *= self.word_probability(word)
        return probability / len(tweet.clean_text.split())

    def add_from_file(self, file_path):
        ''' Adds to collection all tweets in a jsonlist formatted file 

            Assumes that the file is formatted so that each line is a json entry
            Tweets must have all data fields specified in their constructor!
        '''
        with open(file_path) as file:
            lines = file.readlines()
        tweets = [Tweet(json.loads(line)) for line in lines]
        for tweet in tweets:
            self.add_tweet(tweet)        
        
    def as_list(self):
        return [tweet for tweetid, tweet in self.collection.items()] 
