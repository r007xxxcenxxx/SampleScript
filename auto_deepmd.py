# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 23:55:30 2018

這是整套deepMD迭代腳本，可以自動的實現迭代訓練，得到較好的model

this is the iterate script for deepMD, which can train models automatically.

directory structure (defalut):
    |----DFT_1
        |----train
        |----MD
    |----DFT_2
        |----train
        |----MD
    |----DFT_3
        |----train
        |----MD

@author: flower

第一個版本先把MD完的結果與lcurve比對，然後自動挑出deviation 太大的，轉乘POSCAR，然後自己DFT

V1 : Compare between the results from MD and training, and choose configuration which deviation is among 1.5~3 times loss.
     Transform the lammps configurations to VASP POSCARs, and do the single point energy calculation.

"""
def get_l2_loss(refer_criteria):
    if refer_criteria == 'l2_f':
        index_refer = 6
    elif refer_criteria == 'l2_e':
        index_refer= 4
    elif  refer_criteria == 'l2_v':
        index_refer = 8
    else:
        index_refer = 2
    l2_tst = []
    Infile = open("lcurve.out","r")
    FileContent = Infile.readlines()
    Infile.close()
    FileContent = FileContent[1:-1]
    for line in FileContent:
        linecontent=line.split()
        l2_tst.append(float(linecontent[index_refer]))
	# avoid the case that linecontent is empty, 
    return l2_tst

def pick_deviation(l2_tst, devi_criteria):
    #default to pick devi_max_force
    avg_l2_tst = np.mean(l2_tst)
    devi_lo = 1.5 * avg_l2_tst
    devi_hi = 3 * avg_l2_tst
    if devi_criteria == 'max_forces':
        index_devi = 5
    elif devi_criteria == 'max_energy':
        index_devi= 2
    elif  devi_criteria == 'avg_forces':
        index_devi = 7
    else: #need to be modified
        index_devi = 5
    index_configuration = []
    Infile = open("model_devi.out","r")
    FileContent = Infile.readlines()
    Infile.close()
    FileContent = FileContent[1:-1]
    for line in FileContent:
        linecontent=line.split()
        if devi_hi > float(linecontent[index_devi]) > devi_lo:
            index_configuration.append(linecontent[0])
    print ("the deviation criteria is " + devi_criteria + ", the value is " + str(avg_l2_tst))
    print ("the configurations are")
    print (index_configuration)
    return index_configuration
def auto_DFT(index_configuration, ovitos, ovito_file_convert,input_vasp, vasp_run, dft_path):
    DFT_iter = 1 #whole training times, need to be extansed
    DFT_path_iter = dft_path + "/DFT_" + str(DFT_iter) + "/"
    md_path = os.getcwd()
    os.mkdir(DFT_path_iter)
    for i in index_configuration:
        lmp_dump = "result." + i + ".dump"
        corresponding_poscar = "POSCAR" + i
        os.system( ovitos + " " + ovito_file_convert + " -m vasp " + lmp_dump + " " + corresponding_poscar)
        DFT_for_iter = DFT_path_iter + i #whole DFT times each iteration
        os.mkdir(DFT_for_iter)
        os.system("cp " + corresponding_poscar+ " " + DFT_for_iter+"/POSCAR")
        os.system("cp " + input_vasp + "INCAR" + " " + DFT_for_iter+"/INCAR")
        os.system("cp " + input_vasp + "POTCAR" + " " + DFT_for_iter+"/POTCAR")
        #        os.system("cp " + input_vasp + "KPOINTS" + DFT_path+i+"/KPOINTS")
        #        dont need KPOINTS if KSPACING in INCAR
        os.chdir(DFT_for_iter)
        os.system(vasp_run)
        os.chdir(md_path)
    os.chdir(dft_path)
def main():
    parser = argparse.ArgumentParser(description='The setting for whole deepMD iteration')
    #TODO:
    #    more options, like  hyperparameters
    #
    parser.add_argument('-d','--deviation', type = str, default='max_forces', 
                        choices=['max_forces','max_energy','avg_forces'],help='Choose the criterion for iteration' )     
    parser.add_argument('-l','--loss', type = str, default='l2_f', 
                        choices=['l2_f','l2_e','l2_v','l2'],help='Choose the refer for iteration' )     

    parser.add_argument('-e','--ENCUT', type = int, default=300,
                        help='the ENCUT in INCAR for vasp' )  
    parser.add_argument('-o','--ovitos', type = str, default='~/soft/ovito-2.9.0-x86_64/bin/ovitos',
                        help='the bin directory of ovito software' )
    parser.add_argument('-O','--ovito_file_convert', type = str, default='~/hkr/ovito_file_convert.py',
                        help='where is ovito_file_convert.py ?')
    parser.add_argument('-i','--input_vasp', type = str, default="~/hkr/Cu2Se/",
                        help='where is INPUT files for vasp, eg: INCAR, POTCAR, KPOINTS ?')
    parser.add_argument('--vasp_run', type = str, default="nohup vasp_gpu 2>err 1>out &",
                        help='the command for VASP calculation')
    parser.add_argument('--dft_path', type = str,default="/home/lzhpc/hkr/deepmd/222/train/MD/deepmd",
                        help='where to do the iteration, must be given')

    
    args = parser.parse_args()    
    l2_tst = get_l2_loss(args.loss) #get choosen l2_loss from lcurve.out
    index_configuration = pick_deviation(l2_tst, args.deviation ) #get the index for corresponding configuration
    auto_DFT(index_configuration, args.ovitos, args.ovito_file_convert, args.input_vasp, args.vasp_run,args.dft_path)
    #lmp2vasp(index_configuration) #transfer lmp.dump into POSCAR for VASP, run VASP
    #train()
 

    
if __name__ == "__main__":
    import sys
    import numpy as np
    import argparse 
    import os
    
    sys.exit(main())
