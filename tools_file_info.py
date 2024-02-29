import numpy as np
import os

def tools_check_com_log(top_file_name): 
    block_info = {} 
    com_file = []
    log_file = []
    path = os.getcwd()
    file_list = os.listdir(path)
    fn_data = []
    for ifile in range(0,len(file_list)):
        if top_file_name in file_list[ifile] and ".com" in file_list[ifile] :
            com_file.append(file_list[ifile].split(".com")[0]) 
        elif top_file_name in file_list[ifile] and ".log" in file_list[ifile] :
            log_file.append(file_list[ifile].split(".log")[0]) 
    block_info["log_file"]  =  log_file
    block_info["com_file"]  =  com_file
    fn_data.append(block_info)
    return(fn_data) 

def tools_natom_grrm_com(fn):
    fdata = open(fn)
    natom = 0
    line=True
    while line:
        line = fdata.readline()
        tmp = line.split()
        if len(tmp) == 4 or len(tmp) == 5:
            line = fdata.readline()
            while 1:
                natom=natom+1
                line = fdata.readline()
                if "ptions" in line:
                    break
        if natom >0:
            break
    fdata.close()
    return(natom)

def get_coord_grrm_com(fn):
    atmname = []
    coord   = []

    fdata = open(fn)
    natom = 0
    line=True
    while line:
        line = fdata.readline()
        tmp = line.split()
        if len(tmp) == 4 or len(tmp) == 5:
            t_coord = []
            #ttmp = line.split() 
            t_coord.append(float(tmp[1]))
            t_coord.append(float(tmp[2]))
            t_coord.append(float(tmp[3]))
            coord.append(t_coord)
            atmname.append(tmp[0])
        if "ptions" in line:
            break
    fdata.close()
    return atmname,coord 

def get_frozen_coor(file_name): # file name ***.com
    atomname = []
    xyz = []
    fdata = open(file_name)
    line = True
    while line:
        line = fdata.readline()
        if "frozen" in line.lower():
            while 1:
                line = fdata.readline()
                if "option" in line.lower():
                    break
                else:
                    tmp_xyz = []
                    tmp = line.split()
                    atomname.append(tmp[0])
                    tmp_xyz.append(float(tmp[1]))
                    tmp_xyz.append(float(tmp[2]))
                    tmp_xyz.append(float(tmp[3]))
                    xyz.append(tmp_xyz)
    fdata.close()
    return(atomname,xyz)


def get_luplist_txt(luplist_txt):
# the luplist should be like this ##
# ------------------------------------------------------
# # G7G4_re_Rprod
# Path-37 for G4-G7    PT54175      181.3 kj/mol [Elec]
# Path-36 for G4-G7    PT54041      185.9 kj/mol [Elec]
# # G7G24_re_Ccation
# Path-55 for G7-G24    PT18279      160.7 kj/mol [Elec]
# Path-51 for G7-G24    PT17803      171.4 kj/mol [Elec]
# ....--------------------------------------------------
    dict_lup = {}
    # ファイルを読み込んで処理
    with open(luplist_txt, 'r') as f:
        lines = f.readlines()
    for iline in lines:
        if "#" in iline:
            t_key = iline.split("#")[1].strip()
            dict_lup[t_key] = []
        if "PT" in iline:
            t_line = iline.split()
            if len(t_line) != 0:
                dict_lup[t_key].append(t_line[3])

    #for key in dict_lup.keys():
    #    for ipt in range(0,len(dict_lup[key])):
    #        f_lup_name = "%s_%s_%s"%(key,ipt,dict_lup[key][ipt])

    return dict_lup 


def make_lup_com(fn_lup,atmname, coord, ptlog):
    f_lup = open("%s.com"%fn_lup,"w")
    f_lup.write("%%Infile=%s\n"%ptlog)
    f_lup.write("%%link=non-supported\n")
    f_lup.write("# LUP\n")
    f_lup.write("\n")
    f_lup.write("0 1\n")
    for iatm in range(0,len(atmname)):
        f_lup.write("%-2s\t%17.12f\t%17.12f\t%17.12f\n" \
                    % (atmname[iatm],\
                       float(coord[iatm][0]),\
                       float(coord[iatm][1]),\
                       float(coord[iatm][2])))
    f_lup.write("Options\n")
    f_lup.write("DownDC=99999\n")
    f_lup.write("KeepLUPPaths\n")
    f_lup.write("MaxLUPITR=100 100\n")
    f_lup.write("GetConvergedLUPTOP\n")
    f_lup.write("MinFreqValue=50.000000000000\n")
    f_lup.write("EigenCheck\n")
    f_lup.write("Derivative = Force\n")
    f_lup.write("GauProc=2\n")
    f_lup.write("Temperature = 333.15\n")
    f_lup.close()

def make_sadd_com(fn_com, coord):
    f_lup = open("%s.com"%fn_com,"w")
    f_lup.write("%%link=non-supported\n")
    f_lup.write("# Saddle\n")
    f_lup.write("\n")
    f_lup.write("0 1\n")
    for iatm in range(0,len(coord)):
        f_lup.write(coord[iatm])
    f_lup.write("Options\n")
    f_lup.write("Saddle+IRC\n")
    f_lup.write("MinFreqValue=50.000000000000\n")
    f_lup.write("EigenCheck\n")
    f_lup.write("Derivative = Force\n")
    f_lup.write("Temperature = 333.15\n")
    f_lup.write("Gauproc = 2\n")
    f_lup.close()


