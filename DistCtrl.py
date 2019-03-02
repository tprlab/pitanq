import ultradist

class DistCtrl:

    def __init__(self):
        ultradist.init()

    def distance(self):
        return ultradist.distance()


def createDistCtrl():
    return DistCtrl()

if __name__ == '__main__':
    dc = createDistCtrl()
    print (dc.distance())