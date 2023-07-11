import os, cv2, face_recognition
import pandas as pd
from face_recognition.face_detection_cli import image_files_in_folder

# file_dir = 'malpractice_tracking/compare/images/'
file_dir = 'C:/Users/ADEMOLA/Documents/Projects/exam-malpractice-record-tracking/malpractice_tracking/compare/images/'
# C:\Users\ADEMOLA\Documents\Projects\exam-malpractice-record-tracking\malpractice_tracking\compare\images
encoding_for_file = []

for i in os.listdir(file_dir):
    image = file_dir + i
    image = face_recognition.load_image_file(image)
    image_encoding = face_recognition.face_encodings(image)
    encoding_for_file.append(image_encoding[0])

encoding_csv = pd.DataFrame(encoding_for_file)
encoding_csv.to_csv("images_encoding.csv")






# class CompareImage:
#     def find_face_encodings(image_path):
#         # reading image
#         image = cv2.imread(image_path)
#         # get face encodings from the image
#         face_enc = face_recognition.face_encodings(image)
#         # return face encodings
#         if len(face_enc) > 0:
#             return face_enc[0]
#         else:
#             print("can't get face from the provided image")
#             return None
        
#     def compare(self, image_1, image_2):
#         # getting face encodings for first image
#         # image1 = self.find_face_encodings(image_1) "C:\\Users\\ADEMOLA\\Pictures\\passport1.jpg"
#         # # getting face encodings for second image
#         # image2  = self.find_face_encodings(image_2)
#         image_1 = self.find_face_encodings(image_1)
#         # getting face encodings for second image
#         image_2  = self.find_face_encodings(image_2)

#         if image_1 is not None and image_2 is not None:
#             # checking both images are same
#             is_same = face_recognition.compare_faces([image_1], image_2)[0]
#             print(f"Is Same: {is_same}")
#             if is_same:
#                 # finding the distance level between images
#                 distance = face_recognition.face_distance([image_1], image_2)
#                 distance = round(distance[0] * 100)
                
#                 # calcuating accuracy level between images
#                 accuracy = 100 - round(distance)
#                 print("The images are same")
#                 print(f"Accuracy Level: {accuracy}%")
#             else:
#                 print("The images are not same")