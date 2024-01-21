import cv2
import numpy as np
import os
import random

show_images = False
save_images = True


input_mappen = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Beetroot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Carrot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Lettuce_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Radish_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\mixed_transformaties'
]

# MAP OUTPUT transformaties
output_mappen_transformaties = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Beetroot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Carrot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Lettuce',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Radish',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Mixed'
]

def main():
    for i, map_pad in enumerate(input_mappen):
        uitbreiding_map_pad = output_mappen_transformaties[i]

        if os.path.exists(map_pad):
            if not os.path.exists(uitbreiding_map_pad):
                os.makedirs(uitbreiding_map_pad)
            
            for bestandsnaam in os.listdir(map_pad):
                if bestandsnaam.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(map_pad, bestandsnaam)
                    image = cv2.imread(image_path)
                
                        
                    #image = cv2.imread(image_path)                      # Open de afbeelding
                    image2 = foto2_blur_or_sharpened(image)             # keuze blur / sharpened
                    
                    file_name = os.path.basename(image_path)            #bestand naam
                    file_name_without_extension = os.path.splitext(os.path.basename(image_path))[0] #extension van bestand eraf halen
                    
                    enkele_filter_operatie(image, filter_type = 0)      #functie om indivudele filters te testen
                    
                    foto1_bewerkt, factoren1 = data_augmentatie(image)
                    foto2_bewerkt, factoren2 = data_augmentatie(image2)
                    
                    factors_str1 = '_'.join([f"{factor}{value}" for factor, value in factoren1])
                    factors_str2 = '_'.join([f"{factor}{value}" for factor, value in factoren2])

                    # Controleer of de afbeelding succesvol is geladen
                    if image is not None:
                        if (show_images == True):
                            #cv2.imshow(f'{file_name} - Original', image)
                            cv2.imshow(f'{file_name_without_extension}_{factors_str1}', foto1_bewerkt)
                            cv2.imshow(f'{file_name_without_extension}_{factors_str2}', foto2_bewerkt)

                            key = cv2.waitKey(0)
                            if key == ord('q'):
                                break

                            cv2.destroyAllWindows()
                            
                        if (save_images == True):
                            #cv2.imwrite(f'{file_name_without_extension}_{factors_str1}.jpg', foto1_bewerkt)
                            #cv2.imwrite(f'{file_name_without_extension}_{factors_str2}.jpg', foto2_bewerkt)
                            output_map_pad = output_mappen_transformaties[i]  # Krijg het juiste pad op basis van de index i
                            output_file_path1 = os.path.join(output_map_pad, f'{file_name_without_extension}_{factors_str1}.jpg')
                            output_file_path2 = os.path.join(output_map_pad, f'{file_name_without_extension}_{factors_str2}.jpg')

                            random_foto_kiezen = random.randint(0,2)
                            if random_foto_kiezen == 2:
                                cv2.imwrite(output_file_path2, foto2_bewerkt)
                            else:
                                cv2.imwrite(output_file_path1, foto1_bewerkt)
                                

                            
                            
                        
                    else:
                        print("Fout bij het laden van de afbeelding. Controleer het pad en het bestandsformaat.")


def foto2_blur_or_sharpened(image):
    random_factor = random.randint(0,1)
    if (random_factor == 0):
        image_type = filter_blur_image(image)
    else:
        image_type = filter_sharpen_image(image)
    return image_type
        
def filter_blur_image(image_original):
    blurred = cv2.GaussianBlur(image_original, (9, 9), 0)
    return blurred

def filter_sharpen_image(image_original):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(image_original, -1, kernel)
    return sharpened
    pass



