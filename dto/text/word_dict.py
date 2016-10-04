from collections import Counter

class WordDict:

    def __init__(self):
        self.d = Counter()

    def build(self, words_lists):
        self.update(words_lists)

    # the input is a set of words
    def update(self, words):
        self.d.update(words)

    def rank(self):
        ret = []
        for w, c in self.d.most_common():
            ret.append((w, c))
        return ret

    def get_infrequent_words(self, threshold):
        ret = set()
        for w, c in self.d.items():
            if c <= threshold:
                ret.add(w)
        return ret

    def get_frequent_words(self, threshold):
        ret = set()
        for w, c in self.d.items():
            if c >= threshold:
                ret.add(w)
        return ret

if __name__ == '__main__':
    wd = WordDict()
    wd.build(['hello', 'this'])
    wd.update(set(['hello']))
    print wd.d

