import streamlit
import pandas
import requests
import snowflake.connector

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
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Alternative suggestion for picker: streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display data table on the page
streamlit.dataframe(fruits_to_show)

# Display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice (Maybe?)!")

fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Take hte json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output it as a table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
