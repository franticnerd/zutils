from random import randint
import os

# generate a combinations of the elements in list x, including empty sets
def combine(x):
    def dfs(x, sample, pos, res):
        if pos == len(x):
            res.append(sample)
            return
        element = [x[pos]]
        # two cases for each position
        dfs(x, sample, pos + 1, res)
        dfs(x, sample + element, pos + 1, res)
    res, sample = [], []
    dfs(x, sample, 0, res)
    return res

# randomly select k distinct elements from list x
def rand_select(x, k):
    if k > len(x):
        print 'Error! Maximum number exceeded when generating random elements.'
        return None
    y = list(x)
    last_pos = len(y) - 1
    for i in xrange(k):
        rand_pos = randint(0, last_pos)
        y[rand_pos], y[last_pos] = y[last_pos], y[rand_pos]
        last_pos -= 1
    return y[-k:]


# convert a list into a string
def format_list_to_string(l, sep='\t'):
    ret = []
    for e in l:
        if type(e) == float:
            ret.append(format_float_to_string(e))
        elif type(e) == list:
            ret.append(format_list_to_string(e, ' '))
        else:
            ret.append(str(e))
    return sep.join(ret)


def format_float_to_string(f):
    return str.format('{0:.4f}', f)


# ensure the path for the output file exist
def ensure_directory_exist(file_name):
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)


# print ensure_directory_exist('/Users/chao/Downloads/test34/2/hello.txt')
# print format_list_to_string([2.35, 2, [3, 4]])
