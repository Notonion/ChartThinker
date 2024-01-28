import os
import openai
openai.api_base = "https://api.chatanywhere.com.cn/v1"
import json
import time
from tqdm import tqdm
os.environ["OPENAI_API_KEY"] = "your key"
openai.api_key = os.getenv("OPENAI_API_KEY")
import asyncio
def read_json_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def extract_info(data):
    info_dict = {}
    for element in data:
        id = element['id']
        conversations = element['conversations']
        info_string = ''

        for conversation in conversations:
            if conversation['from'] == 'human':
                value = conversation['value']
                info_string += value.replace('<image>\nWhat is the detailed information about the chart', '').strip()
            if conversation['from'] == 'gpt':
                value = conversation['value']
                info_string += '：' + value.strip()
        info_dict[id] = info_string
    return info_dict
async def count_calls_per_minute(semaphore, max_calls):
    count = 0
    start_time = time.time()
    while True:
        await asyncio.sleep(1)
        count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:
            print(f"Counts: {count}")
            count = 0
            start_time = current_time
            semaphore.release(max_calls)  #  semaphore

async def call_chat_gpt_and_save(info_dict, filename,semaphore):
    for id, info in tqdm(info_dict.items()):
        async with semaphore:
            conversation = []
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {
                        
                    },
                    {
                        "role": "user",
                        "content": f"Given text: [{info}]"
                    },
                ],
                temperature=1,  
                n=1,  
                stream=False,  
                stop=None,  
                presence_penalty=2.0, 
                frequency_penalty=0,
            )
            content_list = ''
            for choice in completion.choices:
                content_list = content_list+choice.message.content

            content_list = content_list.split('\n')

            for content in content_list:
                if content.startswith('Question 1'):
                    conversation.append({'from': 'human', 'value': '<image>\n'+content[11:]})
                elif content.startswith('Question'):
                    conversation.append({'from': 'human', 'value': content[11:]})
                elif content.startswith('Answer'):
                    conversation.append({'from': 'gpt', 'value': content[9:]})

            # Save the conversation to the file
            conversation_entry = {
                'id': id,
                'image': id + '.png',
                'conversations': conversation
            }
            with open(filename, 'a') as f:
                json.dump(conversation_entry, f, indent=2)
                f.write(",\n")
async def main(info_dict, output_filename):
    tpm_limit = 30
    semaphore = asyncio.Semaphore(tpm_limit)  

    coroutine1 = call_chat_gpt_and_save(info_dict, output_filename, semaphore)
    coroutine2 = count_calls_per_minute(semaphore, tpm_limit)

    await asyncio.gather(coroutine1, coroutine2)

# Use your own file paths
input_filename = 'input.json'
output_filename = 'output.json'

data = read_json_file(input_filename)
info_dict = extract_info(data)
asyncio.run(main(info_dict, output_filename))
