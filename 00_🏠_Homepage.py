import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.app_logo import add_logo

from utils import reduce_top_margin

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
    layout="wide"
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
        st.text('Interactive maps of housing data from the US Census')
    with col2:
        st.image('images/logo.png')

    st.write('---')

    st.markdown("## Information on the App")

    st.write('---')

    column_1, column_2 = st.columns(2)
    with column_1:
        with st.expander("**Getting Started**"):
            st.write("Getting Started")

    with column_2:
        with st.expander("**Dataset Description**"):
            st.markdown("""
                        This app explores the US Census ACS 2021 5-year estimate DP04 dataset and offers comprehensive information about housing in different areas. This data is collected by surveying households and covers a range details that help you understand local housing patterns.

                        **Metrics available to explore:**

                        1. Median Rent Price ($):

                        This metric reveals the median monthly rent paid by renters in a given location, offering a clear picture of rental expenses.
                        
                        2. Renter Occupied Housing (%):

                        Distinguishing between homes owned and rented, this metric provides the percentage of housing that is occupied by renters, aiding in understanding the distribution of ownership.
                        
                        3. Electric, Renewable, or No Heating Source (%):

                        This category highlights the percentage of homes using electric, renewable, or no heating sources, shedding light on energy consumption and environmental impact.
                        
                        4. Direct Fossil Fuel Heating Source (%):

                        Specifically focusing on heating sources, this metric indicates the percentage of homes relying on direct fossil fuels for heating, contributing to insights on energy choices.
                        
                        5. Median Home Value ($):

                        Reflecting the estimated market value of owner-occupied homes, this metric offers an indication of the economic value of residential properties in the area.

                        By exploring these metrics from the ACS 2021 5-year estimate DP04 dataset, you gain a deeper understanding of the housing dynamics across the US, whether you're interested in ownership patterns, heating sources, property values, monthly costs, or rental affordability.
                        """)

    st.markdown("## Walkthrough from the Developer")
    with st.expander("**Tutorial Videos**"):
        st.write("Getting Started")


if __name__ == "__main__":
    run()
