from fpdf import FPDF
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))


def send(prompt):
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=0)

    return response.choices[0].message.content


def create_pdf(output):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font(family='Times', style='B', size=12)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(w=0, h=8, txt=output, align='L', border=0)
    # pdf.line(10, 22, 200, 22)

    pdf.output('output.pdf', )


def dict_to_string(data):
    output = ''
    for item in data.values():
        if item['separator']:
            separator = f'**{item["prompt"]}** - {item["date"]}\n'
            output += f'{separator}\n{item["output"]}\n\n'
        else:
            output += f'{item["output"]}\n\n'

    return output
