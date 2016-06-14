import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

rss_feeds = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
	     "iol": "http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in rss_feeds:
	publication = "bbc"
    else:
	publication = query.lower()
    feed = feedparser.parse(rss_feeds[publication])
    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000,debug=True)

