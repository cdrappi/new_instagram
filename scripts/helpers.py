import csv, os, unidecode
import configs


def load_csv(filename):
    if not os.path.isfile(filename+".csv"):
        return list(), list()
    cols_to_data = list()
    with open(filename+".csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            temp_row = dict()
            for h,c in zip(header, row):
                if not c:
                    col_val = None
                elif h in configs.int_attrs:
                    try:
                        col_val = int(c)
                    except:
                        col_val = None
                else:
                    col_val = c
                temp_row[h] = col_val
            cols_to_data.append(temp_row)
    return cols_to_data, header

def write_csv(filename, data_list, header):
    with open(filename+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row_dict in data_list:
            writer.writerow([row_dict[h] for h in header])
    return None

def list_of_keys(d, key):
    return [el[key] for el in d]

def influencer_norm(infl):
    # this can be chosen in many different ways,
    # but the person with the number of followers
    # closest to some "magic follower count"
    # has worked well.

    # if the user is one of our seed users,
    # we choose them first.
    if infl["username"] in configs.seed_users:
        return 0

    if not infl["num_followers"]:
        return -1*configs.magic_follower_count
    
    return -1*abs(infl["num_followers"]-configs.magic_follower_count)

def old_format_unicode(a):
    ret = []
    for letter in a:
        try:
            ascii_a = str(letter)
        except:
            ascii_a = " "
        ret.append(ascii_a)
    return "".join(ret)

def format_unicode(a):
    try:
        if not isinstance(a, unicode):
            return a
        else:
            # unidecode converts any unicode string into ASCII
            # i believe it even converts Chinese to pinyin and shit.
            return unidecode.unidecode(a)
    except:
        return old_format_unicode(a)

def format_attr(a, attr):
    formatted_a = format_unicode(a)
    if attr in configs.int_attrs:
        try:
            return int(formatted_a)
        except:
            return None
    else:
        return formatted_a










