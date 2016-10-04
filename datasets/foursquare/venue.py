from zutils.dto.st.location import Location
import re

class Venue:

    def load_raw(self, line, sep=','):
        terms = [i.strip('"') for i in line.strip().split(',')]
        if len(terms) < 16:
            # print line
            raise IOError
        self.vid = terms[0]
        self.name = terms[2]
        location = self.parse_location(line)
        category = self.parse_category(line)
        if location is None or category is None:
            raise IOError
        self.location = location
        self.category = category


    def parse_location(self, line):
        lat_pattern = re.compile(r',4\d\.\d+,')
        lng_pattern = re.compile(r',-7\d\.\d+,')
        lat_obj = re.search(lat_pattern, line)
        lng_obj = re.search(lng_pattern, line)
        if lat_obj and lng_obj:
            lat, lng = lat_obj.group().strip(','), lng_obj.group().strip(',')
            return Location(float(lat), float(lng))
        else:
            return None

    def parse_category(self, line):
        cat_pattern = re.compile(r'"[^"]+::[^"]+"')
        cat_obj = re.search(cat_pattern, line)
        if not cat_obj:
            return None
        raw_category = cat_obj.group().strip('"')
        cat = self.clean_category(raw_category)
        return cat


    def clean_category(self, cat):
        items = cat.split('::')
        if 'Gym' in cat:
            return 'Great Outdoors'
        elif 'Home' in items[1] and 'Home' in items[0]:
            return 'Residence'
        elif items[0] == 'Homes, Work, Others' or\
                items[0] == 'Home, Work, Others' or\
                items[0] == 'Shelter ':
            return 'Professional & Other Places'
        elif items[0] == 'HOUSEOFCAKES ':
            return 'Food'
        elif items[0] == 'College & University':
            return 'Colleges & Universities'
        elif items[0] == 'Outdoors & Recreation':
            return 'Great Outdoors'
        elif items[0] == 'Shops & Services' or items[0] == 'Shops':
            return 'Shop & Service'
        elif items[0] == 'Travel Spots':
            return 'Travel & Transport'
        elif items[0] == 'Nightlife Spot':
            return 'Nightlife Spots'
        else:
            return items[0]


    def to_string(self, sep=','):
        data = [self.vid,
                str(self.location.lat),
                str(self.location.lng),
                self.category,
                self.name]
        return sep.join(data)


if __name__ == '__main__':
    input_dir = '/Users/chao/Dropbox/data/raw/4sq/'
    venue_file = input_dir + 'nyc_venues.csv'
    with open(venue_file, 'r') as fin:
        for line in fin:
            try:
                c = Venue()
                c.load_raw(line)
                print c.to_string()
            except:
                print 'zerror', line
                continue
