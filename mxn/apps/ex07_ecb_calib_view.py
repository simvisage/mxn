'''
Created on 27. 2. 2014

@author: Vancikv
'''

from mxn import \
    ECBCalib, ECBCalibModelView
    
ec = ECBCalib(Mu=3.49)
ecw = ECBCalibModelView(model=ec)
ecw.configure_traits()

