import sys
from zutils.dto.st.location import Location
from zutils.dto.st.timestamp import Timestamp
from zutils.dto.text.message import Message

class Tweet:

    def load_raw(self, line, sep='\x01'):
        items = self.split_line(line, sep)
        if len(items) != 28 or items[9] != 'en':
            raise IOError
        self.tid = long(items[0])
        self.uid = long(items[10])
        self.location = self.load_location(items[2], ',')
        self.timestamp = Timestamp(items[6])
        self.message = Message(items[1])


    def load_clean(self, line, sep='\x01'):
        items = self.split_line(line, sep)
        try:
            self.tid = long(items[0])
            self.uid = long(items[1])
            self.location = Location(float(items[2]), float(items[3]))
            self.timestamp = Timestamp(items[4])
            self.timestamp.timestamp = long(float(items[5]))
            self.message = Message(items[7])
            self.message.words = items[6].strip().split(' ')
        except:
            print 'Error when loading clean tweets'
            print line
            sys.exit(0)


    def split_line(self, line, sep):
        items = line.strip().split(sep)
        return items

    def load_location(self, line, sep):
        items = line.split(',')
        return Location(items[0], items[1])


    def to_string(self, sep='\x01'):
        data = [str(self.tid),
                str(self.uid),
                str(self.location.lat),
                str(self.location.lng),
                str(self.timestamp.time_string),
                str(self.timestamp.timestamp),
                str(' '.join(self.message.words)),
                str(self.message.raw_message.encode('utf-8'))]
                # str(self.message.raw_message.encode('ascii', 'ignore'))]
        return sep.join(data)


if __name__ == '__main__':
    print 'Begin testing Location'
    t = Tweet()
    print t
