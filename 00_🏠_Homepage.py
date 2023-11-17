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

                        1. **Owner vs Renter Occupied:**
                        - This column distinguishes between homes owned by their occupants and those that are rented. It provides insights into the housing landscape, helping you understand the distribution of homeownership and rental properties in your chosen area.

                        2. **House Heating Fuel:**
                        - Reveals the primary heating sources used in homes, offering insights into energy consumption and environmental impact. Categories may include natural gas, electricity, oil, etc.

                        3. **Value:**
                        - Represents the estimated market value of owner-occupied homes. This column gives an indication of the economic value of residential properties in the area.

                        4. **SMOC (Selected Monthly Owner Costs):**
                        - Refers to the total monthly costs associated with owning a home, including mortgage payments, property taxes, and insurance. This metric helps users gauge the financial commitment of homeownership.

                        5. **SMOCAPI (Selected Monthly Owner Costs as a Percentage of Income):**
                        - Expresses the portion of the household income dedicated to covering monthly homeownership costs. This percentage is a crucial indicator for understanding the affordability of homeownership in a given location.

                        6. **Gross Rent:**
                        - Represents the total monthly rent paid by renters. It includes rent plus the cost of any utilities and fuels. This figure provides insights into the overall rental expenses in the area.

                        7. **GRAPI (Gross Rent as a Percentage of Income):**
                        - Indicates the percentage of a household's income allocated to cover rental costs. This metric helps assess the affordability of renting in a specific location.

                        By exploring these metrics from the ACS 2021 5-year estimate DP04 dataset, you gain a deeper understanding of the housing dynamics across the US, whether you're interested in ownership patterns, heating sources, property values, monthly costs, or rental affordability.
                        """)

    st.markdown("## Walkthrough from the Developer")
    with st.expander("**Tutorial Videos**"):
        st.write("Getting Started")


if __name__ == "__main__":
    run()
