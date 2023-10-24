import streamlit as st
from streamlit_extras.app_logo import add_logo

from mapping import create_choropleth
from sidebar import init_sidebar
from utils import reduce_top_margin

st.set_page_config(
    page_title="Heat Maps",
    page_icon="🔥",
    layout="wide"
)


def app():
    # Remove white space at top of page
    reduce_top_margin()

    # Add logo to sidebar
    add_logo("images/sidebar_logo.png", height=100)

    # Add a title and an explanation for the user
    st.title('🔥 Heat Maps')
    st.markdown(
        """
        Description of the page
        """)

    # Initalize the sidebar
    init_sidebar()

    # Fetch the data (cached for performance)

    # Display the map
    # create_choropleth()


app()
