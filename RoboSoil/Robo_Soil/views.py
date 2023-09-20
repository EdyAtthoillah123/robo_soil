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
        round_natrium = round(hasil_operasi_Natrium, 2) 
        print(f"hasil Nilai N (Natrium): {round_natrium}")
        N = hasil_operasi_Natrium
        if N < 1.0:
            Kategori_N = 1
        elif N >= 1.0 and N < 2.0:
            Kategori_N = 2
        elif N >= 2.001 and N < 3.0:
            Kategori_N = 3
        elif N >= 3.001 and N < 5.0:
            Kategori_N = 4
        elif N >= 5.001:
            Kategori_N = 5
        else:
            Kategori_N = 6
        
        hasil_operasi_fosfor = (normalized_mode_pixel * -10.725) + 16.533
        round_fosfor = round(hasil_operasi_fosfor, 2) 
        print(f"hasil Nilai P (Fosfor): {round_fosfor}")
        P = hasil_operasi_fosfor
        if P < 10.0:
            Kategori_P = 1
        elif P > 10.001 and P <= 25.99:
            Kategori_P = 2
        elif P >= 26.0 and P <= 45.99:
            Kategori_P = 3
        elif P >= 46.0 and P <= 60:
            Kategori_P = 4
        elif P > 60.001:
            Kategori_P = 5
        else:
            Kategori_P = 6
        
        hasil_operasi_Kalium = (normalized_mode_pixel * -0.1864 + 0.2471)
        round_kalium = round(hasil_operasi_Kalium, 2) 
        print(f"hasil Nilai K (Kalium): {round_kalium}")
        K = hasil_operasi_Kalium
        if K < 0.1:
            Kategori_K = 1
        elif K >= 0.1 and K <= 0.3999999999:
            Kategori_K = 2
        elif K >= 0.4 and K <= 0.599999999:
            Kategori_K = 3
        elif K >= 0.6 and K <= 1.0:
            Kategori_K = 4
        elif K > 1.0001:
            Kategori_K = 5
        else:
            Kategori_K = 6
        
        # Hasil perhitungan NPK
        N = Kategori_N
        P = Kategori_P
        K = Kategori_K

        # Nilai N, P, dan K yang ingin Anda cocokkan
        target_N_sawah = 3
        target_P_sawah = 4
        target_K_sawah = 3
        
        # lahan sawah irigasi
        if N >= target_N_sawah and P >= target_P_sawah and K < target_K_sawah:
            SaranTanaman1 = "Kategori S1 Sangat Sesuai Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
            print(SaranTanaman1)
        elif N == 2 and P == 3 and K == 2:
                SaranTanaman1 = "Kategori S2 Cukup Sesuai (Sedang) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk"
                print(SaranTanaman1)
        elif N == 1 and P >= 2 or P == 1 and K == 1:
                SaranTanaman1 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman1)
        elif N >= 1 or N == 1 and P == 1 and K == 1:
                SaranTanaman1 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman1)
        elif N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman1 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman1)
        elif N == 1 and P >= 2 or P == 1 and K >= 1 or K == 1:
                SaranTanaman1 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman1)
        elif N >= 1 or N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman1 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman1)
        else:
            SaranTanaman1 = "Tidak Cocok Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih Karena"
            print(SaranTanaman1)
            
        if N < target_N_sawah :
            SaranTanaman1 = "Perlu Perbaikan N Untuk ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
            print(SaranTanaman1)
            if N >= target_N_sawah :
                SaranTanaman1 = "Sangat Cocok Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
                print(SaranTanaman1)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
            
        if P < target_P_sawah :
            SaranTanaman1 = "Perlu Perbaikan P Untuk ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
            print(SaranTanaman1)
            if P >= target_P_sawah :
                SaranTanaman1 = "Sangat Cocok Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
                print(SaranTanaman1)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        if K < target_K_sawah :
            SaranTanaman1 = "Perlu Perbaikan K Untuk ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
            print(SaranTanaman1)
            if K >= target_K_sawah :
                SaranTanaman1 = "Sangat Cocok Untuk Ditanami Sawah Irigasi, Wortel, Bawang Merah, Bawang Putih"
                print(SaranTanaman1)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
    
        # Nilai N, P, dan K yang ingin Anda cocokkan
        target_N_jagung = 3
        target_P_jagung = 4
        target_K_jagung = 4
        
        # lahan sawah irigasi
        if N >= target_N_jagung and P >= target_P_jagung and K < target_K_jagung:
            SaranTanaman2 = "Kategori S1 Sangat Sesuai Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
            print(SaranTanaman2)
        elif N == 2 and P == 3 and K == 3:
                SaranTanaman2 = "Kategori S2 Cukup Sesuai (Sedang) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk"
                print(SaranTanaman2)
        elif N == 1 and P >= 2 or P == 1 and K == 2 :
                SaranTanaman2 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman2)
        elif N >= 1 or N == 1 and P == 1 and K == 1:
                SaranTanaman2 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman2)
        elif N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman2 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman2)
        elif N == 1 and P >= 2 or P == 1 and K >= 1 or K == 1:
                SaranTanaman2 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman2)
        elif N >= 1 or N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman2 = "Kategori S3 Sesuai Marginal (Rendah) Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman2)
        else:
            SaranTanaman2 = "Tidak Cocok Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah Karena"
            print(SaranTanaman2)
            
        if N < target_N_jagung :
            SaranTanaman2 = "Perlu Perbaikan N Untuk ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
            print(SaranTanaman2)
            if N >= target_N_jagung :
                SaranTanaman2 = "Sangat Cocok Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
                print(SaranTanaman2)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
            
        if P < target_P_jagung :
            SaranTanaman2 = "Perlu Perbaikan P Untuk ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
            print(SaranTanaman2)
            if P >= target_P_jagung :
                SaranTanaman2 = "Sangat Cocok Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
                print(SaranTanaman2)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        if K < target_K_jagung :
            SaranTanaman2 = "Perlu Perbaikan K Untuk ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
            print(SaranTanaman2)
            if K >= target_K_jagung :
                SaranTanaman2 = "Sangat Cocok Untuk Ditanami Jagung, Sorgum, Gandum, Kedelai, Kacang Tanah"
                print(SaranTanaman2)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        target_N_Ubi = 3
        target_P_Ubi = 3
        target_K_Ubi = 3
        
        # lahan sawah irigasi
        if N >= target_N_Ubi and P >= target_P_Ubi and K < target_K_Ubi:
            SaranTanaman3 = "Kategori S1 Sangat Sesuai Untuk ditanami Ubi Kayu, Ubi Jalar"
            print(SaranTanaman3)
        elif N == 2 and P == 2 and K == 2:
                SaranTanaman3 = "Kategori S2 Cukup Sesuai (Sedang) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk"
                print(SaranTanaman3)
        elif N == 1 and P >= 1 or P == 1 and K == 1 :
                SaranTanaman3 = "Kategori S3 Sesuai Marginal (Rendah) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman3)
        elif N >= 1 or N == 1 and P == 1 and K == 1:
                SaranTanaman3 = "Kategori S3 Sesuai Marginal (Rendah) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman3)
        elif N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman3 = "Kategori S3 Sesuai Marginal (Rendah) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman3)
        elif N == 1 and P >= 1 or P == 1 and K >= 1 or K == 1:
                SaranTanaman3 = "Kategori S3 Sesuai Marginal (Rendah) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman3)
        elif N >= 1 or N == 1 and P == 1 and K >= 1 or K == 1:
                SaranTanaman3 = "Kategori S3 Sesuai Marginal (Rendah) Untuk ditanami Ubi Kayu, Ubi Jalar Namun memerlukan tambahan pupuk yang lebih banyak"
                print(SaranTanaman3)
        else:
            SaranTanaman3 = "Tidak Cocok Untuk ditanami Ubi Kayu, Ubi Jalar Karena"
            print(SaranTanaman3)
            
        if N < target_N_Ubi :
            SaranTanaman3 = "Perlu Perbaikan N Untuk ditanami Ubi Kayu, Ubi Jalar"
            print(SaranTanaman3)
            if N >= target_N_Ubi :
                SaranTanaman3 = "Sangat Cocok Untuk ditanami Ubi Kayu, Ubi Jalar"
                print(SaranTanaman3)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
            
        if P < target_P_Ubi :
            SaranTanaman3 = "Perlu Perbaikan P Untuk ditanami Ubi Kayu, Ubi Jalar"
            print(SaranTanaman3)
            if P >= target_P_Ubi :
                SaranTanaman3 = "Sangat Cocok Untuk ditanami Ubi Kayu, Ubi Jalar"
                print(SaranTanaman3)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        if K < target_K_Ubi :
            SaranTanaman3 = "Perlu Perbaikan K Untuk ditanami Ubi Kayu, Ubi Jalar"
            print(SaranTanaman3)
            if K >= target_K_Ubi :
                SaranTanaman3 = "Sangat Cocok Untuk ditanami Ubi Kayu, Ubi Jalar"
                print(SaranTanaman3)
        else:
            print("Hasil tidak cocok dengan data yang diberikan.")
        
        print(SaranTanaman1,", dan ", SaranTanaman2,", dan ", SaranTanaman3)
        lbp_histogram = calculate_normalized_lbp_histogram(img_gray)
        print("Program LBP selesai")

        return JsonResponse({'message': 'Gambar berhasil diunggah dan diproses'})
    else:
        return JsonResponse({'message': 'Permintaan tidak valid'})