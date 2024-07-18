from datasets import load_dataset
import os

def save_ner_data(dataset, split, int_to_str_func, output_path):
    """
    Saves NER data to a specified file.

    Args:
        dataset (Dataset): The dataset to save.
        split (str): The split of the dataset (e.g., 'train', 'validation', 'test').
        int_to_str_func (function): Function to convert integer tags to string labels.
        output_path (str): Path to the output file.
    """
    with open(output_path, 'w') as f:
        for tokens, tags in zip(dataset[split]['tokens'], dataset[split]['ner_tags']):
            for token, tag in zip(tokens, tags):
                f.write(f'{token} {int_to_str_func(tag)}\n')
            f.write('\n')

def main():
    dataset = load_dataset("jnlpba")

    # Divide validation set into validation and test
    val_test = dataset['validation']
    dataset['validation'] = val_test.shard(2, index=0)
    dataset['test'] = val_test.shard(2, index=1)

    int_to_str = dataset['train'].features["ner_tags"].feature.int2str
    output_dir = 'datasets/medical_domain/ner/'
    os.makedirs(output_dir, exist_ok=True)

    save_ner_data(dataset, 'train', int_to_str, os.path.join(output_dir, 'train.txt'))
    save_ner_data(dataset, 'validation', int_to_str, os.path.join(output_dir, 'val.txt'))
    save_ner_data(dataset, 'test', int_to_str, os.path.join(output_dir, 'test.txt'))

    # Save labels
    labels = dataset['train'].features['ner_tags'].feature.names
    with open(os.path.join(output_dir, 'labels.txt'), 'w') as f:
        f.write('\n'.join(labels))

if __name__ == "__main__":
    main()
