import feedparser
from flask import Flask

app = Flask(__name__)

rss_feeds = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
	     "iol": "http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/bbc")
def bbc():
    return get_news('bbc')

@app.route("/cnn")
def cnn():
    return get_news('cnn')

@app.route("/iol")
def iol():
    return get_news("iol")

#get_news() must take arguements
def get_news(publication):
    feed = feedparser.parse(rss_feeds[publication])
    first_article = feed['entries'][0]
    return """
      <body>
	  <h1> BBC Headlines </h1>
	  <b>{0}</b> <br/>
	  <i>{1}</i> <br>
	  <p>{2}</p> <br/>
      </body>
</html>""".format(first_article.get("title"),first_article.
get("published"),first_article.get("summary"))

if __name__ == "__main__":
    app.run(port=5000,debug=True)

