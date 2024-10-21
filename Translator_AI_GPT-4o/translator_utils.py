from g4f.client import Client

def translate_using_g4f(input_language, output_language, input_text):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f'''Translate from {input_language} to {output_language} 
                   in the form 
                   input_sentence:
                   Translation:
                   : {input_text}
                   '''}],
    )
    translated_text = response.choices[0].message.content.strip()
    return translated_text.split('\n')[-1].split(':')[-1]