from django.shortcuts import render, redirect

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, download
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from django.contrib.staticfiles import finders

# Download necessary NLTK resources if not already installed
download('punkt')
download('averaged_perceptron_tagger')
download('wordnet')
download('stopwords')

# Initialize reusable objects
translator = Translator()
analyzer = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def audiotosign_model(request):

	try:

		# Retrieve input from POST request
		text = request.POST.get('sen')
		if not text:
			return render(request, 'animation.html')

		print(f"Input: {text}")

		# Translate to English only if needed
		detected_lang = translator.detect(text).lang
		if detected_lang != 'en':
			text = translator.translate(text, dest='en').text
			print(f"Translated Text: {text}")

		# Sentiment Analysis using VADER
		sentiment = analyzer.polarity_scores(text)
		print(f"Sentiment Scores: {sentiment}")

		# Determine polarity label
		if sentiment['compound'] >= 0.05:
			sentiment_label = "positive"
		elif sentiment['compound'] <= -0.05:
			sentiment_label = "negative"
		else:
			sentiment_label = "neutral"

		print(f"Sentiment Label: {sentiment_label}")

		# Tokenization and POS tagging
		words = word_tokenize(text.lower())
		tagged = pos_tag(words)

		# Detect tense from POS tags
		tense = {
			"future": sum(1 for word, pos in tagged if pos == "MD"),
			"present": sum(1 for word, pos in tagged if pos in ["VBP", "VBZ", "VBG"]),
			"past": sum(1 for word, pos in tagged if pos in ["VBD", "VBN"]),
			"present_continuous": sum(1 for word, pos in tagged if pos == "VBG")
		}

		probable_tense = max(tense, key=tense.get)
		print(f"Detected Tense: {probable_tense}")

		# Filter and lemmatize words
		filtered_text = [
			lemmatizer.lemmatize(word, pos='v' if pos.startswith('V') else 'a')
			for word, pos in tagged if word not in stop_words
		]

		# Adjust words based on tense and sentiment
		if probable_tense == "past":
			filtered_text.insert(0, "Before")
		elif probable_tense == "future" and "will" not in filtered_text:
			filtered_text.insert(0, "Will")
		elif probable_tense == "present_continuous":
			filtered_text.insert(0, "Now")

		# Sentiment-based prefixes
		if sentiment_label == "positive":
			filtered_text.insert(0, "Great!")
		elif sentiment_label == "negative":
			filtered_text.insert(0, "Caution:")

		# Handle animations for words
		final_words = []
		for word in filtered_text:
			path = f"{word}.mp4"
			if finders.find(path):
				final_words.append(word)  # Use word's animation if available
			else:
				final_words.extend(list(word))  # Split into characters if not available

		print("Final Processed Words:", final_words)
		return render(request, 'animation.html', {'words': final_words, 'text': text})

	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return render(request, 'animation.html')