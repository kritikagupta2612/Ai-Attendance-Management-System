import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students
def load_dlib_models():
    # Load the dlib face detector and shape predictor models
    detector = dlib.get_frontal_face_detector()  #Possible kitne chehre hai and kaha kaha hai wo detect karke batata hai
    sp = dlib.shape_predictor(   #detect landmark
        face_recognition_models.pose_predictor_model_location())
    facerec = dlib.face_recognition_model_v1(    #we use models to make it more effiecient and accurate
        face_recognition_models.face_recognition_model_location()
        )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    # Load the dlib models
    detector, sp, facerec = load_dlib_models()

    # Detect faces in the image
    faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptors = facerec.compute_face_descriptor(image_np, shape,1) #128 embeddings for each face 
        encodings.append(np.array(face_descriptors))
        return encodings
@st.cache_resource
def get_trained_model():
        # Load the dlib models
        detector, sp, facerec = load_dlib_models()

        # Get all students from the database
        student_db = get_all_students()

        # Prepare training data
        X = [] #suppose 15 students ki embeddings
        y = [] #suppose 15 students ki embeddings ke corresponding labels(ids)

        if not student_db:
            return None

        for student in student_db:

            embedding = student.get('face_embedding')

            if embedding:
                X.append(np.array(embedding)) 
                y.append(student.get('student_id')) 

        # Train the SVM model
        if len(X) == 0:
            return None
        clf = SVC(kernel='linear', probability=True, class_weight='balanced')

        try:
            clf.fit(X, y)
        except ValueError :
            pass
        return {'clf': clf, 'X' : X, 'y': y}

def train_classifier(): #tab use karenge jab kisi naye student ki entry hogi ya fir kisi student ka face update hoga
        st.cache_resource.clear()
        model_data = get_trained_model()
        return bool(model_data)
        
def predict_face(class_image_np): #array k form me faces lelega 
        encodings = get_face_embeddings(class_image_np) #group photo se embeddings nikal k dedega ki itne faces hai aur unke embeddings kya hai

        detected_students = {}
        model_data = get_trained_model()
        if not model_data:
            return detected_students, []  , len(encodings)    # ([] => jitne ki students hai unki list hai
        clf = model_data['clf']
        X_train = model_data['X']
        y_train = model_data['y']

        all_students = sorted(list(set(y_train))) #jitne bhi students hai unki list hai

       
def predict_face(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}
    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        elif len(all_students) == 1:
            predicted_id = int(all_students[0])
        else:
            continue

        student_embeddings = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(
            student_embeddings - encoding
        )

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)

                 
            


