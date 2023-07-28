import json

import openai


openai.api_key = r'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'
test_dict = {'עגבניות שרי תמר': 0.9111111111111111, 'עגבניות שרי צהוב': 0.8958333333333334,
             'עגבניות שרי מיקס': 0.8958333333333334, 'עגבניות שרי קופסא': 0.8823529411764706,
             'עגבניות שרי 460 ג': 0.8823529411764706, 'עגבניות שרי אדומות': 0.8703703703703703,
             'עגבניות שרי ליקופן': 0.8703703703703703, 'עגבניות חתוכות דק רמילוי': 0.7752525252525252,
             'עגבניות מיובשות 200 גרם תקוע': 0.7673160173160173, 'עגבניה': 0.7626262626262627}


def cut_string_between_brackets(input_string):
    start_index = input_string.find('{')
    end_index = input_string.rfind('}')

    if start_index != -1 and end_index != -1:
        cut_string = input_string[start_index:end_index + 1]
        return cut_string
    else:
        return None


def main():
    f = open('question.txt', 'r', encoding='utf-8')
    res = f.read()
    res = res.replace('<<>>', 'ל' + 'עגבניות שרי')
    for key in test_dict:
        res += f'\n{key}'
    response = openai.ChatCompletion.create(
        model="gpt-4",  # The engine to use (GPT-3.5)
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': res}]
    )
    generated_text = response.choices[0].message.content
    dict_text = json.loads(cut_string_between_brackets(generated_text))
    for key in dict_text:
        print(f'{key}: {dict_text[key]}')


if __name__ == '__main__':
    main()
