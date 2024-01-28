import json

# Function to check if the conversation follows the correct order
def check_conversation_order(conversation):
    expected_order = ['human', 'gpt'] * ((len(conversation) + 1) // 2)
    expected_order = expected_order[:len(conversation)]  # trim the expected_order to the length of the actual conversation

    actual_order = [turn['from'] for turn in conversation]
    return actual_order == expected_order

def filter_data(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        data = json.load(input_file)

    filtered_data = []
    for item in data:
        conversations = item.get('conversations', [])
        # Only include conversations that have at least 2 turns and follow the correct order
        if len(conversations) >= 2 and check_conversation_order(conversations):
            filtered_data.append(item)

    print(f'The total number of valid items after filtering: {len(filtered_data)}')

    with open(output_filename, 'w') as output_file:
        json.dump(filtered_data, output_file, indent=2)

filter_data('instruction.json', 'output.json')
