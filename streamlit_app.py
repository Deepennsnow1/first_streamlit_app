import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents\' New Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# New section to display Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice=streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:  
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    # output it to the screen as a table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()


# Check to Confirm the Snowflake Connector Package Will Add Successfully

streamlit.stop()

# Let's Query Some Data, Instead

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.text("The fruit load list contains")
#streamlit.text(my_data_row)

# Let's Change the Streamlit Components to Make Things Look a Little Nicer

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.header("The fruit load list contains")
#streamlit.dataframe(my_data_row)

# Oops! Let's Get All the Rows, Not Just One

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)

# allow the user to add a fruit

add_my_fruit=streamlit.text_input('What fruit would you like to add?', ' ')
streamlit.write('Thanks for adding', add_my_fruit)

# add fruit to snowflake table
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')");
