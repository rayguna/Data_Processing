# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:52:17 2023
@author: Ray Gunawidjaja


[About]
This script generates a montage of two rows of images.
User can also provide the corresponding wf and df images to apply a flat-field normalization.   
Images are read as a numpy array using the plt.imread function. 
Image subtraction can either be done using the cv2.subtract function rather than numpy subtract or by 
 converting the image numpy array into a 64 bit integer to avoid integer overflow.
  This is because imread assumes as 32 bit image.
  
[Flat Field Normalization]
Flat Field Normalization:
    -The images can be normalized according to: (data-df)/(wf-df) = a/b.
    -Image is read as numpy array and substracted using the cv2.subtract function.
    -Some regions of the wf-df image may have zero intensities which results in a zero denominator in the above formula.
     To avoid division by zero, we set b=1 if b<=0.  
    -The flat field normalized image is comparable to data/wf.

[Usage] 
It uses CLI to let user select the different options: 
    --normalize: whether to normalize the data or not.
    --vmin: minimum image z-scale.
    --vmax: maximum image z-scale.
    --title_fontsize: plot title font size.
    
To get information about the parameters, type:
    python make_montage_v1-0.py --h
    or
    python make_montage_v1-0.py --help

Example of usage:
    (a)
    -To generate flat field normalized images, place the appropriate images into wf, df, and data subfolders.
    -On an anaconda prompt with the appropiate modules installed, type: 
        python make_montage.py --normalize True --vmin 0 --vmax 1.5 --title_fontsize 8
    -When prompted, select the main folder in which wf, df, and data subfolders reside and click "Choose".
    -Adjust the vmin and vmax to vary the contrast.
    
    (b)
    -Alternatively, to simply view the raw images, simply place the images within the main folder.
    -On an anaconda prompt with the appropiate modules installed, type: 
        python make_montage.py --normalize False --vmin 0 --vmax 4000 --title_fontsize 8
    -When prompted, select the main folder containing the images and click "Choose".
    -Adjust the vmin and vmax to vary the contrast.
    
[Python Modules]
    -matplotlib: pip install matplotlib
    -numpy: pip install numpy
    -easygui_qt: pip install easygui_qt
    -pyqt5: pip install PyQt5
    -glob: python standard library (built-in)
    -argparse: pip install argparse

ref.:
    - Python CLI: https://docs.python.org/3/howto/argparse.html
    - https://www.geeksforgeeks.org/how-to-subtract-two-images-using-python-opencv/
