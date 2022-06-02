import streamlit
import pandas

streamlit.title('My Parents\' New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Pull csv from S3 bucket into my_fruit_list dataframe
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Use the fruit name column as the index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Add a pick list so the user can pick fruit to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display data table on the page
streamlit.dataframe(my_fruit_list)
