

import unittest
import sys
#regex
import re
#http://www.tweepy.org/
import tweepy

#Get your Twitter API credentials and enter them in a txt file
#These are keys that twitter gives you when you register an App
#if it doesn't find keys.txt, add the full file path
keys = []
inFile = open("keys.txt", "r")
for line in inFile:
    line = line.strip()
    keys.append(line)

consumer_key = str(keys[0])
consumer_secret = str(keys[1])
access_key = str(keys[2])
access_secret = str(keys[3])

def userInput():
    user_input = ""
    while user_input == "":
            user_input = str(input("Write in your sentence? "))
            user_input=user_input.strip()
    input_list_words(user_input)
    user_input = re.sub('[\W_]+', ' ', user_input)
    #print (user_input)

word_dict = {}
def create_word_dict():
    words = open("dictionary.txt", "r")
    for line in words:
        line = line.strip()
        word_dict[line] = 1
    words.close()

def wordCheck(word):
    word = word.lower()
    if word in word_dict:
        return True
    else:
        return False

def userResult(wordList):
    #print(wordList)
    truecount = 0
    badwords = []
    if len(wordList)==1:
        if wordCheck(wordList[0]):
            truecount +=1
        else:
            badwords.append(wordList[0])
    else:
        for item in wordList:
            if wordCheck(item):
                truecount +=1
            else:
                badwords.append(item)
    result = ''
    #print (badwords)
    #badwords = str(badwords)
    badpercentage = ((len(wordList)-truecount)/(len(wordList)))
    badpercentage = str(round(badpercentage, 2))
    result='your incorrectly spelled words are: '+str(badwords)+" your percentage of incorrectly spelled words is "+badpercentage

    #print(badwords)
    frequent_misspelled(badwords)

    print(result)
    return (result)


def input_list_words(user_input):
    input_words = user_input.lower().split(" ")
   #print(input_words)
    #return (input_words)
    userResult(input_words)
    return (input_words)

def frequent_misspelled(badwords):
    badwords_dict = {}
    for word in badwords:
        if word not in badwords_dict:
            badwords_dict[word] = 1
        else:
            badwords_dict[word]+=1

    alotmisspelled = {}
    for item in badwords_dict.keys():
        if badwords_dict[item] >= 2:
            alotmisspelled[item] = badwords_dict[item]

    if len(alotmisspelled) !=0:
        print ("word misspelled :"+ " number of times misspelled" )
        for item in alotmisspelled.keys():
            print(item, ":", alotmisspelled[item])

    return(alotmisspelled)

def avg_length(badwords):
    counter = 0
    total = len(badwords)
    for word in badwords:
        a = len(word)
        counter += a

    avg = round(counter/total)
    return avg

def get_tweets():

    tweet_list = []
    username = ""
    while username == "":
            username = str(input("Enter a valid twitter handle (without @): "))

    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    # this block of code authenticates us with twitter's db
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    #set count to however many tweets you want; twitter only allows 200 at once
    number_of_tweets = 1

    #takes username and number of tweets and gets tweets
    tweets = api.user_timeline(screen_name = username,count = number_of_tweets)

    #create array of tweet information: username, tweet id, date/time, text
    #tweets_for_csv = [[username,tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]
    tweets_list = [[tweet.text.encode("utf-8")] for tweet in tweets]
    
    #declares that it is looking for tweets for var "username"
    print ("finding tweets for {0}".format(username))

    cleaned_tweets = ""
    print("Input: ")
    #scrubs tweets while displaying
    for tweet in tweets_list:
        #removes URLs and b's
        tweet = re.sub(r"http\S+","", str(tweet[0].decode("utf-8")))

        #removes @usernames
        tweet = ' '.join(word for word in str(tweet).split() if word[0] != '@')
        print(tweet)
        #removes nonalphanumeric
        tweet = re.sub('[\W_]+', ' ', tweet)
        #removes RT
        tweet = re.sub('RT ','', tweet)


        #removes some emojis
        emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
        tweet = emoji_pattern.sub(r'', tweet)

        #removes digits from tweets
        tweet = re.sub("\d+", "", tweet)

        cleaned_tweets += tweet
  

    input_list_words(cleaned_tweets)
def suggestWords1(word):
    suggestedwords = []
    word = str(word)
    for i in range(len(word)):
        if word[0:i]+word[i+1:] in word_dict.keys():
            #print("yay " + str(word[0:i]+word[i+1:]))
            suggestedwords.append(word[0:i]+word[i+1:])
        #else:
            #print("nay " + str(word[0:i]+word[i+1:]))
    return (suggestedwords)


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(wordCheck("Happy"), True)
    def test1(self):
        self.assertEqual(wordCheck("Meg"), False)
    def test2(self):
        self.assertEqual(userResult(["thot", "ught", "ugh"]), "your incorrectly spelled words are: ['thot', 'ught'] your percentage of incorrectly spelled words is 0.67")
    def test3(self):
        self.assertEqual(userResult(["jkfsdl"]), "your incorrectly spelled words are: ['jkfsdl'] your percentage of incorrectly spelled words is 1.0")
    def test4(self):
        self.assertEqual(userResult(['hello', 'can']), "your incorrectly spelled words are: [] your percentage of incorrectly spelled words is 0.0")
    def test5(self):
        self.assertEqual(input_list_words("I like corn"), ['i', 'like', 'corn'])
    def test6(self):
        self.assertEqual(input_list_words('sunflower'), ['sunflower'])
    def test7(self):
        self.assertEqual(frequent_misspelled(["uhhh", "uhhh", "uhhh", 'djklfdsjkl', 'hfdjkjfkd', 'ttt', 'ttt']), {'uhhh': 3, 'ttt': 2})
    def test8(self):
        self.assertEqual(frequent_misspelled(["dogg", "catt", "socer"]), {})
    def test9(self):
        self.assertEqual(frequent_misspelled([]),{})
    def test10(self):
        self.assertEqual(avg_length(["dogg", "catt", "socer"]), 4)
    def test11(self):
        self.assertEqual(avg_length(["t"]), 1)
    def test12(self):
        self.assertEqual(suggestWords1("this"), ['his', 'tis'])
    def test13(self):
        self.assertEqual(suggestWords1('thappy'), ['happy'])
    def test14(self):
        self.assertEqual(suggestWords1('ia'), ['a', 'i'])
    def test15(self):
        self.assertEqual(suggestWords1('sunflower'), [])
def main():

    create_word_dict()
    valid = False
    inputChoice = ""

    while valid == False:
        inputChoice = str(input("Check Twitter user? (t/f): "))
        if inputChoice == 't':
            get_tweets()
            valid = True
        elif inputChoice == 'f':
            userInput()
            valid = True

    #userInput()

    print()
    print()
    # print("Testing Unit Tests")

    mytest = MyTest()
    # mytest.test()
    # mytest.test1()
    # mytest.test2()
    # mytest.test3()
    # mytest.test4()
    # mytest.test5()
    # mytest.test6()
    # mytest.test7()
    # mytest.test8()
    # mytest.test9()
    # mytest.test10()
    # mytest.test11()
    mytest.test12()
    mytest.test13()
    mytest.test14()
    mytest.test15()
    


main()    