from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands
import nltk
nltk.download('punkt')
import re
import heapq
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('stopwords')


class GoogleScrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", aliases=["asking"], help="Ask anything from Shobobot!")
    async def ask(self, ctx, *args):
        query = " ".join(args)
        query.replace(" ", "+")

        url = 'https://www.google.com/search?q=' + query

        result = requests.get(url)
        doc = BeautifulSoup(result.text, "lxml")

        id = doc.find_all(id="main")[0]
        article = id.find_all(["a"])

        for i in range(len(article)):
            article[i] = "".join(str(article[i]))
            if 'google.com' in article[i]:
                article[i] = ""
            if '/search' in article[i]:
                article[i] = ""
            if '/advanced_search' in article[i]:
                article[i] = ""
            if '.jpg' in article[i]:
                article[i] = ""
            if '.png' in article[i]:
                article[i] = ""

        urls = ""
        article = "".join(article)
        cont = False
        for i in range(len(article)):
            if article[i] == "h" and article[i + 1] == "t" and article[i + 2] == "t" and article[i + 3] == "p" and article[i + 4] == "s":
                cont = True
            if article[i] == '&' and article[i + 1] == "a" and article[i + 2] == "m" and article[i + 3] == "p":
                cont = False
                urls += ', '
            if cont == True:
                urls += article[i]

        # print(article)
        urls = urls.split(", ")
        while ("" in urls):
            urls.remove("")
        # print(urls)

        newResult = requests.get(urls[0])
        newDoc = BeautifulSoup(newResult.text, "html.parser")
        #print(newDoc)
        text = ""
        # text = newDoc.find_all("p").getText()
        for el in newDoc.find_all(['p', 'b', 'div', 'h1', 'h2', 'h3', 'h4', 'h5']):
            #print(el.get_text())
            text += el.get_text()

        print(text)
        print(urls)

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', text)
        article_text = re.sub(r'\s+', ' ', article_text)

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        sentence_scores = {}
        comment_words = ""
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                comment_words += ' '+word
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        print(summary)

        await ctx.send(summary)

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=stopwords,
                              min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.savefig('wordcloud.png')

# print(doc.prettify())
