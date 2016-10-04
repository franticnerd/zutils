from venue import Venue

class VenueDatabase:

    def __init__(self):
        pass

    def load_raw_from_file(self, input_file):
        self.venues = {}
        with open(input_file, 'r') as fin:
            for line in fin:
                try:
                    venue = Venue()
                    venue.load_raw(line)
                    self.venues[venue.vid] = venue
                except:
                    # print line
                    continue

    def write_clean_venues_to_file(self, output_file):
        cnt = 0
        with open(output_file, 'w') as fout:
            for venue in self.venues.values():
                fout.write(venue.to_string() + '\n')
                cnt += 1
                if cnt % 10000 == 0:
                    print 'Finished writing %d clean venues.' % cnt
        print 'Finished dumping %d clean venues.' % cnt


if __name__ == '__main__':
    vd = VenueDatabase()
    vd.load_raw_from_file('nyc_venues.csv')
    vd.write_clean_venues_to_file('clean_venues.txt')
