from .point_distance import PointDistancePlugin

def classFactory(iface):
    return PointDistancePlugin(iface)