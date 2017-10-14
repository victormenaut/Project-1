import unittest

def userInput():
    user_input = ""
    while user_input == "":
            user_input = str(input("Write in your sentence? "))
            user_input=user_input.strip()
    input_list_words(user_input)
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
    badwords = str(badwords)
    badpercentage = str((len(wordList)-truecount)/(len(wordList)))
    result+=''+'your incorrectly spelled words are: '+badwords+" your percentage of incorrectly spelled words is "+badpercentage
    print (result)

def input_list_words(user_input):
    input_words = user_input.lower().split(" ")
    #print(input_words)
    userResult(input_words)

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(wordCheck("Happy"), True)
    def test1(self):
        self.assertEqual(wordCheck("Meg"), False)
    def test2(self):
        self.assertEqual(userResult(["thot", "ught", "ugh"]), "result" )
    def test3(self):
        self.assertEqual(userResult(["jkfsdl"]), 'jfjf')


def main():
    create_word_dict()
    userInput()
    mytest = MyTest()
    mytest.test()
    mytest.test1()
    #mytest.test2()
    #mytest.test3()

main()