from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create the analyzer object
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze the sentiment of a news headline or description.
    Returns sentiment label and compound score.
    """

    if not text:
        return "Neutral", 0.0

    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, compound