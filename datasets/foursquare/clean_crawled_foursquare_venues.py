import json
import sys
from zutils.config.param_handler import yaml_loader
import codecs

# Step 1: load venues and clean them
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
    keys = ['id', 'name', 'location', 'categories']
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


# Step 2: load category and build mapping, map low-level categories to the first level
def build_category_map(category_file):
    with open(category_file, 'r') as fin:
        cat_obj = json.load(fin)
    cat_map = {}
    for c in cat_obj['categories']:
        name = c['name']
        map_sub_categories(cat_map, c, name)
    return cat_map


def map_sub_categories(cat_map, c, name):
    cat_id = c['id']
    cat_map[cat_id] = name
    for sub_cat in c['categories']:
        map_sub_categories(cat_map, sub_cat, name)

# clean the venues
def clean_venues(venues, cat_map):
    ret = []
    for v in venues.values():
        try:
            vid = v['id']
            lat = str(v['location']['lat'])
            lng = str(v['location']['lng'])
            one_cat_id = v['categories'][0]['id']
            cat = cat_map[one_cat_id]
            check_category_consistency(v, cat_map, cat)
            vname = v['name']
            ret.append((vid, lat, lng, cat, vname))
        except:
            print "Error:", sys.exc_info()[0]
            print json.dumps(v)
            continue
    return ret


def check_category_consistency(v, cat_map, cat):
    for subc in v['categories']:
        subid = subc['id']
        if cat_map[subid] != cat:
            print 'Inconsistent categories', v


def write_venues(venues, output_file):
    with codecs.open(output_file, 'w', 'utf-8') as fout:
        for v in venues:
            fout.write(','.join(v) + '\n')


if __name__ == '__main__':
    # data_dir = '/Users/chao/Dropbox/data/raw/sample_4sq_poi/'
    raw_venue_file = '/Users/chao/data/source/pois-dev/raw/venues.txt'
    category_file = '/Users/chao/data/source/pois-dev/raw/category.txt'
    clean_venue_file = '/Users/chao/data/source/pois-dev/clean/venues.txt'
    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        raw_venue_file = para['raw_venue_file']
        category_file = para['category_file']
        clean_venue_file = para['clean_venue_file']

    cat_map = build_category_map(category_file)
    # print cat_map

    venues = load_venues(raw_venue_file)
    venues = clean_venues(venues, cat_map)
    print 'Number of final venues: ', len(venues)
    write_venues(venues, clean_venue_file)
