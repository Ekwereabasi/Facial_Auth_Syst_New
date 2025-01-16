# import os
# from django.core.exceptions import ValidationError
# from google.cloud import vision_v1
# from django.conf import settings
# from .models import CustomUser

# def authenticate_user_with_facial_recognition(uploaded_image):
#     client = vision_v1.ImageAnnotatorClient()

#     temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
#     with open(temp_image_path, 'wb') as temp_image_file:
#         for chunk in uploaded_image.chunks():
#             temp_image_file.write(chunk)
    
#     with open(temp_image_path, 'rb') as image_file:
#         content = image_file.read()

#     uploaded_image = vision_v1.Image(content=content)
#     response_uploaded = client.face_detection(image=uploaded_image)
    
#     if not response_uploaded.face_annotations:
#         os.remove(temp_image_path)
#         raise ValidationError("No face detected in the uploaded image.")

#     for user in CustomUser.objects.all():
#         profile_picture_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
        
#         if not os.path.isfile(profile_picture_path):
#             continue  
        
#         with open(profile_picture_path, 'rb') as profile_image_file:
#             profile_content = profile_image_file.read()

#         profile_image = vision_v1.Image(content=profile_content)
#         response_profile = client.face_detection(image=profile_image)
        
#         if not response_profile.face_annotations:
#             continue
        
#         uploaded_face = response_uploaded.face_annotations[0]
#         profile_face = response_profile.face_annotations[0]

#         def compare_faces(uploaded_face, profile_face):
            
#             uploaded_bounds = uploaded_face.bounding_poly
#             profile_bounds = profile_face.bounding_poly

            
#             def bbox_overlap(bounds1, bounds2):
             
#                 return True  

#             if bbox_overlap(uploaded_bounds, profile_bounds):
#                 return True

#             return False

#         if compare_faces(uploaded_face, profile_face):
#             os.remove(temp_image_path)
#             return user

#     os.remove(temp_image_path)
#     raise ValidationError("Facial recognition failed. The uploaded image does not match any profile picture.")

import face_recognition
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from .models import CustomUser
from PIL import Image
from io import BytesIO

def preprocess_image(image):
    """Handles in-memory images and processes them."""
    img = Image.open(image)
    img = img.resize((500, 500))  # Resize to standard dimensions
    temp_image = BytesIO()
    img.save(temp_image, format='JPEG')  # Save as JPEG format
    temp_image.seek(0)
    return temp_image




def authenticate_user_with_facial_recognition(uploaded_image):
    # Preprocess the uploaded image
    processed_image = preprocess_image(uploaded_image)

    # Load the uploaded image into a face_recognition-compatible format
    uploaded_image_data = face_recognition.load_image_file(processed_image)
    uploaded_face_encodings = face_recognition.face_encodings(uploaded_image_data)

    if not uploaded_face_encodings:
        raise ValidationError("No face detected in the uploaded image.")

    uploaded_face_encoding = uploaded_face_encodings[0]

    for user in CustomUser.objects.all():
        profile_picture_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)

        if not os.path.isfile(profile_picture_path):
            continue
        
        profile_image_data = face_recognition.load_image_file(profile_picture_path)
        profile_face_encodings = face_recognition.face_encodings(profile_image_data)

        if not profile_face_encodings:
            continue
        
        profile_face_encoding = profile_face_encodings[0]

        # Compare the uploaded face with the profile picture
        matches = face_recognition.compare_faces([profile_face_encoding], uploaded_face_encoding, tolerance=0.6)

        if matches[0]:  # Match found
            return user

    raise ValidationError("Facial recognition failed. The uploaded image does not match any profile picture.")
