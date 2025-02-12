import g4f

response = g4f.ChatCompletion.create(model='gpt-3.5o',
                                    messages=[{"role": "user", "content": "what is machine learning"}])

for message in response:
    print(message, flush=True, end='')