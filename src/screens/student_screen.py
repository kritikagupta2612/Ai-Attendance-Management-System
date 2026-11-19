
import streamlit as st
import numpy as np
import time
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.pipelines.face_pipeline import (
    get_face_embeddings,
    train_classifier,
    predict_face
)

from src.pipelines.voice_pipelines import get_voice_embedding

from src.database.db import get_all_students, create_student


def student_dashboard():
    st.header("DASHBOARD HERE")


def student_screen():

    style_base_layout()
    style_background_dashboard()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to home", type="secondary", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using Face ID", text_alignment="center")
    st.space()
    st.space()

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_source = st.camera_input("Position your face in the center")

    if photo_source is not None:

        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_face(img)

        if num_faces == 0:
            st.warning("Face not found")

        elif num_faces > 1:
            st.warning("Multiple faces found. Please capture only one face.")

        else:
            if detected:

                student_id = list(detected.keys())[0]

                all_students = get_all_students()

                student = next(
                    (s for s in all_students
                     if str(s['student_id']) == str(student_id)),
                    None
                )

                if student:

                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student

                    st.toast(
                        f"Welcome Back {student.get('name')}",
                        icon="👋"
                    )

                    time.sleep(1)
                    st.rerun()

                else:
                    st.error("Student record not found in database.")

            else:
                st.info("Face not recognized. You might be a new student.")
                st.session_state.show_registration = True

    if st.session_state.show_registration:

        if photo_source is None:
            st.warning("Please capture your face again.")

        else:
            with st.container(border=True):

                st.header("Register yourself")

                new_name = st.text_input(
                    "Enter your name",
                    placeholder="Enter your name"
                )

                st.header("Optional: Voice Enrollment")
                st.info("Enroll your voice for voice-only attendance.")

                audio_data = st.audio_input(
                    "Record your voice: I am present, my name is..."
                )

                if st.button("Create Account", type="primary"):

                    if not new_name.strip():
                        st.warning("Please enter your name.")

                    else:
                        with st.spinner("Creating your account..."):

                            img = np.array(
                                Image.open(photo_source).convert("RGB")
                            )

                            encodings = get_face_embeddings(img)

                            if encodings:

                                face_emb = encodings[0].tolist()

                                voice_emb = None

                                if audio_data:
                                    audio_bytes = audio_data.read()
                                    voice_emb = get_voice_embedding(audio_bytes)

                                response_data = create_student(
                                    new_name.strip(),
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )

                                if response_data:

                                    train_classifier()

                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.show_registration = False

                                    st.toast(
                                        f"Profile created! Hi {new_name}",
                                        icon="👋"
                                    )

                                    time.sleep(1)
                                    st.rerun()

                                else:
                                    st.error("Couldn't create your student account.")

                            else:
                                st.error("Couldn't capture your face for registration.")

    footer_dashboard()
