
class GridSpace:

    def __init__(self, ranges, bins):
        self.ranges = ranges
        self.num_bins = bins

    def get_grid_id(self, data):
        index_list = self.get_index_list(data)
        factor = 1
        res = 0
        for i, index in enumerate(index_list):
            res += index * factor
            factor *= self.num_bins[i]
        return res

    def get_index_list(self, data):
        res = []
        for i, value in enumerate(data):
            # the range for each axix
            begin, end = self.ranges[i]
            num_bin = self.num_bins[i]
            index = int(num_bin * (value - begin) / (end - begin))
            # when value == end, need to decrease the index
            if index >= num_bin:    index = num_bin - 1
            res.append(index)
        return res


if __name__ == '__main__':
    gs = GridSpace([(0,100), (0,100)], [10, 10])
    print gs.get_grid_id([90,1])
