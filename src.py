"""
Program Name: TBB
this is a program of the cut-up technique.Future plans: make main function WAY better,
find words with similar emotions of last line. Made by Tyla :)
"""

import random
import os
from textblob import TextBlob
import re


class Cluster:
    def __init__(self, style):
        self.style = style

    def cluster(self, randomLine, lastLine, current_sentiment, new_sentiment, num, max_lines):
        if self.style == "repeat" or self.style == '1':
            return self.repeatCluster(randomLine, lastLine)
        elif self.style == "thematic" or self.style == '2':
            return self.thematicCluster(randomLine, lastLine, current_sentiment, new_sentiment)
        elif self.style == "random" or self.style == '3':
            return self.neutralCluster(randomLine)

    def neutralCluster(self, randomLine):
        # Just prints random lines; that's it lol
        return randomLine

    def repeatCluster(self, randomLine, lastLine, num = random.randint(2,5)):
        # Repeat the last line.
        if num % random.randint(2, num) == 0:  # Repeat every nth line
            return lastLine
        return randomLine

    def thematicCluster(self, randomLine, lastLine, current_sentiment, new_sentiment):
        # Group lines with similar sentiment together.
        if current_sentiment * new_sentiment > 0:  # Similar sentiment
            return randomLine
        return lastLine


def getRandomLine(text_folder, max_words):
    paths = [os.path.join(text_folder, file)
             for file in os.listdir(text_folder)
             if os.path.isfile(os.path.join(text_folder, file))]

    # If no files
    if not paths:
        print('No text files found.')
        return None

    # random file
    path = random.choice(paths)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        nonEmptyLines = [line.strip()
                           for line in lines
                           if line.strip()]

        # No non-empty line found
        if not nonEmptyLines:
            return None

        # Find random line
        line = random.choice(nonEmptyLines)
        phrase = line.split()

        # Limit words in output
        randomPoint = random.randint(1, min(len(phrase), max_words))
        return ' '.join(phrase[:randomPoint])


def analyzeSentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def joinPhrases(phrases, max_words):
    sentence = ""
    sentences = []

    # Check punctuation
    sentenceEnd = re.compile(r'[.!?]')
    for phrase in phrases:
        sentence += ' ' + phrase.strip() # parse sentence

        if sentenceEnd.search(sentence):
            parts = re.split(r'([.!?])', sentence) # putting the end puntuations in parentheses keeps them

            for i in range(0, len(parts) - 1, 2):
                completeSentence = (parts[i] + parts[i + 1]).strip()
                sentences.append(completeSentence)

            # remaining is start of next sentence
            sentence = parts[-1].strip()
        if not sentenceEnd.search(sentence) and len(sentences) > (random.randint(max_words, 10) + 1):
            sentence += "."

    if sentence:
        sentences.append(sentence)

    return ' \n'.join(sentences)


def main():
    text_folder = 'Texts'  # store texts here
    phrases = []

    # Ask user for line order and enforce choices
    while True:
        try:
            style = input("Choose a style (1. repeat / 2. thematic / 3. random): ").lower()

            # Check for valid input and assign to cluster
            if style in ['1', 'repeat', '2', 'thematic', '3', 'random']:
                clusterStyle = Cluster(style)
                break  # Exit loop if valid input is given
            else:
                raise ValueError("Invalid choice. Please select a valid option.")
        except ValueError as e:
            print(e)

    # ask user for amount of lines printed
    while True:
        try:
            max_lines = int(input("Enter maximum number of lines: "))
        except ValueError:
            print("Please enter an integer.")
        else:
            break

    # ask user for amount of words
    while True:
        try:
            max_words = int(input("Enter maximum number of words: "))
        except ValueError:
            print("Please enter an integer.")
        else:
            break

    # Generate first random line
    randomLine = getRandomLine(text_folder, max_words)
    sentiment = analyzeSentiment(randomLine)
    if not randomLine:
        print('No lines found.')
        return

    num = 1
    while (num < max_lines):
        lastLine = randomLine
        randomLine = getRandomLine(text_folder, max_words)
        if randomLine:  # Is randomLine valid?
            new_sentiment = analyzeSentiment(randomLine)
            # check cluster style
            outputLine = clusterStyle.cluster(randomLine, lastLine, sentiment, new_sentiment, num, max_lines)
            phrases.append(outputLine)
            sentiment = new_sentiment
            num += 1

    print(joinPhrases(phrases, max_words))

    input("\nPress Enter to exit.")

if __name__ == "__main__":
    main()
