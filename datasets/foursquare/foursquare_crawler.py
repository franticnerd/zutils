from foursquare import Foursquare, RateLimitExceeded
from collections import deque
from time import sleep
import random
from random import randint
import json
import sys
from zutils.config.param_handler import yaml_loader


def create_clients():
    clients = []
    clients.append(Foursquare(client_id='TXJGNUZMJ1KRZW1DMQCH43LS4G2GYRIJDRWWWZ44XYMHW0SY', client_secret='HAR0VUXOUMTKAGYMEK20SINMZKD2HECG1ZGVTHICHMTUBNKB'))
    clients.append(Foursquare(client_id='Z51MG4J5IW2OIB4QJYFDENW5OGK2IK3JJ3CCXDA5V1GG1URI', client_secret='0KKY3EUPQDK3JPXMC0ICETGP1EZJOXW4UNM5NNCL0YVZ1I0A'))
    clients.append(Foursquare(client_id='MYOBFJCXXTCYJZSHSTAXDZRQ3HSI3CCMKSVWNU5B5UPBLP04', client_secret='GYOPNHNIJBJT0POOYFMBPGEXMWM1VT2TBVBJ4IWEBGCINCYV'))
    clients.append(Foursquare(client_id='DKF1U0IIIGKHKUM3P3Q1CUOB1P5IGO1PBECGCP501V22LGUT', client_secret='PWQBZLVURTBWZJBGQNKULHAPDVYWLSLD45UBMI1SD2XIN3II'))
    clients.append(Foursquare(client_id='Z3ONQA0HX4EOBHTWNMKYPAF3SITXVHOA45LQJIBP2SCHY1JD', client_secret='KBV3MSMGAJ0CQJVGDDM20ZCKOXQYFRLTVQTPLDVM3N0CHPNU'))
    clients.append(Foursquare(client_id='WJTFTKDUFL3TBC1RN4LZ3KMTX4QCUA04U0GXMZGP5IQEWLRM', client_secret='15DFPEVFMYL1Q5LOCQ5D3AKLFGAO3L3SXSYONQBGLQQR5JDR'))
    clients.append(Foursquare(client_id='11TIOC2VSEIR0J0PZA2UIV1V053OQNNUJ1FRWMBJAVQC1M2A', client_secret='FU1BMT1L0Z3R34OLDBM1PMBK5HXFKXBPTR4KGHHACMAWOJFJ'))
    clients.append(Foursquare(client_id='0SCCF3VM21YCYIVH2PWIM5AQRTSWZ1241THVVXLRXDIXGKKF', client_secret='1LWLCHKYGP4FG3P2BAQQSDDSWWAZZS1Q5MYQO15ZS1NDD30F'))
    clients.append(Foursquare(client_id='PXQHCO0MQJ45BNXJ1SZTCCF1CJT5ZWSB4CCT4S0J50F0X2LK', client_secret='3MNNLG4YJ1Z4JQRNNYZLH5WHEHO24DKV2CIIKAQAEY3V4DU1'))
    clients.append(Foursquare(client_id='3GROBV5QXWMX3O30BITHE5VIW2VHE4KEUCROGBVXHXPQILW1', client_secret='HZMRZTCYCCS1E1OVTUMKYFEDEHWDZGLZJSQIJSYNCV1LMVPE'))
    return clients

random.seed(100)
clients = create_clients()

def sample_client():
    rand_index = randint(0, len(clients)-1)
    print 'Client ID: ', rand_index
    return clients[rand_index]


def query_categories(out_file):
    cat = clients[0].venues.categories()
    with open(out_file, 'w') as fout:
        fout.write(json.dumps(cat))

# query_categories('/Users/chao/Downloads/category.txt')


