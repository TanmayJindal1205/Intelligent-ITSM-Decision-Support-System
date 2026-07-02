import streamlit as st

def metric_card(title, value, color="#ffffff"):

    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"""
            <h3 style="
                color:{color};
                margin:0;
                padding-top:8px;
            ">
                {value}
            </h3>
            """,
            unsafe_allow_html=True
        )