# -*- coding: utf-8 -*-
import os, csv, urllib2, json, random, datetime, requests, time
import credentials, dirs, configs, helpers
import twitter#, facebook
from instagram.client import InstagramAPI


class Profile:
    def __init__(self, network, info_dict, follows_list=None):
        self.network = network
        self.init_info(info_dict)
        self.time_pulled = str(datetime.datetime.now())
        self.follows = follows_list
        return None

    def init_info(self, info_dict):
        for attr in configs.profile_attributes:
            if attr in info_dict:
                setattr(self, attr, info_dict[attr])
            else:
                setattr(self, attr, None)
        if not self.website:
            self.website = ""
        return None

    def flush_info(self, subdir="profiles"):
        filename = dirs.dirs_dict[subdir][self.network]+".csv"
        header = ["time_pulled"] + configs.profile_attributes
        with open(filename, "a+") as f:
            writer = csv.writer(f)
            if (not os.path.isfile(filename)) or os.path.getsize(filename) == 0:
                writer.writerow(header)
            profile_info = [self.time_pulled]
            profile_info += [helpers.format_attr(getattr(self, a), a) for a in configs.profile_attributes]
            writer.writerow(profile_info)
        return {k: v for k,v in zip(header, profile_info)}

    def flush_follows(self):
        header = ["follower_id", "follows_id", "time_written"]
        if not self.follows:
            return None
        filename = dirs.dirs_dict["relationships"][self.network]+".csv"
        with open(filename, "a+") as f:
            writer = csv.writer(f)
            if (not os.path.isfile(filename)) or os.path.getsize(filename) == 0:
                writer.writerow(header)
            all_follow_rows = self.get_follows()
            for follows_dict in all_follow_rows:
                writer.writerow([follows_dict[h] for h in header])
        return None

    def get_follows(self):
        if not self.follows:
            return list()
        ret = []
        for follows_id in self.follows:
            ret.append({"follower_id": self.user_id, "follows_id": follows_id, "time_written": self.time_pulled})
        return ret


class Instagram:
    def __init__(self, api_index):
        self.api = InstagramAPI(client_id=credentials.instagram_credentials[api_index]["client_id"],
                                client_secret=credentials.instagram_credentials[api_index]["client_secret"])
        self.access_token = credentials.instagram_credentials[api_index]["access_token"][0]
        return None

    def get_user(self, username):
        users = self.api.user_search(username)
        user_list = [u for u in users if u.username.lower() == username.lower()]
        if not user_list:
            print("Couldn't find Instagram information for " + username)
            return None
        else:
            return user_list[0]

    def check_rate_limit(self):
        while True:
            rl = self.api.x_ratelimit_remaining
            rl = int(rl) if rl else None
            if rl and rl < configs.min_instagram_rate_limit_remaining:
                print("RATE LIMIT: "+str(rl))
                time.sleep(configs.instagram_seconds_sleep_after_rate_limit)
                break
            else:
                print("rate limit: " + str(rl))
                break
        return True

    def get_user_by_id(self, user_id):
        self.check_rate_limit()
        try:
            return self.api.user(user_id)
        except:
            return None

    def get_user_data_dict(self, user):
        try:
            user_id = user.id
            response = urllib2.urlopen("https://api.instagram.com/v1/users/"+str(user_id)+"/?access_token="+self.access_token)
        except:
            return dict()
        data = json.load(response)
        info = {self.tkey(k): data["data"][k].encode("utf8") for k in ["username", "bio", "website", "full_name", "id"]}
        info["link"] = "https://instagram.com/"+info["username"]+"/"
        counts = {self.tkey(k): data["data"]["counts"][k] for k in ["media", "follows", "followed_by"]}
        info.update(counts)
        return info

    def get_follows(self, user_id):
        # rate limit issue happens here
        self.check_rate_limit()
        follows, next_ = self.api.user_follows(user_id)
        while next_:
            self.check_rate_limit()
            more_follows, next_ = self.api.user_follows(user_id, with_next_url=next_)
            follows.extend(more_follows)
        ret = [int(f.id) for f in follows if f.id]
        return ret

        
    @staticmethod
    def tkey(key):
        tk = {"full_name": "name", "media": "num_posts", 
                "follows": "num_follows", "followed_by": "num_followers",
                "bio": "description", "id": "user_id"}
        ret = tk[key] if key in tk else key
        ret = ret.encode("utf8")
        return ret


def strip_username(url, network_name):
    ret = url
    for to_replace in (configs.to_replace_general + configs.to_replace_specific[network_name]):
        ret = ret.replace(to_replace, "")
    for forbidden in configs.forbidden_url_chars:
        if forbidden not in ret:
            continue
        ret = ret[0:ret.index(forbidden)]
    return ret














