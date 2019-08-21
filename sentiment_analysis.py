import csv
import re
import time
import sys

from selenium import webdriver
from textblob import TextBlob
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 12})

class YouTubeClient(object):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def clean_comment(self, comment):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())

    def get_sentiment(self, comment):
        analysis = TextBlob(self.clean_comment(comment))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_comments(self, num_comments, watch_id):

        print("Getting the comments...")

        comments = []

        try:

            # Loading the url
            self.driver.get(f"https://youtube.com/watch?v={watch_id}")

            # Wait for page load
            time.sleep(2)

            # Scroll to load comments
            self.driver.execute_script("window.scrollTo(0,600)")
            time.sleep(3)

            # Calculating the number of scrolls required
            n_scrolls = num_comments * 2 // 45

            # Load all the comments by going to the bottom of the page for 10 iterations
            for _ in range(n_scrolls):
                self.driver.execute_script("window.scrollTo(0,1e10);")
                time.sleep(3)

            # Get all the comments
            elements = self.driver.find_elements_by_tag_name("ytd-comment-thread-renderer")

            # Save comments to a csv file
            for element in elements:

                parsed_comment = {}

                # Getting the information
                parsed_comment['author'] = element.find_element_by_id('author-text').text
                parsed_comment['text'] = element.find_element_by_id('content-text').text
                parsed_comment['sentiment'] = self.get_sentiment(parsed_comment['text'])

                # Append parsed_comment dictionary to comments list
                comments.append(parsed_comment)

            print("Done !")

            return comments

        except Exception as e:
            print(str(e))

        # Close the driver
        self.driver.close()


def main():
    yt = YouTubeClient()
    comments = yt.get_comments(num_comments=int(sys.argv[2]), watch_id=sys.argv[1])

    # Calculating percentages of positive and negative tweets
    positive_comments = [comment for comment in comments if comment['sentiment'] == 'positive']
    positive_percent = len(positive_comments)/len(comments)*100

    negative_comments = [comment for comment in comments if comment['sentiment'] == 'negative']
    negative_percent = len(negative_comments)/len(comments)*100

    neutral_percent = (len(comments) - len(positive_comments) - len(negative_comments))/len(comments)*100

    print("Positive comments percentage: {:.2f} %".format(positive_percent))
    print("Negative comments percentage: {:.2f} %".format(negative_percent))
    print("Neutral comments: {:.2f} %".format(neutral_percent))

    # Printing first 5 positive comments
    print("\n\nTOP POSITIVE COMMENTS:-")
    for comment in positive_comments[:5]:
        print(comment['text'])

    # Printing first 5 negative comments
    print("\n\nTOP NEGATIVE COMMENTS:-")
    for comment in negative_comments[:5]:
        print(comment['text'])

    # Pie Chart
    slices = [positive_percent, negative_percent, neutral_percent]
    labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    colors = ['#05E77F', '#e74c3c', '#E1D70E']
    plt.pie(slices, labels=labels, colors=colors, shadow=True, autopct="%1.1f%%", wedgeprops={'edgecolor': 'black'})
    plt.title('Sentiment Analyis of the Video')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
