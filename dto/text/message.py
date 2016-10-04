from text_parser import TextParser

class Message:

    def __init__(self, s):
        self.raw_message = s

    def clean_words(self, word_parser):
        self.words = word_parser.parse_words(self.raw_message)

    # clean words for one message (NOT efficient)
    def clean_words_pos(self, word_parser, preserve_tags, ark_run_cmd):
        self.words = word_parser.parse_words_by_ark_nlp(self.raw_message, \
                                                preserve_types, ark_run_cmd)

    def set_clean_words(self, clean_words):
        self.words = list(set(clean_words))

    def remove_stopwords(self, stopword_set):
        trimed_words = []
        for w in self.words:
            if w not in stopword_set:
                trimed_words.append(w)
        self.words = trimed_words


if __name__ == '__main__':
    wp = TextParser(min_length = 2)
    m = Message('hello, This is@ went octopi just a test for 12you!. Try it http://')
    preserve_types = ['V', 'N', '^']
    ark_run_cmd='java -XX:ParallelGCThreads=2 -Xmx2G -jar /Users/chao/Dropbox/code/lib/ark-tweet-nlp-0.3.2.jar'
    m.clean_words(wp)
    print m.words
    m.clean_words_pos(wp, set(['S', 'N', '^']), ark_run_cmd)
    print m.words
