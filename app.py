from serpapi import GoogleSearch
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def compare(med_name):
    params = {
    "engine": "google_shopping",
    "q": med_name,
    "location": "Austin, Texas, United States",
    "google_domain": "google.com",
    "hl": "en",
    "gl": "in",
    "api_key": "372ca0cee10dff3df9eb513622470596d290feb49b3166ffc3f06029a3b7473b"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results['shopping_results']
    return shopping_results


c1,c2 = st.columns(2)
c1.image("e_pharmacy.png", width = 200)
c2.header(" E-pharmacy price comparison system")

"""--------------------------------------------------"""

st.sidebar.title("Enter Name of Medicine")
med_name = st.sidebar.text_input("Enter Name here⤵️")
number = st.sidebar.text_input("Enter Number of Options here⤵️")
medicine_comp = []
med_price = []

if med_name is not None:
    if st.sidebar.button("Price compare"):

        shopping_results = compare(med_name)
        lowest_price  = float((shopping_results[0].get('price'))[1:])
        print(lowest_price)
        lowest_price_index = 0
        st.sidebar.image(shopping_results[0].get('thumbnail'))


        for i in range(int(number)):
            current_price = float((shopping_results[i].get('price'))[1:])
            medicine_comp.append(shopping_results[i].get('source'))
            med_price.append(float((shopping_results[i].get('price'))[1:]))

            # --------------------------------------------------------------
            st.title(f"Option{i+1}")
            c1,c2 = st.columns(2)
            c1.write("Company :")
            c2.write(shopping_results[i].get('source'))

            c1.write("title :")
            c2.write(shopping_results[i].get('title'))

            c1.write("price :")
            c2.write(shopping_results[i].get('price'))


            url = shopping_results[i].get('product_link')
            c1.write("Buy Link :")
            link_html = f'<a href="{url}" target="_blank" style="color:blue; text-decoration:none;">Link</a>'
            c2.markdown(link_html, unsafe_allow_html=True)
            """---------------------------------------------------------"""

            if(current_price<lowest_price):
                lowest_price = current_price
                lowest_price_index = i

        # this is best option
        st.title("Best Option")
        c1,c2 = st.columns(2)
        c1.write("Company :")
        c2.write(shopping_results[lowest_price_index].get('source'))

        c1.write("title :")
        c2.write(shopping_results[lowest_price_index].get('title'))

        c1.write("price :")
        c2.write(shopping_results[lowest_price_index].get('price'))


        url = shopping_results[lowest_price_index].get('product_link')
        c1.write("Buy Link :")
        link_html = f'<a href="{url}" target="_blank" style="color:blue; text-decoration:none;">Link</a>'
        c2.markdown(link_html, unsafe_allow_html=True)            

        # ---------------------------------------------------------------
        # Graph Compare
        df = pd.DataFrame(med_price,medicine_comp )
        st.title("Chart comparison")
        st.bar_chart(df)

        # -----------------------------------------------------------------
        fig, ax = plt.subplots()
        ax.pie(med_price, labels=medicine_comp, shadow=True)
        ax.axis("equal")  # Makes the pie chart circular
        st.pyplot(fig)
