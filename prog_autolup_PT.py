import sys
import os
import re
import shutil
import subprocess
import glob
import numpy as np
from tools_file_info import get_luplist_txt,get_coord_grrm_com,make_lup_com

## user setting
## read txt file to get pt for lup 
f_lup_path = 'user_txt_format.txt'
f_com      = "your inpt.com" 
pt_dir     = "your directory path with PT files"

dict_lup   = get_luplist_txt(f_lup_path)
## get coord from  *.com
atmname, coord = get_coord_grrm_com(f_com)
f_top = f_com.split(".")[0]


## for path ###
path = os.getcwd()

for key in dict_lup.keys():
    for ipt in range(0,len(dict_lup[key])):
        fn_lup_dir = "%s_%02d_%s_lup"%(key,ipt,dict_lup[key][ipt])
        fn_pt      =  "%s_%s" % (f_top,dict_lup[key][ipt])
        ## write a lup.com 
        make_lup_com(fn_lup_dir,atmname,coord,fn_pt)
        t_dir =        "%s/%s"%(path,fn_lup_dir)
        t_iter1_dir =  "%s/%s1"%(t_dir,fn_lup_dir)
        os.makedirs(t_dir,exist_ok=True)
        os.makedirs(t_iter1_dir,exist_ok=True)
        shutil.copy("./%s.com"%fn_lup_dir,"%s/%s1.com"%(t_iter1_dir,fn_lup_dir))
        shutil.move("./%s.com"%fn_lup_dir, t_dir)
        shutil.copy("%s/%s.log"%(pt_dir,fn_pt), t_iter1_dir) 
        ## replace 
        ##  
        shutil.copy("./jobsubmit_script.sh", t_dir)
        ## change directory
        os.chdir(t_dir)
        subprocess.run("./jobsubmit_script.sh",shell=True)
        os.chdir(path) 





