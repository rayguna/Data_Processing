<b> This folder houses a collection of projects related to data processing.</b>

1. <i> make_montage: </i> A python CLI which takes on a functional approach for generating a montage from a set of images. You can also apply a flat-field normalization to these images.  

2. <i> image_registration: </i> A jupyter notebook with functions to demonstrate features extraction of an object in two images, followed by the calculation of the homography matrix that describes the differences in the image orientation. We can then apply the calculated homography matrix to orient the target image to the reference image. <br>

3. <i> integrate_debye_rings: </i> A python class within a makepyfais.py module that can be imported and used to instantiate PyFAIs object to integrate Debye ring images into an X-ray diffraction pattern. This module relies on the pyFAI library (https://pyfai.readthedocs.io/en/v2023.1/).  

4. <i> generate_faux_si: </i> A jupyter notebook with python script showing how to generate Debye ring image of Si with the specific detector parameters. The generated image is then converted to a 16-bit using imagej.   
~
