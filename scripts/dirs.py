# dirs.py
import getpass
import configs
import copy


base_directory = ".."

dirs_dict = dict()
for subdir in ["discoveries", "relationships"]:
    dirs_dict[subdir] = {site: "/".join([base_directory,subdir,site]) for site in configs.all_outlets}


dirs_dict["discoveries"]["seed"] = "../discoveries/seed_users"








