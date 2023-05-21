import couchdb
from mastodon import Mastodon, StreamListener
import json
from mpi4py import MPI
import re
from textblob import TextBlob
from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, os, time, json


def streaming(urls, tokens, db):
    # get the rank and the size of the processor
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    # size = comm.Get_size()

    # indicate the db name
    # db_name = 'mastodon_' + str(urls[rank][17:])
    # db_name = 'mastodon_all'

    # # if not exist, create one
    # if db_name not in couch:
    #     db = couch.create(db_name)
    # else:
    #     db = couch[db_name]

    server_url = urls[rank]
    server_token = tokens[rank]
    # optional, better not hardcode here
    m = Mastodon(
        api_base_url=server_url,
        access_token=server_token

    )

    def sentiment_analysis(text):
        blob = TextBlob(text)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        if polarity > 0:
            sentiment_label = "Positive"
        elif polarity < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        return sentiment_label, polarity

    # listen on the timeline
    class Listener(StreamListener):

        # called when receiving new post or status update
        def on_update(self, status):
            # do sth
            json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
            doc_json = json.loads(json_str)
            # print(json_str)
            # doc_id, doc_rev = db.save(json.loads(json_str))
            wanted_json = {}
            employment_words = [
                'job', 'career', 'work', 'occupation', 'profession', 'employment', 'employee', 'employer', 'recruitment',
                'hiring', 'interview', 'resume', 'cv', 'application', 'salary', 'benefits', 'contract', 'promotion',
                'training',
                'skills', 'experience', 'office', 'workplace', 'colleague', 'team', 'performance', 'termination',
                'resignation', 'job security', 'work-life balance', 'human resources','finance','technology','education',
                 'software','bank','art','account', 'money', 'cash', 'wealth', 'rich', 'poor', 'stock','big', 'data', 
                'analytics', 'database', 'server', 'cloud', 'music', 'film', 'show', 'movie', 'artist', 'dancer']
#                 'finance', 'financial', 'bank', 'account', 'money', 'cash', 'wealth', 'rich', 'poor', 'stock',
#                 'market', 'investment', 'investor', 'invest', 'trading', 'trade', 'trader', 'stock', 'market',
#                 'stock', 'exchange', 'stock', 'broker', 'fund', 'gold', 'silver', 'asset', 'currency', 'banking',
#                 'banker', 'interest',
#                 'technology', 'tech', 'computer', 'software', 'hardware', 'data', 'internet', 'network', 'program',
#                 'code', 'developer', 'coding', 'programming', 'algorithm', 'app', 'application', 'website', 'web',
#                 'digital', 'device', 'smartphone', 'mobile', 'phone', 'laptop', 'tablet', 'ipad', 'iphone',
#                 'camera', 'robot', 'machine', 'artificial', 'intelligence', 'ai', 'virtual', 'reality', 'vr',
#                 'augment', 'ar', 'cloud', 'blockchain', 'cyber', 'security', 'hacker', 'hack', 'privacy',
#                 'encryption', 'data', 'science', 'big', 'data', 'analytics', 'database', 'server', 'cloud',
#                 'art', 'paint', 'sing', 'dance', 'music', 'film', 'show', 'movie', 'artist', 'dancer', 'cinema', 'design',
#                 'photo', 'picture', 'actor', 'story', 'theater', 'theatre', 'poem', 'poetry', 'poet', 'song', 'singer',
#                 'band', 'album', 'concert', 'performance', 'exhibition', 'gallery', 'museum', 'creative', 'creativity',
#                 'creative', 'art', 'creative', 'artist', 'creative', 'work', 'creative', 'industry',
#                 'school', 'college', 'university', 'study', 'student', 'teacher', 'tech', 'education', 'course',
#                 'learn', 'class', 'homework', 'assignment', 'exam', 'test', 'grade', 'degree', 'diploma', 'master',
#                 'bachelor', 'phd', 'scholarship', 'research', 'academy', 'academic', 'campus', 'tuition', 'tutor',
#                 'lecture', 'professor', 'classroom', 'lab', 'laboratory', 'library', 'book', 'textbook', 'notebook', 'note',
#                 'paper', 'essay', 'thesis', 'dissertation', 'project'
#             ]
            for ew in employment_words:
                # print(ew in doc_json["content"])
                if ew in doc_json["content"]:
                    wanted_json["content"] = doc_json["content"]
                    wanted_json["sentiment_label"],_ = sentiment_analysis(wanted_json["content"])
                    wanted_json["month"] = doc_json["created_at"][5:7]
                    # doc_id, doc_rev = db.save(wanted_json)
                    db.save(wanted_json)
                    # print(ew)
                    # print(f'{db_name} Document saved with ID: {doc_id} and revision: {doc_rev}')
                    break



            
            # # print(wanted_json)

            # print(f'{db_name} Document saved with ID: {doc_id} and revision: {doc_rev}')
    # make it better with try-catch and error-handling
    # try:
    m.stream_public(Listener())

if __name__ == "__main__":
    print('start')
    # authentication
    admin = 'user'
    password = 'pwd'
    ip = '172.26.134.204'
    url = f'http://{admin}:{password}@{ip}:5984/'

    # get couchdb instance
    couch = couchdb.Server(url)
    
    # indicate the db name
    db_name = 'mastodon_all_servers'
    # db_name = 'mastodon_test'
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    MASTODON_ACCESS_TOKENS="Iiuvste6iNApoHM0RX0J5J_w_y-J52KvZYXeFZ7Mztc, JTOka0FBt1Dv3Y5ptiWQ2tIKTX1O4Y58JmH_Ob65HeQ"
    SERVERS_URLS="https://mastodon.social, https://mastodon.au"
    mastodon_urls = SERVERS_URLS.split(', ')
    mastodon_tokens = MASTODON_ACCESS_TOKENS.split(', ')
    db = None
    if rank == 0:
        # if not exist, create one
        if db_name not in couch:
            db = couch.create(db_name)
        else:
            db = couch[db_name]
    if db is not None:
        streaming(urls=mastodon_urls, tokens=mastodon_tokens, db=db)
