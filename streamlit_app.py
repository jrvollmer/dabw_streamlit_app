import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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


# Function for Fruityvice API call
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # Take the json version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# Fruityvice API call section
streamlit.header("Fruityvice Fruit Advice (Maybe?)!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    # Get Fruityvice API response
    fruityvice_json = get_fruityvice_data(fruit_choice)
    # Output it as a table
    streamlit.dataframe(fruityvice_json)

except URLError as e:
  streamlit.error()


# Snowflake section
streamlit.header("View Our Fruit List - Add Your Favorites!")

# Get fruit load list
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Load the fruit on a button click
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)


# Insert new_fruit into fruit_load_list and return a message thanking the user for adding new_fruit
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

# Allow the user to add a fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add?")
# Add the fruit to the list on a button click
if streamlit.button('Add Fruit to List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_snowflake(add_my_fruit))
  my_cnx.close()
