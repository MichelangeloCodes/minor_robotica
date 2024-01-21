import cv2
import os

def main():
    # Open de videocamera
    cap = cv2.VideoCapture(0)  # 0 geeft de standaardcamera aan. Als je meerdere camera's hebt, kun je 1, 2, enz. proberen.

    # Controleer of de camera correct is geopend
    if not cap.isOpened():
        print("Kon de camera niet openen. Controleer of deze is aangesloten.")
        return

    # Maak de map voor opgeslagen foto's als deze niet bestaat
    save_folder = r'C:\Users\jerom\OneDrive\Documenten\Avans_minor\Project_AgroGantry\Software_Zaken\Image_DataSet\1_FilterFoto_Originele_2022'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    while True:
        # Lees het frame van de camera
        ret, frame = cap.read()

        # Toon het videoframe
        cv2.imshow('Camera', frame)

        # Wacht op de Enter-toets
        key = cv2.waitKey(1)
        if key == 13:  # ASCII-code voor Enter-toets
            # Genereer de bestandsnaam voor de foto
            photo_name = os.path.join(save_folder, 'photo_{}.png'.format(len(os.listdir(save_folder))))

            # Sla de foto op
            cv2.imwrite(photo_name, frame)
            print(f"Foto opgeslagen: {photo_name}")

        # Stop de loop als de Esc-toets wordt ingedrukt
        elif key == 27:
            break

    # Sluit de camera en vensters
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()