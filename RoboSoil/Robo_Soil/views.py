from django.shortcuts import render
import cv2
import numpy as np
from matplotlib import pyplot as plt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

def get_pixel(img, center, x, y):
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value

def lbp_calculated_pixel(img, x, y):
    center = img[x][y]
    val_ar = []
    val_ar.append(get_pixel(img, center, x-1, y-1))
    val_ar.append(get_pixel(img, center, x-1, y))
    val_ar.append(get_pixel(img, center, x-1, y + 1))
    val_ar.append(get_pixel(img, center, x, y + 1))
    val_ar.append(get_pixel(img, center, x + 1, y + 1))
    val_ar.append(get_pixel(img, center, x + 1, y))
    val_ar.append(get_pixel(img, center, x + 1, y-1))
    val_ar.append(get_pixel(img, center, x, y-1))
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]
    return val

def calculate_normalized_lbp_histogram(img_gray):
    height, width = img_gray.shape
    lbp_histogram = np.zeros(256, dtype=int)
    
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            lbp_val = lbp_calculated_pixel(img_gray, i, j)
            lbp_histogram[lbp_val] += 1

    # Normalize the histogram
    lbp_histogram = lbp_histogram / sum(lbp_histogram)

    return lbp_histogram

def find_mode_pixel_value(img):
    img_flat = img.ravel()
    mode_value = int(np.median(img_flat))
    return mode_value

def lbp(request):
    path = 'media/lahan 4 50 cm.jpeg'
    img_bgr = cv2.imread(path, 1)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    mode_pixel = find_mode_pixel_value(img_gray)
    print(f"Nilai pixel yang paling sering muncul: {mode_pixel}")
    normalized_mode_pixel = mode_pixel / 255.0  
    print(f"Nilai yang sering muncul yang telah dinormalisasi: {normalized_mode_pixel}")    
    
    hasil_operasi_Natrium = (normalized_mode_pixel * 0.1928 + 0.021)
    print(f"hasil Nilai N (Natrium): {hasil_operasi_Natrium}")
    N = hasil_operasi_Natrium
    if N < 1:
        print("Sangat rendah")
    elif N >= 1 and N < 2:
        print("Rendah")
    elif N >= 2.001 and N < 3:
        print("Sedang")
    elif N >= 3.001 and N < 5:
        print("Tinggi")
    elif N >= 5.001:
        print("Sangat Tinggi")
    else:
        print("Ketegori Tidak Ditemukan")
    
    hasil_operasi_fosfor = (normalized_mode_pixel * -10.725) + 16.533
    print(f"hasil Nilai P (Fosfor): {hasil_operasi_fosfor}")
    P = hasil_operasi_fosfor
    if P < 10:
        print("Sangat rendah")
    elif P >= 10 and P <= 25:
        print("Rendah")
    elif P >= 26 and P <= 45:
        print("Sedang")
    elif P >= 46 and P <= 60:
        print("Tinggi")
    elif P > 60:
        print("Sangat Tinggi")
    else:
        print("Lebih dari atau sama dengan 2")
    
    hasil_operasi_Kalium = (normalized_mode_pixel * -0.1864 + 0.2471)
    print(f"hasil Nilai K (Kalium): {hasil_operasi_Kalium}")
    K = hasil_operasi_Kalium
    if K < 0.1:
        print("Sangat rendah")
    elif K >= 0.1 and K <= 0.3:
        print("Rendah")
    elif K >= 0.4 and K <= 0.5:
        print("Sedang")
    elif K >= 0.6 and K <= 1.0:
        print("Tinggi")
    elif K > 1.0:
        print("Sangat Tinggi")
    else:
        print("Lebih dari atau sama dengan 2")
    lbp_histogram = calculate_normalized_lbp_histogram(img_gray)
    print("Program LBP selesai")
lbp(None)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        image_path = os.path.join('media', 'uploaded_images', uploaded_image.name)

        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        path = image_path
        img_bgr = cv2.imread(path, 1)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        mode_pixel = find_mode_pixel_value(img_gray)
        print(f"Nilai pixel yang paling sering muncul: {mode_pixel}")
        normalized_mode_pixel = mode_pixel / 255.0  
        print(f"Nilai yang sering muncul yang telah dinormalisasi: {normalized_mode_pixel}")    
        
        hasil_operasi_Natrium = (normalized_mode_pixel * 0.1928 + 0.021)
        print(f"hasil Nilai N (Natrium): {hasil_operasi_Natrium}")
        N = hasil_operasi_Natrium
        if N < 1:
            print("Sangat rendah")
        elif N >= 1 and N < 2:
            print("Rendah")
        elif N >= 2.001 and N < 3:
            print("Sedang")
        elif N >= 3.001 and N < 5:
            print("Tinggi")
        elif N >= 5.001:
            print("Sangat Tinggi")
        else:
            print("Ketegori Tidak Ditemukan")
        
        hasil_operasi_fosfor = (normalized_mode_pixel * -10.725) + 16.533
        print(f"hasil Nilai P (Fosfor): {hasil_operasi_fosfor}")
        P = hasil_operasi_fosfor
        if P < 10:
            print("Sangat rendah")
        elif P >= 10 and P <= 25:
            print("Rendah")
        elif P >= 26 and P <= 45:
            print("Sedang")
        elif P >= 46 and P <= 60:
            print("Tinggi")
        elif P > 60:
            print("Sangat Tinggi")
        else:
            print("Lebih dari atau sama dengan 2")
        
        hasil_operasi_Kalium = (normalized_mode_pixel * -0.1864 + 0.2471)
        print(f"hasil Nilai K (Kalium): {hasil_operasi_Kalium}")
        K = hasil_operasi_Kalium
        if K < 0.1:
            print("Sangat rendah")
        elif K >= 0.1 and K <= 0.3:
            print("Rendah")
        elif K >= 0.4 and K <= 0.5:
            print("Sedang")
        elif K >= 0.6 and K <= 1.0:
            print("Tinggi")
        elif K > 1.0:
            print("Sangat Tinggi")
        else:
            print("Lebih dari atau sama dengan 2")
        lbp_histogram = calculate_normalized_lbp_histogram(img_gray)
        print("Program LBP selesai")

        return JsonResponse({'message': 'Gambar berhasil diunggah dan diproses'})
    else:
        return JsonResponse({'message': 'Permintaan tidak valid'})