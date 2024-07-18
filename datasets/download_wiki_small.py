# import datasets
# import pandas as pd
# import random
# import os

# DIV = 50

# def merge_and_shuffle(file1_path, file2_path, output_file_path):
#     """
#     Merges and shuffles contents of two files, then saves to a new file.

#     Args:
#         file1_path (str): Path to the first file.
#         file2_path (str): Path to the second file.
#         output_file_path (str): Path to the output file.
#     """
#     with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
#         merged_content = file1.readlines() + file2.readlines()
    
#     random.shuffle(merged_content)
#     with open(output_file_path, 'w') as output_file:
#         output_file.writelines(merged_content)

# def save_dataset_to_csv(dataset, output_dir, prefix):
#     """
#     Saves the train, validation, and test splits of a dataset to CSV files.

#     Args:
#         dataset (Dataset): The dataset to save.
#         output_dir (str): Directory to save the CSV files.
#         prefix (str): Prefix for the output file names.
#     """
#     os.makedirs(output_dir, exist_ok=True)
#     train = dataset.iloc[:20000]
#     val = dataset.iloc[20000:22000]
#     test = dataset.iloc[-10000:]
    
#     train.to_csv(os.path.join(output_dir, f'{prefix}_train.csv'), index=False)
#     val.to_csv(os.path.join(output_dir, f'{prefix}_val.csv'), index=False)
#     test.to_csv(os.path.join(output_dir, f'{prefix}_test.csv'), index=False)

# def main():
#     # Load and process English dataset
#     dataset = datasets.load_dataset("wikipedia", "20220301.simple")['train']
#     dataset = dataset.select(range(12000)).to_pandas()
#     save_dataset_to_csv(dataset, './wikipedia_resized/', 'wiki_eng')

#     # Process a smaller English dataset
#     small_english_dataset = dataset.iloc[:3500]
#     small_english_dataset.to_csv('wikil_eng_train.csv', index=False)

#     # Load and process Italian dataset
#     italian_dataset = datasets.load_dataset("wikipedia", "20220301.it")['train']
#     italian_dataset = italian_dataset.select(range(2000)).to_pandas()
#     save_dataset_to_csv(italian_dataset, './wikipedia_resized/', 'wiki_ita')

#     # Convert CSV to TXT
#     for csv_file in ["wiki_eng_train.csv", "wiki_eng_val.csv", "wiki_eng_test.csv", "wikil_eng_train.csv", "wiki_ita_train.csv", "wiki_ita_val.csv", "wiki_ita_test.csv"]:
#         dataset = pd.read_csv('./wikipedia_resized/' + csv_file)
#         txt_file = f"{os.path.splitext(csv_file)[0]}.txt"
#         with open(txt_file, 'w') as f:
#             for row in dataset['text'][:len(dataset)//DIV]:
#                 f.write(row + '\n')

#     # Merge and shuffle English and Italian datasets
#     merge_and_shuffle('wikil_eng_train.txt', 'wiki_ita_train.txt', './wikipedia_resized/wikil_eng_wiki_ita_train.txt')
#     merge_and_shuffle('wiki_eng_val.txt', 'wiki_ita_val.txt', './wikipedia_resized/wikil_eng_wiki_ita_val.txt')
#     merge_and_shuffle('wiki_eng_test.txt', 'wiki_ita_test.txt', './wikipedia_resized/wikil_eng_wiki_ita_test.txt')

#     # Move and clean up
#     for txt_file in ["wiki_eng_train.txt", "wiki_eng_val.txt", "wiki_eng_test.txt"]:
#         os.replace(txt_file, os.path.join('./wikipedia_resized/', txt_file))
    
#     for file in ["wiki_eng_train.csv", "wiki_eng_val.csv", "wiki_eng_test.csv", "wikil_eng_train.csv", "wikil_eng_train.txt", "wiki_ita_train.csv", "wiki_ita_val.csv", "wiki_ita_test.csv", "wiki_ita_train.txt", "wiki_ita_val.txt", "wiki_ita_test.txt"]:
#         os.remove(file)

# if __name__ == "__main__":
#     main()

import datasets
import pandas as pd
import random
import os

DIV = 20

def merge_and_shuffle(file1_path, file2_path, output_file_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        content1 = file1.readlines()
        content2 = file2.readlines()
    merged_content = content1 + content2
    random.shuffle(merged_content)

    with open(output_file_path, 'w') as output_file:
        output_file.writelines(merged_content)

def save_dataset_splits(dataset, output_dir, prefix):
    train = dataset.iloc[:15000]
    val = dataset.iloc[15000:18000]
    test = dataset.iloc[18000:20000]

    os.makedirs(output_dir, exist_ok=True)
    train.to_csv(f'{output_dir}/{prefix}_train.csv', index=False)
    val.to_csv(f'{output_dir}/{prefix}_val.csv', index=False)
    test.to_csv(f'{output_dir}/{prefix}_test.csv', index=False)

def save_small_dataset(dataset, output_file, size=3500):
    little_train = dataset.iloc[:size]
    little_train.to_csv('./wikipedia_resized/' +output_file, index=False)

def save_dataset_to_text_files(file_list, div_factor):
    for file_ in file_list:
        dataset = pd.read_csv('./wikipedia_resized/' +file_)
        output_file = f"{os.path.splitext(file_)[0]}.txt"
        with open(output_file, 'w') as f:
            for row in dataset['text'][:len(dataset) // div_factor]:
                f.write(row)

def clean_files(file_list):
    for f in file_list:
        os.remove('./wikipedia_resized/'+f)

# Load English dataset
english_dataset = datasets.load_dataset("wikipedia", "20220301.simple")['train']
english_dataset = english_dataset.select(range(20000)).to_pandas()

# Save full English dataset splits
save_dataset_splits(english_dataset, './wikipedia_resized', 'wiki_eng')

# Save little English dataset
save_small_dataset(english_dataset, 'wikil_eng_train.csv')

# Load Italian dataset
italian_dataset = datasets.load_dataset("wikipedia", "20220301.it")['train']
italian_dataset = italian_dataset.select(range(5000)).to_pandas()

# Save Italian dataset splits
save_dataset_splits(italian_dataset, './wikipedia_resized', 'wiki_ita')

# Convert CSV files to text files
csv_files = [
    "wiki_eng_train.csv", "wiki_eng_val.csv", "wiki_eng_test.csv", "wikil_eng_train.csv",
    "wiki_ita_train.csv", "wiki_ita_val.csv", "wiki_ita_test.csv"
]
save_dataset_to_text_files(csv_files, DIV)

# Merge and shuffle English and Italian datasets
merge_and_shuffle('wikil_eng_train.txt', 'wiki_ita_train.txt', './wikipedia_resized/wikil_eng_wiki_ita_train.txt')
merge_and_shuffle('wiki_eng_val.txt', 'wiki_ita_val.txt', './wikipedia_resized/wikil_eng_wiki_ita_val.txt')
merge_and_shuffle('wiki_eng_test.txt', 'wiki_ita_test.txt', './wikipedia_resized/wikil_eng_wiki_ita_test.txt')

# Move English text files to the resized folder
for split in ['train', 'val', 'test']:
    os.replace(f"wiki_eng_{split}.txt", f"./wikipedia_resized/wiki_eng_{split}.txt")

# Clean up intermediate files
clean_files(csv_files + [ "wiki_eng_train.txt", "wiki_eng_val.txt", "wiki_eng_test.txt"])
