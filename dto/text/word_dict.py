from collections import Counter


class WordDict:

    def __init__(self):
        self.word_counter = Counter()  # the counter of the words
        self.word_to_id = {}  # key: word, value: word_id
        self.words = None  # a list of words

    def size(self):
        return len(self.words)

    # construct all fields from scratch, input is a list of word list
    def generate(self, word_lists):
        for l in word_lists:
            self.update_count(l)
        self.encode_words()

    # update the support of different words, input is a set/list of words
    def update_count(self, words):
        self.word_counter.update(words)

    # return the words by support, and set the field self.words
    def rank_words(self):
        ranked = self.word_counter.most_common()
        self.words = [e[0] for e in ranked]

    # encode the words by support, starting word_id is 0
    def encode_words(self):
        if self.words is None:
            self.rank_words()
        for (i, w) in enumerate(self.words):
            self.word_to_id[w] = i

    # get the id of a word
    def get_word_id(self, word):
        return self.word_to_id[word]

    # get the word from id
    def get_word(self, id):
        return self.words[id]

    # get the count of a word
    def get_word_cnt(self, word):
        return self.word_counter[word]

    # given a threshold, return all the words that are infrequent
    def get_infrequent_words(self, threshold):
        ret = set()
        for w, c in self.word_counter.items():
            if c <= threshold:
                ret.add(w)
        return ret

    # given a threshold, return all the words that are frequent
    def get_frequent_words(self, threshold):
        ret = set()
        for w, c in self.word_counter.items():
            if c >= threshold:
                ret.add(w)
        return ret

    # write the word info into a file
    def write_to_file(self, output_file, sep = '\t', write_id=True, write_cnt=True):
        with open(output_file, 'w') as fout:
            for word in self.words:
                word_id = self.word_to_id[word]
                word_cnt = self.word_counter[word]
                elements = []
                if write_id: elements.append(str(word_id))
                elements.append(word)
                if write_cnt: elements.append(str(word_cnt))
                fout.write(sep.join(elements) + '\n')

    # load a word dict from the file
    def load_from_file(self, input_file, sep = '\t'):
        self.word_counter = Counter()
        self.word_to_id = {}
        self.words = []
        with open(input_file, 'r') as fin:
            for line in fin:
                items = line.strip().split(sep)
                word_id = int(items[0])
                word = str(items[1])
                self.word_to_id[word] = word_id
                self.words.append(word)
                if len(items) > 2:
                    word_cnt = int(items[2])
                    self.word_counter[word] = word_cnt





# # key: word, value: count
# class WordCounter:
#
#     def __init__(self):
#         self.d = Counter()
#
#     def build(self, words_lists):
#         self.update(words_lists)
#
#     # the input is a set of words
#     def update(self, words):
#         self.d.update(words)
#
#     # return a list of tuples, ordered by their supports in the corpora
#     def rank(self):
#         ret = []
#         for w, c in self.d.most_common():
#             ret.append((w, c))
#         return ret
#
#     def get_infrequent_words(self, threshold):
#         ret = set()
#         for w, c in self.d.items():
#             if c <= threshold:
#                 ret.add(w)
#         return ret
#
#     def get_frequent_words(self, threshold):
#         ret = set()
#         for w, c in self.d.items():
#             if c >= threshold:
#                 ret.add(w)
#         return ret

if __name__ == '__main__':
    wd = WordDict()
    wd.generate([['hello', 'world'], ['hello']])
    print wd.word_counter
    print wd.word_to_id
    print wd.words
    wd.write_to_file('/Users/chao/Downloads/test.txt')
