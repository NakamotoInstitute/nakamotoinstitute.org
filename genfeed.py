from feedgen.feed import FeedGenerator

def print_enc(s):
  '''Print function compatible with both python2 and python3 accepting strings
  and byte arrays.
  '''
  print(s.decode('utf-8') if type(s) == type(b'') else s)

fg = FeedGenerator()
fg.load_extension('podcast')
fg.title('The Crypto-Mises Podcast')
fg.author({'name': 'Satoshi Nakamoto Institute'})
fg.link( href='http://nakamotoinstitute.org/', rel='alternate' )
fg.subtitle('The official podcast of the Satoshi Nakamoto Institute')
fg.language('en')
fg.podcast.itunes_summary('Michael Goldstein and Daniel Krawisz of the Satoshi Namaoto Institute discuss Bitcoin, economics, and cryptography.')
fg.link( href='http://nakamotoinstitute.org/podcast/feed/', rel='self' )
print_enc (fg.rss_str(pretty=True))

with open("./sni/templates/podcast/feed.xml", "w") as f:
    f.write(fg.rss_str(pretty=True))
