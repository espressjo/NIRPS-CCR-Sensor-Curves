#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 12:18:23 2021

@author: noboru
"""
from matplotlib import pyplot as plt
import pandas as pd
from os.path import join,isfile
from os import listdir,getcwd
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from sys import argv

p = [ arg.replace('--path=','') for arg in argv if '--path' in arg]
if len(p)<1: 
    p = getcwd()
else:
    p = p[0]
path_etc = join(p,'etc')
path_ccr = join(p,'CCR_Sensors')
path_figure = join(p,'figures')
path_ls = join(p,'lakeshore_database')
sensor = [f.replace('.csv.out','') for f in listdir(path_ccr) if all(['X' in f,'.csv.out' in f]) ]
import seaborn as sns
if not isfile(join(path_etc,'header.csv')):
    print('header.csv should be in %s'%p)
    exit(0)
header = pd.read_csv(join(path_etc,'header.csv'))
sns.set_theme()
with PdfPages(join(p,'sensor_curves.pdf')) as pdf:
    for sens in sensor:
        f,ax = plt.subplots()
        desc = ''
        if sens in header:
            desc = header[sens].to_numpy()[0]
        data_ls = pd.read_csv(join(path_ls,sens+'.fix'))
        data_copl = pd.read_csv(join(path_ccr,sens+'.csv.out'))
        x,y = data_ls['temperature'],data_ls['resistance']
        ax.plot(x.to_numpy(),(y.to_numpy()),'o',markersize=2,label='man. curve')
        x,y = data_copl['temperature'],data_copl['resistance']
        ax.plot(x.to_numpy(),10**(y.to_numpy()),'o',markersize=2,label='COPL curve')
        ax.legend()
        ax.set(title="%s\n%s"%(sens,desc),xlabel='temperature (°K)',ylabel='Resistance (OHM)')
        ax.set_xlim([90,300])
        ax.set_ylim([160,1035])
        
        plt.tight_layout()
        pdf.savefig(f)
        f.savefig(join(path_figure,"%s.png"%sens))
        plt.close()
    d = pdf.infodict()
    d['Title'] = 'CCR Lakeshore Sensor Curves'
    d['Author'] = 'Jonathan St-Antoine'
    d['Subject'] = 'Sensor curves for CCR Lakeshore 1 and 2'
    d['Keywords'] = 'Sensor curves for CCR Lakeshore 1 and 2'
    d['CreationDate'] = datetime.now().strftime("%Y-%m-%d")
    d['ModDate'] = datetime.today()