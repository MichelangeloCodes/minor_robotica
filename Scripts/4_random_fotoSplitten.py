import os
import random
from shutil import copyfile

# Lijst van mappen met afbeeldingen
mappen = [
    r"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Beetroot",
    r"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Carrot",
    r"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Lettuce",
    r"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Radish",
    r"C:\Users\jerom\Downloads\Data2023\Image_DataSet\1_Foto_origineel\Mixed",
    
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Beetroot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Carrot',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Lettuce',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Radish',
    r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\3_Foto_filterToepassing\Mixed'
]

# Functie om bestanden in een map te tellen
def tel_bestanden(map_pad):
    return len([naam for naam in os.listdir(map_pad) if os.path.isfile(os.path.join(map_pad, naam))])

# Functie om afbeeldingen te verdelen in trainings-, validatie- en testsets
def verdeel_sets(map_pad):
    bestanden = os.listdir(map_pad)
    random.shuffle(bestanden)  # Randomiseer de bestandenlijst

    # Bereken het aantal bestanden
    aantal_bestanden = len(bestanden)
    aantal_test = int(0.02 * aantal_bestanden)  # 2% voor test
    aantal_validatie = int(0.1 * aantal_bestanden)  # 10% voor validatie

    test_set = bestanden[:aantal_test]
    validatie_set = bestanden[aantal_test:aantal_test + aantal_validatie]
    trainings_set = bestanden[aantal_test + aantal_validatie:]

    return trainings_set, validatie_set, test_set

# Functie om bestanden te verplaatsen naar de doelmap
def verplaats_bestanden(bestanden, doelmap, oorspronkelijke_map):
    for bestand in bestanden:
        bronpad = os.path.join(oorspronkelijke_map, bestand)
        doelpad = os.path.join(doelmap, bestand)
        copyfile(bronpad, doelpad)


totaal = 0
totaal_training = 0
totaal_validatie  = 0
totaal_test = 0

for map_pad in mappen:
    trainings_set, validatie_set, test_set = verdeel_sets(map_pad)

    # Doelmap voor trainings-, validatie- en testsets
    doelmap_train = r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\4_FotoSet_Train_Val_Test\1_train'
    doelmap_val = r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\4_FotoSet_Train_Val_Test\2_val'
    doelmap_test = r'C:\Users\jerom\Downloads\Data2023\Image_DataSet\4_FotoSet_Train_Val_Test\3_test'

    # Verplaats bestanden naar respectievelijke mappen
    verplaats_bestanden(trainings_set, doelmap_train, map_pad)
    verplaats_bestanden(validatie_set, doelmap_val, map_pad)
    verplaats_bestanden(test_set, doelmap_test, map_pad)

    aantal_items = tel_bestanden(map_pad)
    print(f"Aantal items in {map_pad}: {aantal_items}")
    print(f"Aantal items in trainingsset: {len(trainings_set)}")
    print(f"Aantal items in validatieset: {len(validatie_set)}")
    print(f"Aantal items in testset: {len(test_set)}")
    
    totaal = totaal + aantal_items
    totaal_training = totaal_training + len(trainings_set)
    totaal_validatie = totaal_validatie + len(validatie_set)
    totaal_test = totaal_test + len(test_set)
    print("------------")
    
print(f"Aantal items in totaal: {totaal}")
print(f"Totaal items in trainingsset: {totaal_training}")
print(f"Totaal items in validatieset: {totaal_validatie}")
print(f"Totaal items in testset: {totaal_test}")  
