import numpy as np
import os
import cv2


class Rotation():
    def __init__(self,file,save_file,direction):
        self.file = file
        self.save_file = save_file
        self.direction = direction

        self.rotate()

    def rotate(self):
        direction = int(self.direction)

        if direction == 90:
            self.rotate_90()
        elif direction == 180:
            self.rotate_180()
        elif direction == 270:
            self.rotate_270()
        else:
            print("SADECE DİK AÇI DÖNÜŞÜMLERİ!!!")

    def rotate_90(self):
        os.chdir(self.file)

        for img in os.listdir():
            if img.endswith(".jpg") or img.endswith(".png"):
                image = cv2.imread(img)
                rotated_shape = [image.shape[1], image.shape[0], image.shape[2]]
                rotated = np.zeros(rotated_shape, dtype="uint8")

                for i in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        rotated[j][i] = image[i][j]

                cv2.imwrite(self.save_file + "\\" + img,rotated)
                print(img + " was rotated at " + self.direction + " degree to the file " + self.save_file)

            else:
                continue

    def rotate_180(self):
        os.chdir(self.file)

        for img in os.listdir():
            if img.endswith(".jpg") or img.endswith(".png"):
                image = cv2.imread(img)
                rotated_shape = image.shape
                rotated = np.zeros(rotated_shape, dtype="uint8")

                for i in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        rotated[(int(image.shape[0]) -1) -i][j] = image[i][j]

                cv2.imwrite(self.save_file + "\\" + img, rotated)
                print(img + " was rotated at " + self.direction + " degree to the file " + self.save_file)

            else:
                continue

    def rotate_270(self):
        os.chdir(self.file)

        for img in os.listdir():
            if img.endswith(".jpg") or img.endswith(".png"):
                image = cv2.imread(img)
                rotated_shape = [image.shape[1], image.shape[0], image.shape[2]]
                rotated = np.zeros(rotated_shape, dtype="uint8")

                for i in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        rotated[(int(image.shape[1]) - 1) - j][i] = image[i][j]

                cv2.imwrite(self.save_file + "\\" + img, rotated)
                print(img + " was rotated at " + self.direction + " degree to the file " + self.save_file)

            else:
                continue



images = "D:\Projelerim"
new_images = "D:\Projelerim"

try:
    rotation = Rotation(images,new_images,"270")
except:
    print("\n\nAll images were succesfully rotated!!!")


