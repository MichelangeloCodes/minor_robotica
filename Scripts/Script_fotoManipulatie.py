import cv2
import os
import numpy as np

show_images = True
save_images = False

# ========================================================================
'''
DEZE CODE WA BEDOELD OM DE TRANSFORMATIES EN FILTERS IN 1 CODE TE VERWERKEN.
DIT KOST WAT TIJD EN KON ANDERS BETER GEBRUIKT WORDEN
DUS NU MOETEN BEIDE SCRIPT LOS UITGEVOERD WORDEN OM ALLES TE VERWERKEN    
'''
# ========================================================================

# MAP INLEZEN
input_mappen = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Beetroot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Carrot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Lettuce',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Radish',
    r'"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Mixed"'
]

# MAP OUTPUT transformaties
output_mappen_transformaties = [
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Beetroot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Carrot_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Lettuce_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\Radish_transformaties',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\2_Foto_matrixTransformaties\mixed_transformaties'
]


def main():
    fotomap_verwerken()


def fotomap_verwerken():
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
                        (
                            verticaal_geflipte_afbeelding,
                            horizontaal_geflipte_afbeelding,
                            gedraaide_afbeelding,
                            gedraaide_tegen_afbeelding,
                            gesheerde_verticaal_afbeelding,
                            gesheerde_horizontaal_afbeelding,
                        ) = foto_transformeren(
                            originele_afbeelding,
                            uitbreiding_map_pad,
                            bestandsnaam
                        )
                        show_transformeerde_images(
                            originele_afbeelding,
                            verticaal_geflipte_afbeelding,
                            horizontaal_geflipte_afbeelding,
                            gedraaide_afbeelding,
                            gedraaide_tegen_afbeelding,
                            gesheerde_verticaal_afbeelding,
                            gesheerde_horizontaal_afbeelding,
                            bestandsnaam
                        )
                        save_transformeerde_images(
                            verticaal_geflipte_afbeelding,
                            horizontaal_geflipte_afbeelding,
                            gedraaide_afbeelding,
                            gedraaide_tegen_afbeelding,
                            gesheerde_verticaal_afbeelding,
                            gesheerde_horizontaal_afbeelding,
                            uitbreiding_map_pad,
                            bestandsnaam
                        )
        else:
            print(f"De map {map_pad} bestaat niet.")

def foto_transformeren(originele_afbeelding, uitbreiding_map_pad, bestandsnaam):
    verticaal_geflipte_afbeelding = cv2.flip(originele_afbeelding, 1)
    horizontaal_geflipte_afbeelding = cv2.flip(originele_afbeelding, 0)
    gedraaide_afbeelding = cv2.rotate(originele_afbeelding, cv2.ROTATE_90_CLOCKWISE)
    gedraaide_tegen_afbeelding = cv2.rotate(originele_afbeelding, cv2.ROTATE_90_COUNTERCLOCKWISE)
    (
        gesheerde_verticaal_afbeelding,
        gesheerde_horizontaal_afbeelding,
    ) = shear_transformatie_uitvoeren(originele_afbeelding)
    return (
        verticaal_geflipte_afbeelding,
        horizontaal_geflipte_afbeelding,
        gedraaide_afbeelding,
        gedraaide_tegen_afbeelding,
        gesheerde_verticaal_afbeelding,
        gesheerde_horizontaal_afbeelding,
    )

def shear_transformatie_uitvoeren(originele_afbeelding):
    verticale_shear_factor = 0.1
    verticale_shear_matrix = np.array([
        [1, verticale_shear_factor, 0],
        [0, 1, 0]
    ], dtype=np.float32)

    horizontale_shear_factor = 0.25
    horizontale_shear_matrix = np.array([
        [1, 0, 0],
        [horizontale_shear_factor, 1, 0]
    ], dtype=np.float32)

    hoogte, breedte = originele_afbeelding.shape[:2]
    gesheerde_verticaal_afbeelding = cv2.warpAffine(originele_afbeelding, verticale_shear_matrix, (breedte, hoogte))
    gesheerde_horizontaal_afbeelding = cv2.warpAffine(originele_afbeelding, horizontale_shear_matrix, (breedte, hoogte))

    return (
        gesheerde_verticaal_afbeelding,
        gesheerde_horizontaal_afbeelding,
    )

def show_transformeerde_images(
    originele_afbeelding,
    verticaal_geflipte_afbeelding,
    horizontaal_geflipte_afbeelding,
    gedraaide_afbeelding,
    gedraaide_tegen_afbeelding,
    gesheerde_verticaal_afbeelding,
    gesheerde_horizontaal_afbeelding,
    bestandsnaam
):
    
    if show_images:
        images = [
            originele_afbeelding,
            verticaal_geflipte_afbeelding,
            horizontaal_geflipte_afbeelding,
            gedraaide_afbeelding,
            gedraaide_tegen_afbeelding,
            gesheerde_verticaal_afbeelding,
            gesheerde_horizontaal_afbeelding
        ]
        titles = [
            f'{bestandsnaam}_Origineel',
            f'{bestandsnaam}_FLIP-VER',
            f'{bestandsnaam}_FLIP-HOR',
            f'{bestandsnaam}_Gedraaid',
            f'{bestandsnaam}_Gedraaid_tegen',
            f'{bestandsnaam}_SHEAR-VER',
            f'{bestandsnaam}_SHEAR-HOR'
        ]
        index = 0
        while True:
            cv2.imshow(titles[index], images[index])
            key = cv2.waitKey(0)
            if key == ord('q'):
                cv2.destroyAllWindows()
                raise SystemExit("Code gestopt door gebruiker.")
            elif key == ord('x'):
                cv2.destroyWindow(titles[index])
                index = (index + 1) % len(images)
            elif key == ord('z'):
                cv2.destroyWindow(titles[index])
                index = (index - 1) % len(images)

def save_transformeerde_images(
    verticaal_geflipte_afbeelding,
    horizontaal_geflipte_afbeelding,
    gedraaide_afbeelding,
    gedraaide_tegen_afbeelding,
    gesheerde_verticaal_afbeelding,
    gesheerde_horizontaal_afbeelding,
    uitbreiding_map_pad,
    bestandsnaam
):
    if save_images:
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_FLIP-VER.jpg'), verticaal_geflipte_afbeelding)
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_FLIP-HOR.jpg'), horizontaal_geflipte_afbeelding)
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_Gedraaid.jpg'), gedraaide_afbeelding)
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_Gedraaid_tegen.jpg'), gedraaide_tegen_afbeelding)
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_SHEAR-VER.jpg'), gesheerde_verticaal_afbeelding)
        cv2.imwrite(os.path.join(uitbreiding_map_pad, f'{bestandsnaam}_SHEAR-HOR.jpg'), gesheerde_horizontaal_afbeelding)


if __name__ == "__main__":
    main()
