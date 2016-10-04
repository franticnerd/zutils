from math import sin, cos, sqrt, atan2, radians

class Location:
    def __init__(self, lat, lng):
        self.lat = float(lat)
        self.lng = float(lng)

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng

    def euclidean_dist(self, l):
        diff_lat = self.lat - l.lat
        diff_lng = self.lng - l.lng
        return sqrt(diff_lat**2 + diff_lng**2)

    def geometric_dist(self, l):
        R = 6373.0
        dlat = radians(self.lat) - radians(l.lat)
        dlng = radians(self.lng) - radians(l.lng)
        a = (sin(dlat/2))**2 + cos(self.lat) * cos(l.lat) * (sin(dlng/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance

if __name__ == '__main__':
    print 'Begin testing Location'
    l1 = Location(52.2296756, 21.0122287)
    l2 = Location(52.406374, 16.9251681)

    print l1.euclidean_dist(l2)
    print l1.geometric_dist(l2)