"""

import matplotlib.pyplot as plt
import numpy as np
import easygui_qt as easy
import glob
import argparse




def my_bool(s):
    """pass a boolean argument
       ref.: https://copyprogramming.com/howto/argparse-not-parsing-boolean-arguments#argparse-not-parsing-boolean-arguments
    """
    
    return s != 'False'

parser = argparse.ArgumentParser()
parser.add_argument("--normalize", default=True, type=my_bool,
                    help="Choose whether to normalize the image. Set it to 1 for True or 0 for False.")
parser.add_argument("--vmin", type=float, help="Set minimum image z-scale")
parser.add_argument("--vmax", type=float, help="Set maximum image z-scale")
parser.add_argument("--title_fontsize", type=int, help="Change plot title fontsize. Set the value to 0 to disable plot title.")


args = parser.parse_args()


def main():
    """Read WF, DF, and data image files and save to dictionaries
    """
    
    dir=easy.get_directory_name()
    
    if dir !="":
    
        lst_subfolders=["WF","DF","Data"]
        
        #read images and store into dictionaries
        dictTIF, dictFilenames = read_images(dir, lst_subfolders)
                    
        #make montage from the image files
        make_montage(dictTIF, dictFilenames, lst_subfolders)
    
    else:
        print("No path has been selected.")                


def read_images(dir, lst_subfolders):
    """Read images and store into dictionaries
    
       inputs:
           dir (path): directory where WF, DF, and Data subfolders are located.
           lst_subfolders (list): a list of subfolder names in which the various images are stored, e.g., ["DF", "WF", "Data"].
           
       return:
           dict_tif (dictionary): a list of tif files corresponding to the keys specified in the subfolders list.
           dict_filenames (dictionary): a list of filenames corresponding to the keys specified in the subfolders list.
    """
    
    #get wf, df, and data
    #iterate through subfolders
    
    dict_tif={}
    dict_filenames={}
    
    #store images into a dictionary
    for subfolder in lst_subfolders:
        for filepath in glob.glob("%s/%s/*.tif" %(dir, subfolder)):
            #print(file) #check
            #read image and store into a dictionary    
    
            im=np.array(plt.imread(filepath), dtype='int64') #np.array(Image.open(filepath)) #change to 64 bit to avoid an integer overflow
                
            filename=filepath.split("/")[-1].split("\\")[-1].split(".")[0]
            
            if subfolder not in dict_tif.keys() and subfolder not in dict_filenames.keys():
                dict_tif[subfolder]=[]
                dict_tif[subfolder].append(im)
                
                dict_filenames[subfolder]=[]
                
                dict_filenames[subfolder].append(filename)
                
            else:
                dict_tif[subfolder].append(im)
                
                dict_filenames[subfolder].append(filename)
        
    return dict_tif, dict_filenames
    

def make_montage(dict_tif, dict_filenames, lst_subfolders):
    """Make a montage from images extracted from the subfolders list.
    
       inputs:
           dict_tif (dictionary): a list of tif files corresponding to the keys specified in the subfolders list.
           dict_filenames (dictionary): a list of filenames corresponding to the keys specified in the subfolders list.
           lst_subfolders (list): a list of subfolder names in which the various images are stored, e.g., ["DF", "WF", "Data"].
           
       return: 
           None
        
       output:
           display a 2 x int(no_imgs/2) montage.
    """
        
    #display images
    no_imgs=len(dict_tif[lst_subfolders[-1]])
      

    #initialize img
    arr_img=np.zeros([1024,1024])
    
    for i in range(no_imgs):
    
        if args.normalize: #normalize images as: (data-df)/(wf-df)
           
            arr_img= ff_normalize(dict_tif["Data"][i], dict_tif["WF"][i], dict_tif["DF"][i]) #np.divide(a,b)

        else: #don't normalize    
        
            arr_img=dict_tif["Data"][i]
            
        #sort images 
        #(a) assuming a four 2-frame cameras and the sequence is: 
        #   C1-frame1, C2-frame1, C3-frame1, C4-frame1, C1-frame2, C2-frame2, C3-frame2, C4-frame2 
        if not i%2: #if odd
            plt.subplot(2, int(no_imgs/2), int((i+2)/2))
        
        else: #if even
            plt.subplot(2, int(no_imgs/2), int(4+(i+2)/2))
        #End of a four 2-frame cameras-------------------------------------------------------------

        #(b) for a normal sequential images, comment the above block and replace it with:
        #plt.subplot(2, int(no_imgs/2), int(i+1))
        #End of images-----------------------------------------------------------------------------
            
        plt.imshow(arr_img, cmap='gray', vmin=args.vmin, vmax=args.vmax)
        
        if args.title_fontsize>0: #display title only if value is >0
            plt.title(dict_filenames["Data"][i], fontsize=args.title_fontsize)
        
    plt.show()
    
    
def ff_normalize(arr_data, arr_wf, arr_df):
    """Perform a flat field normalization: (arr_data-arr_df)/(arr_wf-arr_df).
    
       inputs:
           -data (numpy array): raw image
           -wf (numpy array): whitefield image
           -df (numpy array): darkfield image
           
       return:
           -a flat-field normalized image (numpy array)
    """
    
    #first, make sure that the iages are 64 bit. Otherwise, it can trigger an integer overflow.
    arr_data=np.array(arr_data, dtype='int64')
    arr_wf=np.array(arr_wf, dtype='int64')
    arr_df=np.array(arr_df, dtype='int64')
    
    a=arr_data-arr_df
    b=arr_wf-arr_df
    
    #avoid division by zero
    b[b<=0]=1
    
    #normalize data
    ff=np.divide(a,b)
    
    return ff

    
            
if __name__ == "__main__":
    main()


