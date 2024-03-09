from textblob import TextBlob

def get_sentiment_score(description):
    blob = TextBlob(description)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# Example usage:
description = input("Enter the short description: ")
sentiment_score = get_sentiment_score(description)
print("Sentiment Score:", sentiment_score)
