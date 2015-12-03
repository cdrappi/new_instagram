# configs.py
import getpass

magic_follower_count = 50000

all_outlets = ('instagram',)
all_social_networks = ('instagram',)

profile_attributes = ["username", "user_id", "name", "num_posts", 
                      "num_follows", "num_followers", "link",
                      "description", "website"]

int_attrs = ["user_id", "num_posts", "num_follows", "num_followers"]

min_instagram_rate_limit_remaining = 100
instagram_seconds_sleep_after_rate_limit = 60

min_twitter_rate_limit_remaining = {"friends": 3, "user": 20, "limit": 20}
twitter_seconds_sleep_after_rate_limit = {"friends": 60, "user": 60, "limit": 60}
twitter_prob_reset_rate_limit = 0.3

seed_users = [
                "itsreallyken",
                "justinjedlica", 
                "judsonharmon",
                "chrisfawcettnyc",
                "fredrikeklundny", 
                "jordancarlyle30",
                "officialdaveywavey"
            ]



