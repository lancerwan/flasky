import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

rss_feeds = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
	     "iol": "http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(rss_feeds[publication])
    first_article = feed['entries'][0]
    return render_template("home.html",
			   title=first_article.get("title"),
			   published=first_article.get("publish"),
			   summary=first_article.get("summary"))
if __name__ == "__main__":
    app.run(port=5000,debug=True)

