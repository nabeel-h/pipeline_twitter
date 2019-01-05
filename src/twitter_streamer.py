import credentials
import json
import time
import sys
import os
from twython import TwythonStreamer


#Twitter Keys
consumer_key = credentials.twitter['consumer_key']
consumer_secret = credentials.twitter['consumer_secret']
access_token = credentials.twitter['access_token']
access_token_secret = credentials.twitter['access_token_secret']
#aws keys
aws_key_id = credentials.aws['key_id']
aws_key = credentials.aws['key']


class StdListener(TwythonStreamer):
    def __init__(self, local_fp):
        self.local_fp = local_fp

    def on_status(self, status):
        # print(status.text)
        pass

    def on_success(self, data):
        try:
            all_data = json.loads(data)
            tw_data = {}
            # status_sent_entity = {}
            # retweet_status_sent_entity = {}
            # print("Collecting Tweet")

            tw_data["status_created_at"] = str(all_data['created_at'])
            tw_data["status_id"] = str(all_data['id'])
            tw_data["status_text"] = str(all_data['text'])
            tw_data["user"] = str(all_data['user']['screen_name'])
            tw_data["user_id"] = str(all_data['user']['id'])
            tw_data["geo"] = str(all_data['geo'])
            tw_data["coordinates"] = str(all_data['coordinates'])
            tw_data["place"] = str(all_data['place'])
            tw_data = json.dumps(tw_data)
            try:
                print(tw_data)
                with open(str(self.local_fp), "r") as feedsjson:
                    feeds = json.load(feedsjson)
                feeds.append(tw_data)
                with open(str(self.local_fp), 'w') as jsonFile:
                    json.dump(feeds, jsonFile)
                print("#SAVED:"+str(self.local_fp))
            except Exception as e:
                print(e)
            # print(all_data.keys())
        except BaseException as e:
            print("failed on data {}".format(e))
            time.sleep(5)

    def on_error(self, status_code):
        if status_code == 420:
            return False

def main(input_searchName, fp):
    file_name = "\\src\\data\\"
    local_fp = fp + file_name + input_searchName[0]+"_twitter.json"


    with open(local_fp, 'w') as outfile:
        json.dump([], outfile)

    searched_list = input_searchName
    
    stream = StdListener(
						consumer_key, 
						consumer_secret,
                        access_token,
						access_token_secret,
                        searched_list,
                        local_fp
                        )
    
    while True:
        try: 
            stream.statuses.filter(track=searched_list)
        except:
            time.sleep(5)
            continue


if __name__ == '__main__':
    print(sys.argv[1:])
    script_dir = os.path.dirname(os.path.realpath('__file__'))
    fp = r'\Users\nabeel\PycharmProjects\twitterProj'
    abs_fp = os.path.join(script_dir, fp)
    print(abs_fp)
    main(['trump'], abs_fp)


'''
class twitterStreamer(luigi.Task):
    name = luigi.Parameter()
    def requires(self):
        return None
    def output(self):
        return luigi.LocalTarget('tweetStream.json')
    def run(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        print(self.output().path)
        streamListener = StdListener(self.name, self.output().path)
        #stream = tweepy.Stream(auth=api.auth, listener=streamListener)
        while True:
            stream = tweepy.Stream(auth=api.auth, listener=streamListener)
            stream.filter(self.name)
if __name__ == '__main__':
    # luigi.run()
    luigi.build([twitterStreamer(name='trump')], local_scheduler=True)
'''
