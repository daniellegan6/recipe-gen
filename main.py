import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
from recipe_scrapers import scrape_me
#python -m streamlit run your_script.py

template = """
###
Convert the recipe to fit the user preferance based on his diet list.
The desired format:
ingredients: (write the ingredients line by line)
seperate paragraph
constructor: -||-
seperate paragraph
Enjoy!
###

###
Beloow is a list with the diet preferance and the recipe:
Diet:{diet},
Recipe:{recipe}
###

YOUR ANSWER:
"""
# if using few shot prompting:
###
# Below is an example:
# Diet list: vegan, gluten free.
# Recipe: 1.5 cup milk, 100g butter, 1 cup wheet.
# Therefor your answer will be: 1.5 cup soy-milk, 100g vegan butter like Naturina, 1 cup gluten free wheet. 
###
# <comma_separated_list_of_ingredients_names>

prompt = PromptTemplate(
    input_variables=["diet", "recipe"],
    template=template,
)

def load_LLM():
    llm = OpenAI(temperature=0)
    return llm

llm = load_LLM()


#rendering page with streamlit
st.set_page_config(page_title="Recipe Generator", page_icon=":root:")

st.title("Recipe Generator")

#session
if 'clicked_url' not in st.session_state:
    st.session_state.clicked_url = False

if 'submit_clicked' not in st.session_state:
    st.session_state.submit_clicked = False

if 'clicked_rec' not in st.session_state:
    st.session_state.clicked_rec = False

def click_url_button():
    st.session_state.clicked_url = True

def click_rec_button():
    st.session_state.clicked_rec = True

def submit_click():
    st.session_state.submit_clicked = True

col1, col2, col3 = st.columns(3)
with col1:
    diet_choices = st.multiselect(label="", options=['vegan','sugar free', 'gluten free', 'dairy free', 'vegeterian'], placeholder='Choose diet preference')
with col2:
    url_clicked = st.button('url', key=0, on_click=click_url_button)
with col3:
    recipe_clicked = st.button('recipe', key=1, on_click=click_rec_button)

def scrapping(url):
    try:
        scraper = scrape_me(url)
        ingredients, instructions = scraper.ingredients()[0], scraper.instructions()
        text = "ingredients: {} \ninstructions: {}".format(ingredients, instructions)
        return text
    except: 
        return None

def get_input_button():
    if st.session_state.clicked_url:
        col_a, col_b = st.columns(2)
        with col_a:
            input_url = st.text_input(label="", placeholder="enter url")
        with col_b:
            st.button("submit", key=2, on_click=submit_click)
            input_text = scrapping(input_url)
            if input_text is not None:
                if st.session_state.submit_clicked:
                    return input_text
                else: 
                    st.session_state.submit_clicked = False
                    st.write("Error: can't read url, try another one")
    if st.session_state.clicked_rec:
        st.session_state.clicked_rec = False
        col_a, col_b = st.columns(2)
        with col_a:
            input_text = st.text_area(label="", placeholder="enter recipe")
        with col_b:
            st.button("submit", key=3, on_click=submit_click)
            if input_text is None or st.session_state.submit_clicked:
                st.session_state.submit_clicked = False
                st.write("Error: not a valid text")
                return None
        return input_text
        

input_recipe = get_input_button()

if input_recipe is not None and st.session_state.submit_clicked:
    prompt_with_values = prompt.format(diet=diet_choices, recipe=input_recipe)
    formatted_recipe = llm(prompt_with_values)
    st.write(formatted_recipe)
    st.download_button('Download recipe', formatted_recipe) 
    st.session_state.submit_clicked = False
    st.session_state.clicked_url = False

    
    



# def run_componenet(props):
#     value = component_toolbar_buttons(key='toolbar_buttons', **props)
#     return value

# def handle_event(value):
#     st.write('recived from component', value)

# props = {
#     'buttons': {
#         'url': False,
#         'recipe': False
#     }
# }

# st.column_config(['col', 'col2'])
# handle_event(run_componenet(props))

