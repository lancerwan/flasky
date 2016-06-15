import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib
import urllib2

app = Flask(__name__)

rss_feeds = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml",
	     "iol": "http://www.iol.co.za/cmlink/1.640"}

defaults = {'publication':'bbc',
	    'city': 'London,UK',
            'currency_from':'GBP',
	    'currency_to':'USD'}


#exchangerate is not free,so I use baidu API
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=1bdf148c17cd4b939a2e8facf31033e8"

@app.route("/", methods=["GET","POST"])
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = defaults['publication']
    articles = get_news(publication)
    # get customize weather based on use input or default
    city = request.args.get('city')
    if not city:
	city = defaults['city']
    weather = get_weather(city)
    currency_from = request.args.get("currency_from")
    if not currency_from:
	currency_from = defaults["currency_from"]
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = defaults["currency_to"]
    rate,currencies = get_rate(currency_from,currency_to)
    return render_template("home.html",articles=articles,
    weather=weather,
    currency_from=currency_from,
    currency_to=currency_to,
    rate=rate,
    currencies=sorted(currencies))

def get_news(query):
    if not query or query.lower() not in rss_feeds:
	publication = defaults['publication']
    else:
	publication = query.lower()
    feed = feedparser.parse(rss_feeds[publication])
    weather = get_weather("LONDON,UK")
    return feed['entries']

def get_weather(query):
    api_url =" http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8044648e995ce47f5469a4a98021e197"
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
	weather = {"description":
		  parsed["weather"][0]["description"],
		 "temperature":parsed["main"]["temp"],
		 "city":parsed["name"],
		 "country":parsed['sys']['country']
		  }
    return weather

def get_rate(frm,to):

    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate,parsed.keys())

if __name__ == "__main__":
    app.run(port=5000,debug=True)

