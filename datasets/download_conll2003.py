import wget
import os

def download_files(urls, output_dir):
    """
    Downloads files from given URLs to the specified directory.

    Args:
        urls (list): List of URLs to download.
        output_dir (str): Directory to save the downloaded files.
    """
    os.makedirs(output_dir, exist_ok=True)
    for url in urls:
        file_name = os.path.basename(url)
        wget.download(url, os.path.join(output_dir, file_name))

# Define URLs and output directory
conll2003_urls = [
    "https://raw.githubusercontent.com/chnsh/BERT-NER-CoNLL/master/data/train.txt",
    "https://raw.githubusercontent.com/chnsh/BERT-NER-CoNLL/master/data/valid.txt",
    "https://raw.githubusercontent.com/chnsh/BERT-NER-CoNLL/master/data/valid.txt",  # Download as dev.txt
    "https://raw.githubusercontent.com/chnsh/BERT-NER-CoNLL/master/data/test.txt"
]
output_dir = "./datasets/CoNLL2003/"

# Process each file
download_files(conll2003_urls, output_dir)
