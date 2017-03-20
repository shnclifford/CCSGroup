
"""Module for computing the Structural Similarity Image Metric (SSIM)."""

from ssim.ssimlib import SSIM
from ssim.ssimlib import SSIMImage
from ssim.ssimlib import get_gaussian_kernel
from ssim.compat import Image
from sklearn import datasets

def compute_ssim(image1, image2, gaussian_kernel_sigma=1.5,
                 gaussian_kernel_width=11):
    """Computes SSIM.
    Args:
      im1: First PIL Image object to compare.
      im2: Second PIL Image object to compare.
    Returns:
      SSIM float value.
    """
    gaussian_kernel_1d = get_gaussian_kernel(
        gaussian_kernel_width, gaussian_kernel_sigma)
    return SSIM(image1, gaussian_kernel_1d).ssim_value(image2)

img1 = Image.open("images/1.png")
digits = datasets.load_digits()

print compute_ssim(img1, img2)