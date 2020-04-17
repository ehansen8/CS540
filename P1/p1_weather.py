# Evan Hansen
# CS 540
# P1
def euclidean_distance(data_point1, data_point2):
    x = extract_data_point(data_point1)
    y = extract_data_point(data_point2)

    d = ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2) ** 0.5
    return d


# Helps the euclidean_distance function by turning the dict values into
# a vector of floats
def extract_data_point(dp):
    x = [dp['PRCP'], dp['TMAX'], dp['TMIN']]
    return x


def read_dataset(filename):
    data_list = []
    KEY_LIST = ['DATE', 'PRCP', 'TMAX', 'TMIN', 'RAIN']
    with open(filename, 'r') as f:
        for line in f:
            d = {}
            val_list = line.rstrip().split(' ')
            for i in range(len(val_list)):
                v = val_list[i]
                # Saves from casting to float later
                if is_number(v):
                    v = float(v)

                d[KEY_LIST[i]] = v

            data_list.append(d)

    return data_list


# Checks if string is float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def majority_vote(nearest_neighbors):
    rain_count = 0
    for d in nearest_neighbors:
        if d['RAIN'] == 'TRUE':
            rain_count += 1

    if rain_count / len(nearest_neighbors) < 0.5:
        return 'FALSE'
    return 'TRUE'


def k_nearest_neighbors(filename, test_point, k):
    l = read_dataset(filename)

    # Sorts list from smallest euclidean distance to largest
    l.sort(key=lambda e: euclidean_distance(test_point, e))

    # Takes the first k closest neighbors
    nearest_neighbors = l[:k]
    vote = majority_vote(nearest_neighbors)
    return vote

