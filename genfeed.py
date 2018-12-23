from feedgen.feed import FeedGenerator
from pytz import timezone
from sqlalchemy import desc

from sni.models import *

TIMEZONE = timezone('US/Central')


def localize_time(time):
    return TIMEZONE.localize(time)


fg = FeedGenerator()
fg.load_extension('podcast')
fg.title('The Crypto-Mises Podcast')
fg.podcast.itunes_author('Satoshi Nakamoto Institute')
fg.link(href='http://nakamotoinstitute.org/', rel='alternate')
fg.subtitle('The official podcast of the Satoshi Nakamoto Institute')
fg.language('en')
fg.copyright('cc-by-sa')
fg.podcast.itunes_summary('Michael Goldstein and Daniel Krawisz of the Satoshi Nakamoto Institute discuss Bitcoin, economics, and cryptography.')
fg.podcast.itunes_owner('Michael Goldstein', 'michael@bitstein.org')
fg.link(href='http://nakamotoinstitute.org/podcast/feed/', rel='self')
fg.podcast.itunes_explicit('no')
fg.image('http://nakamotoinstitute.org/static/img/cryptomises/cmpodcast_144.jpg')
fg.podcast.itunes_image('http://nakamotoinstitute.org/static/img/cryptomises/cmpodcast_1440.jpg')
fg.podcast.itunes_category('Technology', 'Tech News')


eps = Episode.query.order_by(desc(Episode.date)).all()

for ep in eps:
    fe = fg.add_entry()
    fe.id('http://nakamotoinstitute/podcast/'+ep.slug+'/')
    fe.title(ep.title)
    fe.podcast.itunes_summary(ep.summary + ' If you enjoyed this episode, show your support by donating to SNI: ' + ep.address)
    fe.podcast.itunes_subtitle(ep.subtitle)
    fe.podcast.itunes_author('Satoshi Nakamoto Institute')
    fe.enclosure('https://s3.amazonaws.com/nakamotoinstitute/cryptomises/'+ep.slug+'.mp3', 0, 'audio/mpeg')
    fe.podcast.itunes_duration(ep.duration)
    fe.pubDate(localize_time(ep.time))

fg.rss_file('./sni/templates/podcast/feed.xml', pretty=True)
