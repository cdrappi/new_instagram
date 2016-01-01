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

def write_csv(filename, data_list, header, write_type="w", sort=None, sort_rev=False):
    filename_csv = filename+".csv"
    with open(filename_csv, write_type) as f:
        writer = csv.writer(f)
        if write_type == "w" or ((not os.path.isfile(filename_csv)) or os.path.getsize(filename_csv) == 0):
            writer.writerow(header)
        if sort:
            data_list = sorted(data_list, key=lambda k: sort_by_list(k, sort), reverse=sort_rev)
        for row_dict in data_list:
            writer.writerow([row_dict[h] if h in row_dict else "" for h in header])
    return None

def sort_by_list(k, sort):
    return tuple(k[s] for s in sort)

def list_of_keys(d, key):
    return [el[key] for el in d]

def influencer_norm(infl):
    # this can be chosen in many different ways,
    # but the person with the number of followers
    # closest to some "magic follower count"
    # has worked well.

    # if the user is one of our seed users,
    # we choose them first.

    first_sort = (-1 * infl['degree'])

    if not infl["num_followers"]:
        return first_sort, -1*configs.magic_follower_count
    
    return first_sort, -1*abs(infl["num_followers"]-configs.magic_follower_count)

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










