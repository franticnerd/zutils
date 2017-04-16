from random import randint

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

