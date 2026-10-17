import streamlit as st
from streamlit import session_state as state


def sidebar():
    with st.sidebar:
        # Operation Selection
        state.operation = st.selectbox(
            "Select Operation",
            [
                "Add",
                "Subtract",
                "Left Shift",
                "Right Shift",
                "NOT",
                "AND",
                "OR",
                "XOR",
                "XNOR",
                "Hide Password",
            ],
        )

        # Dynamic Input Fields based on the operation chosen
        if state.operation in ("Add", "Subtract", "Left Shift", "Right Shift"):
            state.operation_value = st.number_input("Operation Value", value=0)
        elif state.operation == "Hide Password":
            state.secret_text = st.text_input("Secret Text", type="password")

        st.divider()

        # Session State Initialization
        if "img_1" not in state:
            state.img_1 = None
        if "img_2" not in state:
            state.img_2 = None
        if "last_img" not in state:
            state.last_img = None

        # Image Source Selection
        input_method = st.radio(
            "Image Source", ["Upload Image", "Use Camera"], horizontal=True
        )

        # Default to First Image
        img_upload = "First Image"

        # Two-image selection logic
        if state.operation in ("AND", "XOR", "XNOR", "OR"):
            img_upload = st.radio(
                "Select Image Slot:", ["First Image", "Second Image"], horizontal=True
            )

        img_input = None

        # Camera or Upload Logic
        if input_method == "Use Camera":
            img_input = st.camera_input("Take a picture", key="main_cam")

            # messages for camera overlap
            if img_input is not None:
                if img_upload == "Second Image" and img_input == state.img_1:
                    st.warning(
                        "👆 To capture the Second Image, click 'Clear photo' above first."
                    )
                elif img_upload == "First Image" and img_input == state.img_2:
                    st.warning(
                        "👆 Click 'Clear photo' above to retake the First Image."
                    )
        else:
            img_input = st.file_uploader(
                "Upload Image",
                type=["png", "jpg", "jpeg"],
                key="file_upload",
            )

        # Data Save Logic
        if img_input is not None and img_input != state.last_img:
            if img_upload == "First Image":
                state.img_1 = img_input
            elif img_upload == "Second Image":
                state.img_2 = img_input
            state.last_img = img_input

        st.divider()

        # Execution Button
        if st.button("Apply Operation", type="primary", use_container_width=True):
            st.toast("Processing Image...")