# retrieve all the POIs in a region, num_bin_init is the number of bins along each axis (x and y)
def retrieve_all_venues(min_x, min_y, max_x, max_y, num_bin_init, output_file, task_file):
    tasks = init_tasks(min_x, min_y, max_x, max_y, num_bin_init)
    with open(output_file, 'a') as fout:
        while len(tasks) > 0:
            region = tasks.popleft()
            print 'Processing region: ', region
            try:
                venues = query_venues_in_one_region(region)
            except:
                write_remaining_tasks(tasks, task_file)
                fout.flush()
                fout.close()
            # 50 is the limit of the foursquare crawling service for each request
            if len(venues) >= 50:
                # partition the region into 2*2 subregions
                sub_regions = partition_region(region, 2)
                tasks.extend(sub_regions)
            else:
                fout.write(str(region) + '\x01' + json.dumps(venues) + '\n')
            print '\t\t------------------- # POIs in this region: ', len(venues)
            print '\t\tNumber of regions to be processed:', len(tasks)


# partition the region and initialize the tasks, each task is a rectangle region.
def init_tasks(min_x, min_y, max_x, max_y, num_bin_init):
    tasks = deque()
    regions = partition_region((min_x, min_y, max_x, max_y), num_bin_init)
    tasks.extend(regions)
    # print 'Initial regions: ', regions
    print 'Initial number of tasks to be processed:', len(tasks)
    return tasks


# partiton the region into grids, num_bin_axis specifies the number of bins per axis
def partition_region(region, num_bin_axis):
    min_x, min_y, max_x, max_y = region
    regions = []
    delta_x = (max_x - min_x) / num_bin_axis
    delta_y = (max_y - min_y) / num_bin_axis
    # print delta_x, delta_y
    for i in xrange(num_bin_axis):
        min_xx = min_x + delta_x * i
        max_xx = min_xx + delta_x
        # print min_xx, max_xx
        for j in xrange(num_bin_axis):
            min_yy = min_y + delta_y * j
            max_yy = min_yy + delta_y
            region = (min_xx, min_yy, max_xx, max_yy)
            regions.append(region)
    return regions


def query_venues_in_one_region(region):
    min_lat, min_lng, max_lat, max_lng = region
    sw = ','.join((str(min_lat), str(min_lng)))
    ne = ','.join((str(max_lat), str(max_lng)))
    query = {'limit': 100, 'intent':'browse', 'sw':sw, 'ne':ne}
    while True:
        client = sample_client()
        try:
            result = client.venues.search(params = query)
            break
        except RateLimitExceeded:
            print 'Rate limit exceeded!'
            sleep(10)
    return result['venues']




def write_remaining_tasks(tasks, task_file):
    with open(task_file, 'w') as fout:
        for task in tasks:
            fout.write(str(task) + '\n')


if __name__ == '__main__':
    min_lat, min_lng, max_lat, max_lng = 33.7, -118.67, 34.33, -118.15
    num_bin_axis = 30
    data_dir = '/Users/chao/Downloads/la_4sq_venues/'
    if len(sys.argv) > 1:
        para_file = sys.argv[1]
        para = yaml_loader().load(para_file)
        data_dir = para['dir']
        min_lat = para['min_lat']
        min_lng = para['min_lng']
        max_lat = para['max_lat']
        max_lng = para['max_lng']
        num_bin_axis = para['num_bin_axis']
    poi_file = data_dir + 'raw_venues.txt'
    task_file = data_dir + 'remaining_tasks.txt'
    retrieve_all_venues(min_lat, min_lng, max_lat, max_lng, num_bin_axis, poi_file, task_file)


# retrieve_all_venues(40.5, -74.3, 40.95, -73.7, 20, '/Users/chao/Downloads/ny_poi.txt', '/Users/chao/Downloads/ny_tasks.txt')
# retrieve_all_venues(33.7, -118.67, 34.33, -118.15, 30, '/Users/chao/Downloads/la_poi.txt', '/Users/chao/Downloads/la_tasks.txt')







# x = clients[0].venues.search(params={'limit': 100, 'intent':'browse', 'sw':'40.7128, -74.0059', 'ne':'40.7138, -74.0050'})
# print type(x)
# print len(x['venues'])
# print type(x['venues'])
# print x['venues']
# print json.dumps(x['venues'])
# v = x['venues'][0]
# for k,y in v.items():
#     print k, '\t', y
# print v, type(v)

