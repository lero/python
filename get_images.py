#!/usr/bin/env python2

import os
import httplib
import twitter
from urlparse import urlparse
from multiprocessing import Pool

def get_messages(twitter_id):
    api = twitter.Api()
    last_id = None if not os.path.isfile('%s-last_id' % twitter_id) else open('%s-last_id' % twitter_id).read()
    statuses = api.GetUserTimeline(screen_name=twitter_id, since_id=last_id, include_rts=True)
    tweets = [s.text for s in statuses]
    if len(tweets):
        ids = [s.id for s in statuses]
        open('%s-last_id' % twitter_id, 'w').write(str(ids[0]))
        urls = [ url for tweet in tweets for url in tweet.split() if 'http://' in url ]
        if len(urls):
            pool = Pool(processes=20)
            pool.map(get_real_url, urls)

def get_real_url(url):
    url1 = urlparse(url)
    conn1 = httplib.HTTPConnection(url1.hostname)
    conn1.request('GET', url1.path)
    pic_url = conn1.getresponse().getheader('location')
    conn1.close()
    get_pic(pic_url)

def get_pic(pic_url):
    url2 = urlparse(pic_url)
    conn2 = httplib.HTTPConnection(url2.hostname)
    conn2.request('GET', url2.path)
    response = conn2.getresponse()
    f_type = response.getheader('Content-Type')
    if f_type and f_type.startswith('image/'):
        if not os.path.exists('pic'): os.makedirs('pic')
        open('pic/' + url2.path.split('/')[-1], 'w').write(response.read())
        print 'getting %s' % pic_url
    conn2.close()

if __name__ == '__main__':
    for twitter_id in ['iLikeGirlsDaily']:
        get_messages(twitter_id)
