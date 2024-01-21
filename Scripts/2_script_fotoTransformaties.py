import cv2
import os
import numpy as np

show_images = False
save_images = True

# MAP INLEZEN
input_mappen = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Beetroot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Carrot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Lettuce',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Radish',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Mixed'
]

# MAP OUTPUT transformaties
output_mappen_transformaties = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Beetroot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Carrot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Lettuce_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Radish_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Mixed_transformaties'
]

for i, map_pad in enumerate(input_mappen):
    uitbreiding_map_pad = output_mappen_transformaties[i]

    if os.path.exists(map_pad):
        if not os.path.exists(uitbreiding_map_pad):
            os.makedirs(uitbreiding_map_pad)

        for bestandsnaam in os.listdir(map_pad):
            if bestandsnaam.endswith(('.jpg', '.jpeg', '.png')):
                afbeelding_pad = os.path.join(map_pad, bestandsnaam)
                originele_afbeelding = cv2.imread(afbeelding_pad)

                if originele_afbeelding is not None:
                    verticaal_geflipte_afbeelding = cv2.flip(originele_afbeelding, 1)
                    horizontaal_geflipte_afbeelding = cv2.flip(originele_afbeelding, 0)
                    gedraaide_afbeelding = cv2.rotate(originele_afbeelding, cv2.ROTATE_90_CLOCKWISE)
                    gedraaide_tegen_afbeelding = cv2.rotate(originele_afbeelding, cv2.ROTATE_90_COUNTERCLOCKWISE)

                    # SHEAR VERTICAAL
                    verticale_shear_factor = 0.1
                    verticale_shear_matrix = np.array([
                        [1, verticale_shear_factor, 0],
                        [0, 1, 0]
                    ], dtype=np.float32)
                    

                    # SHEAR HORIZONTAAL
                    horizontale_shear_factor = 0.15
                    horizontale_shear_matrix = np.array([
                        [1, 0, 0],
                        [horizontale_shear_factor, 1, 0]
                    ], dtype=np.float32)

                    # Voer shear-transformaties uit
                    hoogte, breedte = originele_afbeelding.shape[:2]
                    gesheerde_verticaal_afbeelding = cv2.warpAffine(originele_afbeelding, verticale_shear_matrix, (breedte, hoogte))
                    gesheerde_horizontaal_afbeelding = cv2.warpAffine(originele_afbeelding, horizontale_shear_matrix, (breedte, hoogte))

                    if (show_images == True):
                        naam_zonder_extensie, extensie = os.path.splitext(bestandsnaam)
                        
                        cv2.imshow(f'{naam_zonder_extensie}_Origineel', originele_afbeelding)
                        cv2.imshow(f'{naam_zonder_extensie}_FLIP-VER', verticaal_geflipte_afbeelding)
                        #cv2.imshow(f'{naam_zonder_extensie}_FLIP-HOR', horizontaal_geflipte_afbeelding)
                        cv2.imshow(f'{naam_zonder_extensie}_Gedraaid', gedraaide_afbeelding)
                        cv2.imshow(f'{naam_zonder_extensie}_Gedraaid_tegen', gedraaide_tegen_afbeelding)
                        #cv2.imshow(f'{naam_zonder_extensie}_SHEAR-VER', gesheerde_verticaal_afbeelding)
                        cv2.imshow(f'{naam_zonder_extensie}_SHEAR-HOR', gesheerde_horizontaal_afbeelding)

                        key = cv2.waitKey(0)
                        if key == ord('q'):
                            break

                        cv2.destroyAllWindows()

                    if (save_images == True):
                        naam_zonder_extensie, extensie = os.path.splitext(bestandsnaam)

                        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_FLIP-VER.jpg'), verticaal_geflipte_afbeelding)
                        #cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_FLIP-HOR.jpg'), horizontaal_geflipte_afbeelding)
                        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_Gedraaid.jpg'), gedraaide_afbeelding)
                        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_Gedraaid_tegen.jpg'), gedraaide_tegen_afbeelding)
                        #cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_SHEAR-VER.jpg'), gesheerde_verticaal_afbeelding)
                        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{naam_zonder_extensie}_SHEAR-HOR.jpg'), gesheerde_horizontaal_afbeelding)

    else:
        print(f"De map {map_pad} bestaat niet.")
