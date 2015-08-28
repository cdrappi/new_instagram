# main.py
import time, httplib2, urllib2, random
import configs, helpers, dirs, credentials
import social_apis

def flush_followed_user(api, network, fid, influencers):
    if fid in helpers.list_of_keys(influencers, "user_id"):
        print("-"*100)
        print("we already have the user id: "+str(fid))
        print("-"*100)
        return None
    # print(fid)
    new_user = api.get_user_by_id(fid)
    if not new_user:
        print("we couldn't get the user")
        return None
    new_user_info = api.get_user_data_dict(new_user)
    new_ambassador_id = None
    new_profile = social_apis.Profile(network, new_user_info, new_ambassador_id)
    flushed_dict = new_profile.flush_info("discoveries")
    print("flushed "+str(flushed_dict))
    return flushed_dict


def discover_network(network, api_list):
    # """ first, load all of the previous influencers and relationships """
    influencers, infl_header = helpers.load_csv(dirs.dirs_dict["discoveries"][network])
    # print(influencers)
    relationships_loaded, rel_header = helpers.load_csv(dirs.dirs_dict["relationships"][network])
    # """ next, check which users we've already searched """
    user_ids_searched = set(int(rel["follower_id"]) for rel in relationships_loaded)
    # """ we'll only search influencers who we haven't searched """
    influencers_to_search = [i for i in influencers if i["user_id"] and int(i["user_id"]) not in user_ids_searched]
    # print(influencers_to_search)
    # """ while there are influencers to search, we should search one of them """
    while len(influencers_to_search) > 0:
        try:
            infl = max(influencers_to_search, key=helpers.influencer_norm)
            print("chose: " + str(infl))
            follows = random.choice(api_list).get_follows(infl["user_id"])
            print("this person follows: " + str(follows))
            profile = social_apis.Profile(network, infl, follows_list=follows)
            relationships_loaded.extend(profile.get_follows())
            profile.flush_follows()
            influencers_to_search.remove(infl)
            for fid in follows:
                # try:
                flushed_dict = flush_followed_user(random.choice(api_list), network, fid, influencers)
                if not flushed_dict:
                    continue
                influencers.append(flushed_dict)
                influencers_to_search.append(flushed_dict)
                # except:# httplib2.ServerNotFoundError:
                    # print("they prob have weird characters")
        except (urllib2.URLError, httplib2.ServerNotFoundError) as e:
            print("some internet error")
    return None


def discover():
    api_dict = {
                "instagram": [social_apis.Instagram(i) for i in range(len(credentials.instagram_credentials))], 
                }
    for network in configs.all_social_networks:
        discover_network(network, api_dict[network])
    return None

def dedup(folder, network, on_keys):
    rows, header = helpers.load_csv(dirs.dirs_dict[folder][network])
    stored_keys = set()
    new_rows = list()
    for row in rows:
        row_key = tuple(row[on_key] for on_key in on_keys)
        if row_key not in stored_keys:
            new_rows.append(row)
            stored_keys.add(row_key)
    helpers.write_csv(dirs.dirs_dict[folder][network], new_rows, header)
    return None

def seed():
    username_dict, header = helpers.load_csv(dirs.dirs_dict["discoveries"]["seed"])
    usernames = helpers.list_of_keys(username_dict, "username")
    insta_api = social_apis.Instagram(0)
    for username in usernames:
        user = insta_api.get_user(username)
        user_info = insta_api.get_user_data_dict(user)
        if user_info:
            follows_list = insta_api.get_follows(user_info["user_id"])
            profile = social_apis.Profile("instagram", user_info)
            profile.flush_info("discoveries")
    return None


if __name__ == "__main__":
    discover()
    # dedup("relationships", "instagram", ["follower_id", "follows_id"])
    # seed()













