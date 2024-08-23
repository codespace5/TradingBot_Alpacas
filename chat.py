import requests

api_key = "skkkkkkkkkkkkkkkk-yk4TIBiKckoessctyh" "U5T3BlbkFJz68IXN6mOfDhFkAXGkG3"

def chat_with_chatgpt(prompt):
    model = "text-davinci-003"
    response = requests.post(
        f"https://api.openai.com/v1/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "prompt": prompt,
            "max_tokens": 5000,
            "model": model
        }
    )

    if response.status_code == 200:
        data = response.json()
        choices = data["choices"]
        if choices:
            generated_text = choices[0]["text"].strip()
            print(generated_text)
        else:
            print("No completion choices returned.")
    else:
        print("Request failed with status code:", response.status_code)


prompt_string = """
Current BTC/USD data is as follows:
symbol='BTC/USD' timestamp=datetime.datetime(2023, 11, 16, 12, 25, 10, 692305, tzinfo=TzInfo(UTC)) Ask_exchange=None Ask_price=37135.5 Ask_size=0.276708 bid_exchange=None bid_price=37106.956 bid_size =0.5547

MA25 is 34830.67738.
MA75 is 29549.469233333337.

the price values for 25 days:
[30693.226, 34427.39, 34191.685, 34701.289, 34109.1, 34088.6765, 34025.3665, 34321.405, 34243.43, 34444.9, 35484.835, 3438 6.025, 34691.744, 35181.957, 34845.675, 34913.7825, 35276.515, 36589.7905, 36768.015, 37106.4445, 37096.9415, 36947.728, 3 6 641.4755, 35620.4765 , 37466.8835 ]

the price values for 75 days:
[25871.41, 25975.116, 25688.05, 25745.93, 25803.645, 26309.161, 25861.055, 25829.9685, 25766.3, 25751.1, 25917.26, 26213.956, 26649.95, 26563.0595, 26562.576, 26631.7685, 26853.825, 27084.11, 27091.783, 26646.789, 26547.1485, 26569.8, 26142.75, 26335.55, 26231.4, 26421.645, 26969.955, 26926.785, 27049.385, 28072.53, 27633.665, 27386.639, 27699.144, 27533.952, 27929.25, 27951.1095, 27943.19, 27609.457, 27125.933, 26814.499, 26794.97, 26907.783, 26884.967, 27263.29, 28198.33, 28731.8835, 28291.2155, 29329.21, 29563.0595, 29969.0615, 30693.226, 34427.39, 34191.685, 34701.289, 34109.1, 34088.6765, 34025.3665, 34321.405, 34243.43, 34444.9, 35484.835, 34386.025, 34691.744, 35181.957, 34845.675, 34913.7825, 35276.515, 36589.7905, 36768.015, 37106.4445, 37096.9415, 36947.728, 36641.4755, 35620.4765, 37466.8835]

Please analyze MA25 and MA75 and let me know if I can make money if I buy BTC/USD now.
Which is better: buy or hold?
Answer the only one word.

"""
# chat_with_chatgpt(prompt=prompt_string)
chat_with_chatgpt("what is an apple?")


# import openai
# openai.api_key = "sggggggggggggggggk-yk4TIBiKckoess" "ctyhU5T3BlbkFJz68IXN6mOfDhFkAXGkG3"
# def chat_with_chatgpt(prompt, model="davinci-003):
#     response = openai.Completion.create(
#         engine=model,
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = response.choices[0].text.strip()
#     return message


# user_prompt = "Write a summary of the benefits of exercise."
# chatbot_response = chat_with_chatgpt(user_prompt)
# print(chatbot_response)