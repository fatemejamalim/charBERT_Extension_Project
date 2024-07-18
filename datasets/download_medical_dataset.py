import datasets
import os

def save_texts_to_file(texts, file_path):
    """
    Saves a list of texts to a specified file.

    Args:
        texts (list): List of text strings to save.
        file_path (str): Path to the output file.
    """
    with open(file_path, 'w', encoding="utf-8") as f:
        for text in texts:
            f.write(text + '\n')

def main():
    dataset = datasets.load_dataset("pubmed_qa", "pqa_unlabeled")
    dataset = dataset['train'].shuffle(seed=42).select(range(len(dataset["train"]) // 2))
    full_texts = dataset["long_answer"]

    train_len = len(full_texts)
    val_len = test_len = int(train_len * 0.1)
    train_texts = full_texts[:train_len - val_len - test_len]
    val_texts = full_texts[train_len - val_len - test_len:train_len - test_len]
    test_texts = full_texts[train_len - test_len:]

    general_path = 'datasets/medical_domain/mlm/'
    os.makedirs(general_path, exist_ok=True)

    save_texts_to_file(train_texts, os.path.join(general_path, 'train_pubmed_full.txt'))
    save_texts_to_file(val_texts, os.path.join(general_path, 'val_pubmed_full.txt'))
    save_texts_to_file(test_texts, os.path.join(general_path, 'test_pubmed_full.txt'))

if __name__ == "__main__":
    main()
