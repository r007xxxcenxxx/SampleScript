# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 01:23:40 2019

@author: flower
"""

# using for plotting the electric properties from BoltzTraP results with pymatgen
# with many help from STMD-UCL/SUMO
import argparse
import  pymatgen.electronic_structure.boltztrap as BZ

parser = argparse.ArgumentParser()
parser.add_argument('-d','--directory ', type = str, default='./',
                       help='The directory in which to save files.' )  
parser.add_argument('-f','--file', type = str, default='~/soft/ovito-2.9.0-x86_64/bin/ovitos',
                        help='the directory of BoltzTraP result' ) # maybe can rename prefix to boltztrap. 
parser.add_argument('-p', '--property', type = str, default='seeb', 
                        choices=['seeb','cond','PF'],
                        help='which type of properties need plotted')
parser.add_argument('--xlim', type = list, default=[1E18,1E21], 
                        help='the range of x axis'))
parser.add_argument('--xscale', type = str, default='symlog',
                        choices=['symlog','linear'],
                        help='which type of xscale want to use, will divide minmum X if linear')
parser.add_argument('plot_with', type = str, default='n',
                        choices=['n','T'],
                        help='plot properties with concentratino or T' )
args = parser.parse_args()    
print (args)
aaa = args.ENCUT
class get_data():
    def __init__(self, f):
        
        pass
    def seeb(self, f):
        print ("yayaya" + str(aaa))
        return 0 # 應該是傳回一個字典，包含{["p"][T], ["n"][T0]} e
    def cond(self, f):
        print ("hahah")
    def PF(self, f):
        
a = getattr(get_data(), args.functino)
a()
