### image_registration

Image registration is needed to align multiple images that are captured using different cameras to make the coordinates equivalent. Here, we use two functions to align a target image to a reference image:
- calculate_homography_matrix() <br>
- apply_homography_matrix() <br>

The first function calculates the homography matrix. The second function applies the homography matrix to correct the orientation of the target image.

