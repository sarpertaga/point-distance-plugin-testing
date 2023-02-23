from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination)

class PointDistanceAlgorithm(QgsProcessingAlgorithm):

    first = "First Input"
    second = "Second Input"
    output = "Output"
    
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.first,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.second,
                self.tr('Second layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        self.addParameter(
                QgsProcessingParameterFileDestination(
                    self.output,
                    self.tr('Output File'),
                    'Distance as "km"',
                )
            )
            
    def processAlgorithm(self, parameters, context, feedback):
        first, second = self.parameterAsSource(parameters, self.first, self.second, context)
        distance = self.parameterAsFileOutput(parameters, self.output, context)

            sLayers = QgsProject.instance().mapLayersByName(first)
            sLayer = sLayers[0]

            sFeat = sLayer.getFeature(0)
            tFeat = sLayer.getFeature(0)

            sGeom = sFeat.geometry()
            tGeom = tFeat.geometry()

            dist = sGeom.distance(tGeom)

            #print(dist)

            tLayers = QgsProject.instance().mapLayersByName(second)
            tLayer = tLayers[0]
            tFeats = tLayer.getFeatures()
            sFeats = sLayer.getFeatures()

            for sfeat in sFeats:
                sgeom = sfeat.geometry()
                for tfeat in tFeats:
                    tgeom = tfeat.geometry()
                    dist_2 = ((sgeom.distance(tgeom))/2)/100000, "km"
                    #print(sfeat.id(), tfeat.id(), dist_2)
            
            return (self.output: distance)
    
    def name(self):
        return 'point_distance'

    def displayName(self):
        return self.tr('Distance Between two Points')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PointDistanceAlgorithm()
