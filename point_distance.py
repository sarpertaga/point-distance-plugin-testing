import os
import sys
import inspect
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingAlgorithm, QgsApplication
import processing
from .point_distance_provider import PointDistanceProvider


cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class PointDistancePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initProcessing(self):
      self.provider = PointDistanceProvider()
      QgsApplication.processingRegistry().addProvider(self.provider)
        
    def initGui(self):
      self.initProcessing()
      icon = os.path.join(os.path.join(cmd_folder, 'logo.png'))
      self.action = QAction(QIcon(icon), 'Distance Between Points', self.iface.mainWindow())
      self.action.triggered.connect(self.run)
      self.iface.addPluginToMenu('&Point Distance', self.action)
      self.iface.addToolBarIcon(self.action)

    def unload(self):
      QgsApplication.processingRegistry().removeProvider(self.provider)
      self.iface.removeToolBarIcon(self.action)
      self.iface.removePluginMenu('&Point Distance', self.action)  
      del self.action

    def run(self):
      processing.execAlgorithmDialog('point_distance:point_distance')