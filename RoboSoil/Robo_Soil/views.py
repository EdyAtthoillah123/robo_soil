from django.shortcuts import render
import cv2
import numpy as np
from matplotlib import pyplot as plt

def home(request):
    context={}
    return render(request, "Structures/home.html", context)

def compute_lbp(image):
    lbp_image = np.zeros_like(image)
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            center = image[i, j]
            code = 0
            code |= (image[i - 1, j - 1] > center) << 7
            code |= (image[i - 1, j] > center) << 6
            code |= (image[i - 1, j + 1] > center) << 5
            code |= (image[i, j + 1] > center) << 4
            code |= (image[i + 1, j + 1] > center) << 3
            code |= (image[i + 1, j] > center) << 2
            code |= (image[i + 1, j - 1] > center) << 1
            code |= (image[i, j - 1] > center) << 0
            lbp_image[i, j] = code
    return lbp_image


def lbp(request):
    # Crop Image
    image = cv2.imread('media/image1.png')
    width, height = 640, 480
    original_height, original_width = image.shape[:2]
    center_x, center_y = original_width // 2, original_height // 2
    top_left_x = center_x - (width // 2)
    top_left_y = center_y - (height // 2)
    bottom_right_x = center_x + (width // 2)
    bottom_right_y = center_y + (height // 2)
    cropped_image = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    resized_image = cv2.resize(cropped_image, (width, height))
    cv2.imwrite('media/hasil_pemangkasan.jpg', resized_image)
    # cv2.imshow('Hasil Pemangkasan', resized_image)
    # GrayScale
    # img = cv2.imread('media/hasil_pemangkasan.jpg')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('media/grayscale.jpg',gray)
    img = cv2.imread('media/hasil_pemangkasan.jpg', cv2.IMREAD_GRAYSCALE)
    equalized_image = cv2.equalizeHist(img)
    kernel = np.array([ [1, 2, 1],
                        [2, 4, 2],
                        [1, 2, 1] ]) / 16.0

    filtered_image = cv2.filter2D(equalized_image, -1, kernel)
    lbp_result = compute_lbp(filtered_image)
    lbp_histogram, _ = np.histogram(lbp_result, bins=np.arange(257), range=(0, 256))
    min_val = min(lbp_histogram)
    max_val = max(lbp_histogram)

    normalized_histogram = [(x - min_val) / (max_val - min_val) for x in lbp_histogram]
    print("Histogram LBP (Setelah Normalisasi):")
    print(normalized_histogram)

    # Atau menyimpannya ke file
    np.savetxt('media/histogram_lbp_normalized.txt', normalized_histogram)
    print("Histogram LBP:")
    print(lbp_histogram)
    print(normalized_histogram)
    mode_value = max(lbp_histogram)

    print("Nilai tertinggi dalam histogram LBP adalah:", mode_value)
    
    cv2.imwrite('media/hasil_lbp.jpg', lbp_result)
    cv2.imshow('Hasil LBP', lbp_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    # cv2.imwrite('hasil_equalisasi_dan_tapis.jpg', filtered_image)
    # cv2.imshow('Hasil Equalisasi dan Tapis', filtered_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow('GrayScale', gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

	
# def get_pixel(img, center, x, y):
	
# 	new_value = 0
	
# 	try:
# 		# If local neighbourhood pixel
# 		# value is greater than or equal
# 		# to center pixel values then
# 		# set it to 1
# 		if img[x][y] >= center:
# 			new_value = 1
			
# 	except:
# 		# Exception is required when
# 		# neighbourhood value of a center
# 		# pixel value is null i.e. values
# 		# present at boundaries.
# 		pass
	
# 	return new_value

# Function for calculating LBP
# def lbp_calculated_pixel(img, x, y):

# 	center = img[x][y]

# 	val_ar = []
	
# 	# top_left
# 	val_ar.append(get_pixel(img, center, x-1, y-1))
	
# 	# top
# 	val_ar.append(get_pixel(img, center, x-1, y))
	
# 	# top_right
# 	val_ar.append(get_pixel(img, center, x-1, y + 1))
	
# 	# right
# 	val_ar.append(get_pixel(img, center, x, y + 1))
	
# 	# bottom_right
# 	val_ar.append(get_pixel(img, center, x + 1, y + 1))
	
# 	# bottom
# 	val_ar.append(get_pixel(img, center, x + 1, y))
	
# 	# bottom_left
# 	val_ar.append(get_pixel(img, center, x + 1, y-1))
	
# 	# left
# 	val_ar.append(get_pixel(img, center, x, y-1))
	
# 	# Now, we need to convert binary
# 	# values to decimal
# 	power_val = [1, 2, 4, 8, 16, 32, 64, 128]

# 	val = 0
	
# 	for i in range(len(val_ar)):
# 		val += val_ar[i] * power_val[i]
		
# 	return val

# def lbp(request):
#     path = 'media/foto-aerial-kuk.jpeg'
#     img_bgr = cv2.imread(path, 1)

#     height, width, _ = img_bgr.shape

#     # We need to convert RGB image
#     # into gray one because gray
#     # image has one channel only.
#     img_gray = cv2.cvtColor(img_bgr,
#                             cv2.COLOR_BGR2GRAY)

#     # Create a numpy array as
#     # the same height and width
#     # of RGB image
#     img_lbp = np.zeros((height, width),
#                     np.uint8)

#     for i in range(0, height):
#         for j in range(0, width):
#             img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)

#     plt.imshow(img_bgr)
#     plt.show()

#     plt.imshow(img_lbp, cmap ="gray")
#     plt.show()

#     print("LBP Program is finished")
