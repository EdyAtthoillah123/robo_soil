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
            Kategori_N = 1
            print(Kategori_N)
        elif N >= 1 and N < 2:
            Kategori_N = 2
            print(Kategori_N)
        elif N >= 2.001 and N < 3:
            Kategori_N = 3
            print(Kategori_N)
        elif N >= 3.001 and N < 5:
            Kategori_N = 4
            print(Kategori_N)
        elif N >= 5.001:
            Kategori_N = 5
            print(Kategori_N)
        else:
            Kategori_N = 6
            print(Kategori_N)
        
        hasil_operasi_fosfor = (normalized_mode_pixel * -10.725) + 16.533
        print(f"hasil Nilai P (Fosfor): {hasil_operasi_fosfor}")
        P = hasil_operasi_fosfor
        if P < 10:
            Kategori_P = 1
            print(Kategori_P)
        elif P >= 10 and P <= 25:
            Kategori_P = 2
            print(Kategori_P)
        elif P >= 26 and P <= 45:
            Kategori_P = 3
            print(Kategori_P)
        elif P >= 46 and P <= 60:
            Kategori_P = 4
            print(Kategori_P)
        elif P > 60:
            Kategori_P = 5
            print(Kategori_P)
        else:
            Kategori_P = 6
            print(Kategori_P)
        
        hasil_operasi_Kalium = (normalized_mode_pixel * -0.1864 + 0.2471)
        print(f"hasil Nilai K (Kalium): {hasil_operasi_Kalium}")
        K = hasil_operasi_Kalium
        if K < 0.1:
            Kategori_K = 1
            print(Kategori_K)
        elif K >= 0.1 and K <= 0.3:
            Kategori_K = 2
            print(Kategori_K)
        elif K >= 0.4 and K <= 0.5:
            Kategori_K = 3
            print(Kategori_K)
        elif K >= 0.6 and K <= 1.0:
            Kategori_K = 4
            print(Kategori_K)
        elif K > 1.0:
            Kategori_K = 5
            print(Kategori_K)
        else:
            Kategori_K = 6
            print(Kategori_K)
        
        # Hasil perhitungan NPK
        N = hasil_operasi_Natrium
        P = hasil_operasi_fosfor
        K = hasil_operasi_Kalium

        # Nilai N, P, dan K yang ingin Anda cocokkan
        target_N = 1
        target_P = 2
        target_K = 2

        # Mencocokkan dengan kategori yang dihitung
        if N <= target_N :
            print("Perlu Perbaikan Nilai N")
            if N == target_N :
                print("Perlu Perbaikan N")
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
            
        if P <= target_P :
            print("Perlu Perbaikan Nilai P")
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        if K <= target_K :
            print("Perlu Perbaikan Nilai K")
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")

        
        # Rekomendasi_N = Kategori_N
        # if Kategori_N <= 1:
        #     Rekomendasi_N = "S3"
        #     print(Rekomendasi_N)
        # else:
        #     Kategori_K = 6
        #     print(Kategori_K)  
        
        # SaranTanaman = RekomendasiTanaman
        lbp_histogram = calculate_normalized_lbp_histogram(img_gray)
        print("Program LBP selesai")

        return JsonResponse({'message': 'Gambar berhasil diunggah dan diproses'})
    else:
        return JsonResponse({'message': 'Permintaan tidak valid'})