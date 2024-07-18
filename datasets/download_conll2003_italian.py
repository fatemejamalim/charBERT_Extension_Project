import wget
import os

def download_and_convert_conllu_to_txt(conllu_url, output_dir, n_stop=100_000):
    """
    Downloads a .conllu file, converts it to .txt, and saves it.

    Args:
        conllu_url (str): URL of the .conllu file.
        output_dir (str): Directory to save the converted .txt file.
        n_stop (int): Maximum number of lines to process.
    """
    file_name = conllu_url.split("/")[-1]
    conllu_file = wget.download(conllu_url, file_name)
    txt_file_path = os.path.join(output_dir, file_name.replace(".conllu", ".txt"))

    os.makedirs(output_dir, exist_ok=True)
    with open(conllu_file, 'r', encoding='utf-8') as f_in, open(txt_file_path, 'w') as f_out:
        for i, line in enumerate(f_in):
            if i >= n_stop:
                break
            parts = line.split("\t")
            if len(parts) == 3:
                if line.startswith('0'):
                    f_out.write("\n")
                token = parts[1]
                tag = parts[2]
                f_out.write(f"{token} {tag}")

    os.remove(conllu_file)

# Define URLs and output directory
conllu_urls = [
    "https://raw.githubusercontent.com/Babelscape/wikineural/master/data/wikineural/it/train.conllu",
    "https://raw.githubusercontent.com/Babelscape/wikineural/master/data/wikineural/it/val.conllu",
    "https://raw.githubusercontent.com/Babelscape/wikineural/master/data/wikineural/it/test.conllu"
]
output_dir = "./CoNLL2003_ita/"

# Process each file
for url in conllu_urls:
    download_and_convert_conllu_to_txt(url, output_dir, n_stop=200_000 if 'train' in url else 100_000)
