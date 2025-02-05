from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

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

        urls = ""
        article = "".join(article)
        cont = False
        for i in range(len(article)):
            if article[i] == "h" and article[i+1] == "t" and article[i+2] == "t" and article[i+3] == "p" and article[i+4] == "s":
                cont = True
            if article[i] == '"':
                cont = False
                urls += ', '
            if cont == True:
                urls += article[i]

        #print(article)
        urls = urls.split(", ")
        while ("" in urls):
            urls.remove("")
        #print(urls)

        newResult = requests.get(urls[0])
        newDoc = BeautifulSoup(newResult.text, "html.parser")
        print(newDoc)
        text = newDoc.find_all("p")
        print(text)
        print(urls[0])

        # id = doc.find_all(id="main")[0]
        span = doc.find_all("div")
        # em = doc.find(text="...")

        ans = ""
        ansList = str(span)
        ansList = ansList.split("><")
        count = 0

        for i in ansList:
            if "..." in i:
                ans += i
                count += 1
            if count == 10:
                break

        final = ""
        cont = False
        for i in range(len(ans)):
            if ans[i] == ">":
                cont = True
                continue
            if ans[i] == "<":
                cont = False
            if cont == True:
                final += ans[i]

        final = final.split('..')
        final = "".join(final)
        #final = final.split('. ')

        #print(final)

        await ctx.send(final)

#print(doc.prettify())