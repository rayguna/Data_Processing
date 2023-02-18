<b> make_montage </b>

[About]
This script generates a montage of two rows of images. User can also provide the corresponding wf and df images to apply a flat-field normalization.   
Images are read as a numpy array using the plt.imread function. Image subtraction can either be done using the cv2.subtract function rather than numpy subtract or by converting the image numpy array into a 64 bit integer to avoid integer overflow. This is because imread assumes as 32 bit image.
  
[Flat Field Normalization]
Flat Field Normalization:
    - The images can be normalized according to: (data-df)/(wf-df) = a/b.
    - Image is read as numpy array and substracted using the cv2.subtract function.
    - Some regions of the wf-df image may have zero intensities which results in a zero denominator in the above formula. To avoid division by zero, we set b=1 if b<=0.  
    - The flat field normalized image is comparable to data/wf.

[Usage] 
It uses CLI to let user select the different options: 
`
    --normalize: whether to normalize the data or not.
    --vmin: minimum image z-scale.
    --vmax: maximum image z-scale.
    --title_fontsize: plot title font size.
 `   
To get information about the parameters, type:
    `
    python make_montage_v1-0.py --h
    or
    python make_montage_v1-0.py --help
    `
    
Example of usage:
    
    (a)
    `
    - To generate flat field normalized images, place the appropriate images into wf, df, and data subfolders.
    - On an anaconda prompt with the appropiate modules installed, type:
        `
        python make_montage_v1-0.py --normalize True --vmin 0 --vmax 1.5 --title_fontsize 8
        `
    - When prompted, select the main folder in which wf, df, and data subfolders reside and click "Choose".
    - Adjust the vmin and vmax to vary the contrast.
    `
    
    (b)
    `
    - Alternatively, to simply view the raw images, simply place the images within the main folder.
    - On an anaconda prompt with the appropiate modules installed, type: python make_montage_v1-0.py --normalize False --vmin 0 --vmax 4000 --title_fontsize 8
    - When prompted, select the main folder containing the images and click "Choose".
    - Adjust the vmin and vmax to vary the contrast.
    `
[Python Modules]
    - matplotlib: pip install matplotlib
    - numpy: pip install numpy
    - easygui_qt: pip install easygui_qt
    - glob: python standard library (built-in)
    - argparse: pip install argparse

ref.:

    - Python CLI: https://docs.python.org/3/howto/argparse.html
    - https://www.geeksforgeeks.org/how-to-subtract-two-images-using-python-opencv/
~
