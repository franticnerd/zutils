import json

def load_venues(input_file):
    final_venues = {}
    with open(input_file, 'r') as fin:
        for line in fin:
            region_str, venue_str = line.strip().split('\x01')
            venues = json.loads(venue_str)
            venues = trim_venues(venues)
            extend_venues(final_venues, venues)
    return final_venues

# trim the venues by removing unnecessary fields
def trim_venues(venues):
    ret = []
    keys = ['id', 'name', 'location', 'categories', 'stats', 'description', 'tags']
    for venue in venues:
        trimmed_venue = {}
        for k in keys:
            if k in venue:
                trimmed_venue[k] = venue[k]
        ret.append(trimmed_venue)
    return ret


def extend_venues(final_venues, venues):
    for v in venues:
        vid = v['id']
        if vid not in final_venues:
            final_venues[vid] = v


def write_venues(venues, output_file):
    with open(output_file, 'w') as fout:
        for v in venues.values():
            fout.write(json.dumps(v) + '\n')


input_file = '/Users/chao/Downloads/ny_4sq_venues/venues.txt'
output_file = '/Users/chao/Downloads/ny_4sq_venues/clean_venues.txt'
venues = load_venues(input_file)
print len(venues)
write_venues(venues, output_file)
