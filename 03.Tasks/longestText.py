#!/bin/python
import argparse
import pandas as pd

def find_longest_text_line(file_path):
    dataset = pd.read_csv(file_path, sep='\t', encoding='utf-8')
    max_length = dataset['text'].str.len().max()
    longest_line = dataset.loc[dataset['text'].str.len() == max_length, 'text'].values[0]
    num_words = len(longest_line.split())
    print("The longest line in the 'text' column is:")
    print(len(longest_line))
    print("Number of words in the longest line:", num_words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find the longest line in the text column of a CSV file.')
    parser.add_argument('file', type=str, help='Path to the CSV file')
    args = parser.parse_args()

    find_longest_text_line(args.file)