def enkele_filter_operatie(image, filter_type):
    try:
        if filter_type == 1:
            image_blurred = filter_blur_image(image)
            cv2.imshow('Image_Blur', image_blurred)
        
        elif filter_type == 2:
            image_sharpened = filter_sharpen_image(image)
            cv2.imshow('Image_Sharpened', image_sharpened)
        
        elif filter_type == 3:
            image_adjusted_saturation = filter_saturation(image)  
            cv2.imshow('Image_Adjusted_Saturation', image_adjusted_saturation)
        
        elif filter_type == 4:
            image_adjusted_brightness = filter_brightness(image)  
            cv2.imshow('Image_Adjusted_Brightness', image_adjusted_brightness)
        
        elif filter_type == 5:
            image_adjusted_exposure = filter_exposure(image)  
            cv2.imshow('Image_Adjusted_Exposure', image_adjusted_exposure)
        
        elif filter_type == 6:
            image_noise_added_saltPeper = filter_noise_salt_and_pepper(image)
            cv2.imshow('image_noise_salt', image_noise_added_saltPeper)
        
        elif filter_type == 7:
            image_noise_added_gaussian = filter_noise_gaussian(image)
            cv2.imshow('image_noise_gaus', image_noise_added_gaussian)
        
    except:
        print("An exception occurred")
    
def filter_saturation(image, fact_sat):
    saturation_factor = fact_sat
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype=np.float64)
    hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
    hsv[:, :, 1][hsv[:, :, 1] > 255] = 255
    hsv = np.array(hsv, dtype=np.uint8)
    adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return adjusted_image

def filter_brightness(image, fact_brght):
    brightness_factor = fact_brght
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
    return adjusted_image

def filter_exposure(image, fact_exp):
    gamma = fact_exp
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted_image = cv2.LUT(image, table)
    return adjusted_image

def filter_noise_salt_and_pepper(image, fact_Noise):
    noisy_image = image.copy() # Maak een kopie van de originele afbeelding anders werkte het niet

    amount = fact_Noise
    height, width = noisy_image.shape[:2]
    noise_mask = np.random.choice([0, 1, 2], size=(height, width), p=[1 - amount, amount / 2., amount / 2.])

    salt = noise_mask == 1
    pepper = noise_mask == 2

    noisy_image[salt] = 255  
    noisy_image[pepper] = 0   

    return noisy_image

def filter_noise_gaussian(image, fact_Noise):
    row, col, ch = image.shape
    mean = 0
    var = fact_Noise
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = np.clip(image + gauss * 255, 0, 255).astype(np.uint8)
    return noisy
    
def data_augmentatie(image):   
    factoren = []
    
    fact_sat = randomGetal(-30, 35, 1)
    image_bewerking = filter_saturation(image, fact_sat)
    print("fact_sat:\t", fact_sat)
    factoren.append(("Sat", fact_sat))
    
    fact_brght = randomGetal(-25, 30, 1)
    image_bewerking = filter_brightness(image_bewerking, fact_brght)
    print("fact_brght:\t", fact_brght)
    factoren.append(("Brght", fact_brght))
    
    i = random.randint(1,3)
    if(i == 3):             # 1 op 3 met autoexposure
        fact_exp = randomGetal(-5, 5, 1)
        image_bewerking = filter_exposure(image_bewerking, fact_exp)
        print("fact_exp:\t", fact_exp)
        factoren.append(("Exp", fact_exp))
    else:
        fact_exp = 0
        print("fact_exp:\t", fact_exp, "\tNO EXPOSURE")
        factoren.append(("Exp", fact_exp))
    
    i = random.randint(1,6)
    if(i == 5 or i == 6):   # 2 op 6 met noise filter 
        fact_Noise = randomGetal(0, 6, 0)
        
        if(i == 5):
            image_bewerking = filter_noise_salt_and_pepper(image_bewerking, fact_Noise)
            print("Noise salt:\t", fact_Noise)
            factoren.append(("NoiseSP", fact_Noise))
        else:
            image_bewerking = filter_noise_gaussian(image_bewerking, fact_Noise)
            print("Noise gaussian:\t", fact_Noise)
            factoren.append(("NoiseG", fact_Noise))
    else:
        fact_Noise = 0
        print("Noise:\t\t", fact_Noise, "\tNO NOISE")
        factoren.append(("Noise", fact_Noise))
        
    return image_bewerking, factoren
    
def randomGetal(min, max, optellen):
    num = random.randrange(min, max)
    num = (num / 100) + optellen
    return num


if __name__ == "__main__":
    main()