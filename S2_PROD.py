#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
# from osgeo import gdal
# import osgeo
import rasterio


class S2_PROD():
    
    def __init__(self, path2prod):
        self.path_to_prod = path2prod
        self.metadata_path =  glob.glob(os.path.join(path2prod, 'MTD*.xml'))[0]
        self.manifest = glob.glob(os.path.join(path2prod, 'manifest.safe'))[0]
        # Read metadata file 
        tree = ET.parse(self.metadata_path)
        self.MTD = tree.getroot()
        # Orbit number
        self.Orbit = self.MTD.find('.//SENSING_ORBIT_NUMBER').text
        # Satellite
        self.Sat = self.MTD.find('.//SPACECRAFT_NAME').text
        # product level
        self.Prod_level = self.MTD.find('.//PROCESSING_LEVEL').text
        # Acquisition start
        self.Acq_start = self.MTD.find('.//PRODUCT_START_TIME')
        
        # TCI
        Img_list = self.MTD.findall('.//IMAGE_FILE')
        for i in range(len(Img_list)):
            if (Img_list[i].text.find('TCI_10m') != -1):
                self.TCI_10m = self.S2_band(os.path.join(self.path_to_prod,Img_list[i].text + '.jp2'))
        
        
    class S2_band():
    
        def __init__(self, path2band):
            self.path = path2band
            self.data = rasterio.open(self.path)
            self.crs = self.data.crs
            
            index = self.data.indexes 
            
            img_tmp = np.zeros([int(self.data.width), int(self.data.height), int(self.data.count)])
            for i in range(len(index)):
                img_tmp[:,:,i] = self.data.read(i+1)
                
            self.img = img_tmp
            del img_tmp
            
        
        def show(self):
            
            plt.figure()
            plt.imshow(self.img.astype(int))
        
        
        
        
