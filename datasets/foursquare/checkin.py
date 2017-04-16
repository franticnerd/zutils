from zutils.dto.st.location import Location
from zutils.dto.st.timestamp import Timestamp
from zutils.dto.text.message import Message
from zutils.datasets.twitter.tweet import Tweet

class Checkin(Tweet):

    def load_raw(self, line):
        raw_items = line.strip().split(',')
        items = [i.strip('"') for i in raw_items]
        if len(items) < 9:
            raise IOError
        self.tid = long(items[0])
        self.timestamp = Timestamp(items[1])
        self.location = Location(items[2], items[3])
        self.vid = items[-1] # foursquare venue id
        self.uid = long(items[-2])
        self.message = Message(','.join(items[4:-4]))


    def load_clean(self, line):
        items = line.strip().split('\x01')
        if len(items) != 9:
            raise IOError
        self.tid = long(items[0])
        self.uid = long(items[1])
        self.location = Location(float(items[2]), float(items[3]))
        self.timestamp = Timestamp(items[4])
        self.timestamp.timestamp = long(float(items[5]))
        self.message = Message(items[7])
        self.message.words = items[6].split()
        self.vid = items[8]



    def join_with_venue(self, venue_database):
        if self.vid not in venue_database.venues:
            self.category = None
            return
        venue = venue_database.venues[self.vid]
        self.location.lat = venue.location.lat
        self.location.lng = venue.location.lng
        self.category = venue.category

    def to_string(self, sep='\x01'):
        data = [str(self.tid),
                str(self.uid),
                str(self.location.lat),
                str(self.location.lng),
                str(self.timestamp.time_string),
                str(self.timestamp.timestamp),
                str(' '.join(self.message.words)),
                self.message.raw_message,
                str(self.vid)
                # self.category
                ]
        return sep.join(data)


if __name__ == '__main__':
    print 'Begin testing Location'
    with open('sample.txt', 'r') as fin:
        for line in fin:
            c = Checkin()
            c.load_raw(line)

