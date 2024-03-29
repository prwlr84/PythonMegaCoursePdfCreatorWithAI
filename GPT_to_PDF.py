import time
import streamlit as st
from helpers import send, create_pdf, dict_to_string


def initialize_session_variables():
    st.session_state.setdefault('full_dict', {})
    st.session_state.setdefault('output', '')
    st.session_state.setdefault('gpt_button_counter', 0)
    st.session_state.setdefault('output_counter', 0)
    st.session_state.setdefault('separator', False)


def display_gpt_input(col):
    prompt = col.text_area('Type your prompt here:', key='prompt')
    gpt_button = col.button('Submit')  # disabled=st.session_state.gpt_button_counter >= 3)
    if gpt_button:
        st.session_state.output = send(prompt)
        st.session_state.gpt_button_counter += 1


def display_gpt_output(col):
    col.write('Output:')
    col.info(st.session_state.output)
    add_prompt = col.checkbox('Add prompt before', key='separator')
    if col.button('Add to PDF'):
        add_output_to_pdf(add_prompt)


def add_output_to_pdf(add_prompt):
    st.session_state.full_dict[st.session_state.output_counter] = {
        'date': time.strftime("%H:%M,%d.%m.%Y"),
        'prompt': st.session_state.prompt if add_prompt else '',
        'separator': st.session_state.separator,
        'output': st.session_state.output
    }
    st.session_state.output_counter += 1
    st.session_state.output = ''
    st.rerun()


def display_pdf_ops(col):
    st.warning(dict_to_string(st.session_state.get('full_dict')))
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        pdf_button = st.button('Generate PDF')
        if pdf_button:
            create_pdf(dict_to_string(st.session_state.get('full_dict')))
            with open('output.pdf', 'rb') as pdf_file:
                pdf_data = pdf_file.read()
            st.download_button(label='Download PDF', data=pdf_data, file_name='output.pdf', mime='application/pdf')
    with f_col2:
        st.empty()
        st.empty()
        reset_button = st.button('Start new PDF')
        if reset_button:
            st.session_state.full_dict = ''
            st.rerun()


st.set_page_config(layout='wide')
initialize_session_variables()
# params = st.query_params

st.header('GPT to PDF')
st.subheader('Collect your GPT outputs into a PDF')

col1, col2, col3 = st.columns(3)

with col1:
    display_gpt_input(col1)

if st.session_state.output:
    with col2:
        display_gpt_output(col2)

if st.session_state.get('full_dict'):
    with col3:
        display_pdf_ops(col3)

