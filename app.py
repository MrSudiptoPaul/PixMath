import streamlit as st
from streamlit import session_state as state
from ui import sidebar
import operations as ops
import io

sidebar()

col1, col2 = st.columns(2)

with col1:
    st.write("### Images to Process")

    if state.img_1 is not None:
        st.image(state.img_1, caption="First Image")
    else:
        st.info("Waiting for First Image...")

    if state.operation in ("AND", "XOR", "OR"):
        if state.img_2 is not None:
            st.image(state.img_2, caption="Second Image")
        else:
            st.info("Waiting for Second Image...")

with col2:
    st.write("### Final Processed Image")

    if state.last_op != state.operation and not state.execute_operation:
        state.final_result_img = None
        state.show_decoded_text = False

    if state.execute_operation:
        try:
            result_img = None
            op = state.operation

            if state.img_1 is None:
                st.error("Please upload the First Image.")
            else:
                if op == "NOT":
                    result_img = ops.apply_not(state.img_1)
                elif op == "Add":
                    result_img = ops.apply_add(state.img_1, state.operation_value)
                elif op == "Subtract":
                    result_img = ops.apply_subtract(state.img_1, state.operation_value)
                elif op in ("AND", "OR", "XOR"):
                    if state.img_2 is None:
                        st.error(
                            "Please upload the Second Image for logical operations."
                        )
                    else:
                        if op == "AND":
                            result_img = ops.apply_and(state.img_1, state.img_2)
                        elif op == "OR":
                            result_img = ops.apply_or(state.img_1, state.img_2)
                        elif op == "XOR":
                            result_img = ops.apply_xor(state.img_1, state.img_2)

                elif op == "Hide Password":
                    if state.secret_text:
                        result_img = ops.hide_password(state.img_1, state.secret_text)
                    else:
                        st.error("Please enter a Secret Text to hide.")

            if result_img is not None:
                state.final_result_img = result_img
                state.last_op = op
                state.show_decoded_text = False
            else:
                state.final_result_img = None

        except Exception as e:
            st.error(f"Something went wrong: {e}")

        state.execute_operation = False

    if state.final_result_img is not None:

        st.image(state.final_result_img, caption=f"Result of {state.last_op}")

        if state.last_op == "Hide Password":
            if st.button("Decode Text from Image"):
                state.show_decoded_text = True

            if state.show_decoded_text:
                img_bytes = io.BytesIO()
                state.final_result_img.save(img_bytes, format="PNG")
                img_bytes.seek(0)

                decoded_text = ops.decode_password(img_bytes)
                st.info(f"**Decoded Text:** {decoded_text}")

    elif not state.execute_operation:
        st.info("Ready? Click **'Apply Operation'**.")
