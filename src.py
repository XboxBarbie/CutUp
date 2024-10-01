"""
this is a program of the cut-up technique.Future plans: make main function WAY better,
find words with similar emotions of last line. Made by Tyla :)
"""

import random
import os
from textblob import TextBlob

class Cluster:
    def __init__(self, style):
        self.style = style

    def cluster(self, randomLine, lastLine, current_sentiment, new_sentiment, num, max_lines):
        if self.style == "repeat" or self.style == '1':
            return self.repeat_cluster(randomLine, lastLine, num)
        elif self.style == "crescendo" or self.style == '2':
            return self.crescendo_cluster(randomLine, lastLine, num, max_lines)
        elif self.style == "thematic" or self.style == '3':
            return self.thematic_cluster(randomLine, lastLine, current_sentiment, new_sentiment)

    def repeat_cluster(self, randomLine, lastLine, num):
        # Repeat the last line.
        if num % 2 == 0:  # Repeat every 2nd line
            return lastLine
        return randomLine

    def crescendo_cluster(self, randomLine, lastLine, num, max_lines):
       # Increase the chance of repetition as you near the end.
        repeat_chance = num / max_lines  # Higher chance to repeat near the end
        if random.random() < repeat_chance:
            return lastLine
        return randomLine

    def thematic_cluster(self, randomLine, lastLine, current_sentiment, new_sentiment):
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
    with open(path, 'r') as f:
        lines = f.readlines()
        non_empty_lines = [line.strip()
                           for line in lines
                           if line.strip()]

        # No non-empty line found
        if not non_empty_lines:
            return None

        # Find random line
        line = random.choice(non_empty_lines)
        phrase = line.split()

        # Limit words in output
        randomPoint = random.randint(1, min(len(phrase), max_words))
        return ' '.join(phrase[:randomPoint])

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def main():
    text_folder = 'Texts' # store texts here

    # ask user for line order
    style = input("Choose a style (1. repeat/ 2. crescendo/ 3. thematic): ").lower()
    cluster_style = Cluster(style)

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


    # Print first random line
    randomLine = getRandomLine(text_folder, max_words)
    sentiment = analyze_sentiment(randomLine)
    if not randomLine:
        print('No lines found.')
        return

    print(randomLine)

    num = 1
    while (num < max_lines):
        lastLine = randomLine
        randomLine = getRandomLine(text_folder, max_words)
        if randomLine: # Is randomLine valid?
            new_sentiment = analyze_sentiment(randomLine)
            # check cluster style
            outputLine = cluster_style.cluster(randomLine, lastLine, sentiment, new_sentiment, num, max_lines)
            print(outputLine)
            sentiment = new_sentiment
            num += 1

    # Ask user if they want to save
    save = str(input("\nWould you like to save the result? (y/n): "))
    while True:
        if save == 'y':
            s = open("CutUp.txt", "w")
            s.write(joinPhrases(phrases, max_words))
            s.close()
            print("File saved!")
            break
        elif save == 'n':
            print("Thank you for using CutUp!")
            break
        else:
            print("Please enter either 'y' or 'n'.")
    
    input("Press Enter to exit.")


if __name__ == "__main__":
    main()
