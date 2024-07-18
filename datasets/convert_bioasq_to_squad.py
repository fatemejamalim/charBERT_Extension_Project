import json

def load_bioasq_data(file_path):
    """
    Load BioASQ data from a JSON file.

    Args:
        file_path (str): Path to the BioASQ JSON file.

    Returns:
        dict: Loaded BioASQ data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def convert_bioasq_to_squad(bioasq_data):
    """
    Convert BioASQ data to SQuAD-like format.

    Args:
        bioasq_data (dict): BioASQ data.

    Returns:
        list: SQuAD-like formatted data.
    """
    squad_like_data = []

    for question_entry in bioasq_data['questions']:
        question_id = question_entry['id']
        question_text = question_entry['body']
        context = "".join([snippet['text'] + "\n" for snippet in question_entry['snippets']])
        answers = extract_answers(question_entry)

        squad_like_data.append({
            'paragraphs': [{
                'context': context,
                'qas': [{
                    'question': question_text,
                    'id': question_id,
                    'answers': answers
                }]
            }]
        })

    return squad_like_data

def extract_answers(question_entry):
    """
    Extract answers from a BioASQ question entry.

    Args:
        question_entry (dict): A single question entry from BioASQ data.

    Returns:
        list: Extracted answers.
    """
    answers = []

    if 'exact_answer' in question_entry:
        for answer in question_entry['exact_answer']:
            if isinstance(answer, dict):
                answers.append({'text': answer['text'], 'answer_start': answer['offset']})
            else:
                answers.append({'text': answer, 'answer_start': 0})
    
    elif 'ideal_answer' in question_entry:
        for answer in question_entry['ideal_answer']:
            if isinstance(answer, dict):
                answers.append({'text': answer['text'], 'answer_start': 0})
            else:
                answers.append({'text': answer, 'answer_start': 0})

    return answers

def save_to_json(data, output_file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to save.
        output_file_path (str): Path to the output JSON file.
    """
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    bioasq_file_path = './datasets/bioasq/11B1_golden.json'
    output_file_path = 'bioasq_to_squad_test.json'

    bioasq_data = load_bioasq_data(bioasq_file_path)
    squad_like_data = convert_bioasq_to_squad(bioasq_data)
    save_to_json(squad_like_data, output_file_path)

    bioasq_file_path = './datasets/bioasq/training11b.json'
    output_file_path = 'bioasq_to_squad_train.json'

    bioasq_data = load_bioasq_data(bioasq_file_path)
    squad_like_data = convert_bioasq_to_squad(bioasq_data)
    save_to_json(squad_like_data, output_file_path)

if __name__ == "__main__":
    main()
