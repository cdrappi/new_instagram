import csv, os
import configs


def cast_or_none(info, cast):
    if not info:
        return None
    else:
        return cast(info)

def list_to_dict(l, key_by):
    ret = dict()
    for el in l:
        ret[el[key_by]] = el
    return ret

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

def initialize_source_dict(value):
    return {site: {outlet: value for outlet in configs.all_sites} for site in configs.all_sources}

def levenshtein(word1,word2):
    columns = len(word1)+1
    rows = len(word2)+1
    current_row = [0]
    for column in range(1,columns):
        current_row.append(current_row[column-1]+1)
    for row in range(1,rows):
        previous_row = current_row
        current_row = [previous_row[0]+1]
        for column in range(1,columns):
            insert_cost = current_row[column-1]+1
            delete_cost = previous_row[column]+1
            if word1[column-1] != word2[row-1]:
                replace_cost = previous_row[column-1]+1
            else:                
                replace_cost = previous_row[column-1]
            current_row.append(min(insert_cost,delete_cost,replace_cost))
    return current_row[-1]

def list_of_keys(d, key):
    return [el[key] for el in d]

def influencer_norm(infl):
    # this can be chosen in many different ways,
    # but closest to some "magic follower count"
    # has worked well.

    # if the user is one of our seed users,
    # we choose them first.
    if infl["username"] in ["cjbraz", "itsreallyken", "justinjedlica", 
                            "judsonharmon", "chrisfawcettnyc", "fredrikeklundny", 
                            "jordancarlyle30", "officialdaveywavey"]:
        return 0

    if not infl["num_followers"]:
        return -1*configs.magic_follower_count
    
    return -1*abs(infl["num_followers"]-configs.magic_follower_count)


def format_unicode(a):
    if not isinstance(a, unicode):
        return a
    ret = []
    for letter in a:
        try:
            ascii_a = str(letter)
        except:
            ascii_a = " "
        ret.append(ascii_a)
    return "".join(ret)

def format_attr(a, attr):
    formatted_a = format_unicode(a)
    if attr in configs.int_attrs:
        try:
            return int(formatted_a)
        except:
            return None
    else:
        return formatted_a










