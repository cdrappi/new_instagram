# main.py
import sys, time, httplib2, urllib2, random
import configs, helpers, dirs, credentials
import social_apis

def flush_followed_user(api, network, fid, influencer_user_ids):
    if fid in influencer_user_ids:
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
    influencer_user_ids      = set(helpers.list_of_keys(influencers, 'user_id'))
    # print(influencers)
    relationships_loaded, rel_header = helpers.load_csv(dirs.dirs_dict["relationships"][network])
    # """ next, check which users we've already searched """
    user_ids_searched = set(int(rel["follower_id"]) for rel in relationships_loaded)
    # """ we'll only search influencers who we haven't searched """
    influencers_to_search = [i for i in influencers if i["user_id"] and int(i["user_id"]) not in user_ids_searched]
    # print(influencers_to_search)

    # """ while there are influencers to search, we should search one of them """
    while len(influencers_to_search) > 0:
        infl = max(influencers_to_search, key=helpers.influencer_norm)
        print("chose: " + str(infl))
        
        try:
            follows = random.choice(api_list).get_follows(infl["user_id"])
            print("this person follows: " + str(follows))
            
            profile = social_apis.Profile(network, infl, follows_list=follows)
            relationships_loaded.extend(profile.get_follows())
            profile.flush_follows()
            
            for fid in follows:
                flushed_dict = flush_followed_user(random.choice(api_list), network, fid, influencer_user_ids)
                if not flushed_dict:
                    continue
                influencers.append(flushed_dict)
                influencer_user_ids.add(flushed_dict['user_id'])
                
                influencers_to_search.append(flushed_dict)
        except:
            print("An error occured - onto the next one")
        
        influencers_to_search.remove(infl)
        
        
    return None


def discover():
    """ after running seed, this will find new people
        that the seed users follow """
    api_dict = {
                "instagram": [social_apis.Instagram(i) for i in range(len(credentials.instagram_credentials))], 
                }
    for network in configs.all_social_networks:
        discover_network(network, api_dict[network])
    return None

def dedup(folder, network, on_keys):
    rows, header = helpers.load_csv(dirs.dirs_dict[folder][network])
    if not rows:
        return

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
    # """ to get information of the seed users.
    #     these are stored in configs.seed_users;
    #     right now it contains the initial
    #     list Brandon sent over a while ago.
    # """
    usernames = configs.seed_users
    insta_api = social_apis.Instagram(0)
    for username in usernames:
        user = insta_api.get_user(username)
        user_info = insta_api.get_user_data_dict(user)
        if user_info:
            profile = social_apis.Profile("instagram", user_info)
            profile.flush_info("discoveries")
    return None

def dedup_discoveries():
    """ if you want to remove duplicate items from the list of people """

    dedup("discoveries", "instagram", ["user_id",])
    return

def dedup_relationships():
    """ if you want to remove duplicate items from the list of relationships """

    dedup("relationships", "instagram", ["follower_id", "follows_id",])
    return

def sysargs_to_function(sa):
    fn = sa[0]
    args = sa[1:]
    fn_call = fn + "(" + ",".join(args) + ")"
    return fn_call

def run_main():
    if len(sys.argv) >= 2:
        to_exec = sysargs_to_function(sys.argv[1:])
        eval(to_exec)
    else:
        print("please enter a command to run")
    return None


if __name__ == "__main__":
    run_main()













