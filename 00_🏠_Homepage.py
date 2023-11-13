import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page

from utils import reduce_top_margin

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
    # layout="wide"
)


def run():

    # Remove white space at top of page
    reduce_top_margin()

    # Add logo to sidebar
    add_logo("images/sidebar_logo.png", height=100)

    st.experimental_set_query_params()

    col1, col2 = st.columns(2)
    with col1:
        st.title('Geographic Analysis App')
        st.text('Putting Data Analytics "On the Map"')
    with col2:
        st.image('images/logo.png')

    st.write('---')

    # Add tutorial video
    # components.iframe(
    #     src="https://www.loom.com/share/")

    column_1, column_2, column_3 = st.columns((1, 3, 3))

    with column_1:
        st.write('Most Used Pages:')

    with column_2:
        if st.button("Page 1", use_container_width=True):
            switch_page("page_1")
        if st.button("Page 2", use_container_width=True):
            switch_page("page_1")
        if st.button("Page 3", use_container_width=True):
            switch_page("page_1")

    with column_3:
        if st.button("Page 4", use_container_width=True):
            switch_page("page_1")
        if st.button("Page 5", use_container_width=True):
            switch_page("page_1")
        if st.button("Page 6", use_container_width=True):
            switch_page("page_1")

    st.write('---')

    column_1, column_2, column_3 = st.columns(3)
    with column_1:
        with st.expander("**Item 1**"):
            st.write("Getting Started")

    with column_2:
        with st.expander("**Item 2**"):
            st.write("Getting Started")

    with column_3:
        with st.expander("**Item 3**"):
            st.write("Getting Started")


if __name__ == "__main__":
    run()
