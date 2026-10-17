import streamlit as st
from streamlit import session_state as state
from ui import sidebar

sidebar()

# --- MAIN APP AREA ---

col1, col2 = st.columns(2)

with col1:
    st.write("### Images to Process")

    if state.img_1 is not None:
        st.image(state.img_1, caption="First Image")
    else:
        st.info("Waiting for First Image...")

    if state.operation in ("AND", "XOR", "XNOR", "OR"):
        if state.img_2 is not None:
            st.image(state.img_2, caption="Second Image")
        else:
            st.info("Waiting for Second Image...")

with col2:
    st.write("### Final Processed Image")
