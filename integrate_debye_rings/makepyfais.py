import glob
import pyFAI, fabio
import matplotlib.pyplot as plt

class MakePyFAIs:

    def __init__(self, poni_path, lst_labels=[]):
        """Instantiate a list of azimuthal integrators
       Inputs:
        - poni_path (dir): the path in which the poni files are located
        - lst_labels (list): a list of ordered labels that match the poni files to the target images
        
        E.g.:
         - pyFAIs=Make_PyFAIs("poni") #by default, use one poni file to integrate all images.
         - pyFAIs=Make_PyFAIs("poni", ["C1", "C2", "C3", "C4"]) #use 4 poni files to integrate images according to the labels specified in the list
        """
            
        self.lst_ponis=glob.glob("%s/*.poni" %poni_path)
        self.lst_ai=[] #saves a list of azimuthal integrator objects
        
        self.dict_ais={}
        
        self.lst_labels=lst_labels


        # Read poni files
        if self.lst_labels==[]: #a. use only one poni file for all integration
            self.ai=pyFAI.load(self.lst_ponis[0])
                
        else: #b. use labeled poni files
            for poni in self.lst_ponis:
                #self.lst_ai.append(pyFAI.load(poni))
                #print("\nIntegrator: \n", self.lst_ponis[-1]) #check
                for k in self.lst_labels:
                    if k in poni:
                        self.dict_ais[k]=[pyFAI.load(poni)]
                
    def apply_masks(self, dict_ais, lst_masks, labeled2):
        """Append masks to dict_ais. Apply images first, and then apply mask.
        
           Inputs:
            - dict_ponis(dict)=a dictionary of arrays: [poni, img, mask]
            - labeled2(bool)=Mask labels. Either True or False.
            
           Return:
            modified dict_ais
        """
        
        for k in dict_ais.keys():
            if labeled2==True: #append mask according to the labels
                [dict_ais[k].append(mask) for mask in lst_masks if k in mask]
                
            else: #just append one universal mask to all ais.
                dict_ais[k].append(lst_masks[0])
                
        return dict_ais
                
    
    def apply_images(self, dict_ais, lst_imgs, labeled1):
        """Append images to dict_ais. Apply images first, and then apply mask.
        
           Inputs:
            - dict_ponis(dict)=a dictionary of arrays: [poni, img, mask]
            - lst_imgs(list):a list of Debye Ring images (*.tif) 
            - labeled1(bool)=Image labels. Either True or False.
            
            Return:
             modified dict_ais
        """
        
        self.lst_imgs=lst_imgs

        #check if labels are specified (i.e., self.dict_ais!={})
        if labeled1==True: #append mask according to the labels
            for k in dict_ais.keys():
                for img in self.lst_imgs:
                    if k in img:
                        dict_ais[k].append(fabio.open(img).data)

        else: #just append each image to each ais
            dict_ais={}
            for i, img in enumerate(self.lst_imgs):
                if str(i) not in dict_ais.keys(): #add the same poni as the first element
                    dict_ais[str(i)]=[self.ai]

                dict_ais[str(i)].append(fabio.open(img).data)
                
        return dict_ais
    
    
    def integrate(self, img_path, mask_path=None):
        """Integrate list of images from the compiled dictionary.
        
           Inputs:
            - img_path (dir): the path in which distortion corrected images (*.tif) are located
            - mask_path(dir): the path in which mask files (*.edf) are located
        """


        print("Processing... Please wait...")


        self.dict_XRDs={}

        self.mask_path=mask_path
        
        # Read images 
        self.lst_imgs=glob.glob("%s/*.tif" %img_path)
        
        #read masks
        self.lst_masks=glob.glob("%s/*.edf" %mask_path)
        
        #if dict_ais check if mask is true or false
        #check if number of labels equals the number of ponis and images
        if len(self.lst_labels)==len(self.lst_ponis) and len(self.lst_ponis)==len(self.lst_imgs): #no labels
            labeled1=True
            print("The corresponding poni files are applied to each image according to the provided labels.")
        else:
            labeled1=False
            print("Only one poni file is applied to all image(s)")


        #apply images
        self.dict_ais=self.apply_images(self.dict_ais, self.lst_imgs, labeled1)
        
        #apply masks only if provided or if user-specifies
        if self.mask_path!=None and self.lst_masks!=[]:
            #check if the labels match the mask filenames
            check_mask_labels=True
            labels_match_masks=0

            for label in self.lst_labels:
                for mask in self.lst_masks:
                    if label in mask:
                        labels_match_masks+=1

            if labels_match_masks==len(self.lst_labels):
                check_mask_labels=True
            else:
                check_mask_labels=False

            #check if number of masks equals number of images    
            if len(self.lst_labels)==len(self.lst_masks) and len(self.lst_imgs)==len(self.lst_masks) and check_mask_labels:
                labeled2=True
                print("Mask(s) are applied according to the provided labels.")
            else:
                labeled2=False
                print("One mask(s) is applied to all images. To apply separate masks, label mask file names according to the provided labels.")

            self.dict_ais=self.apply_masks(self.dict_ais, self.lst_masks, labeled2)
        

        #perform integration
        for k,v in self.dict_ais.items():
            if self.lst_masks!=[] or self.lst_masks!=[]: #if mask is provided
                res = self.dict_ais[k][0].integrate1d(self.dict_ais[k][1],
                                1000, mask=fabio.open(self.dict_ais[k][2]).data,
                                unit="2th_deg")
            else: #if no mask is provided
                res = self.dict_ais[k][0].integrate1d(self.dict_ais[k][1],
                             1000, unit="2th_deg")
            
            self.dict_XRDs[k]=[res.radial, res.intensity]
                   
        return self.dict_XRDs
        
    def create_a_montage(self):
        """Plot both the images and the integrated XRD patterns
        """
        
        plt.figure(figsize=(10, 5))
        
        for i, k in enumerate(self.dict_ais.keys()):
            plt.subplot(2, len(self.lst_imgs), i+1)
            
            title=self.lst_imgs[i].split("\\")[-1].split(".")[0]
            plt.title(title, fontsize=8)
            plt.imshow(self.dict_ais[k][1], cmap='gray', vmax=500)
            
            #if mask is provided, overlay it
            if len(self.lst_masks) != 0 and self.mask_path != None:
                plt.imshow(fabio.open(self.dict_ais[k][2]).data, alpha=0.5)

            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)

            
            plt.subplot(2, len(self.lst_imgs), i+len(self.lst_imgs)+1)
            plt.plot(self.dict_XRDs[k][0], self.dict_XRDs[k][1])
            
        plt.tight_layout()
        plt.show()
        
        print("Done!")
        print("")