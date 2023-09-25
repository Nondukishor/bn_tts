"""Data loader for the LJSpeech dataset. See: https://keithito.com/LJ-Speech-Dataset/"""
import os
import re
import codecs
import unicodedata
import numpy as np
from torch.utils.data import Dataset

#vocab = "PE abcdefghijklmnopqrstuvwxyz'.?"  # P: Padding, E: EOS.
vocab = "PE অআইঈউঊঋএঐওঔা ি ী ু ূ ৃ ে ৈ ো ৌক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণত থ দ ধ ন প ফ ব ভমযরলশষসহড়ঢ়য়ৎংঃঁ্ঽ‍্য‍  ‍্র'"
#vocab = "PE অআইঈউঊঋএঐওঔা ি ী ু ূ ৃ ে ৈ ো ৌক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণত থ দ ধ ন প ফ ব ভমযরলশষসহড়ঢ়য়ৎংঃঁ্ঽ‍্য‍  ‍্র'.?"
char2idx = {char: idx for idx, char in enumerate(vocab)}
idx2char = {idx: char for idx, char in enumerate(vocab)}


def text_normalize(text):
    text = ''.join(char for char in unicodedata.normalize('NFD', text)
                   if unicodedata.category(char) != 'Mn')  # Strip accents
    #print(text)
    #text = text.lower()
    text = re.sub("[^{}]()".format(vocab), " ", text)
    text = re.sub("[ ]+", " ", text)
    return text

def read_metadata(metadata_file):
    fnames, text_lengths, texts = [], [], []
    transcript = os.path.join(metadata_file)
    #transcript = "/content/drive/My Drive/TTS_B/datasets/LJSpeech-1.1/line_index.tsv"
    lines = codecs.open(transcript, 'r', 'utf-8').readlines()
    for line in lines:
        fname, text = line.strip().split("\t")

        fnames.append(fname)

        text = text_normalize(text) + "E"  # E: EOS
        text = [char2idx[char] for char in text]
        text_lengths.append(len(text))
        texts.append(np.array(text, np.float32))

    return fnames, text_lengths, texts


def get_test_data(sentences, max_n):
    normalized_sentences = [text_normalize(line).strip() + "E" for line in sentences]  # text normalization, E: EOS
    texts = np.zeros((len(normalized_sentences), max_n + 1), np.float32)
    for i, sent in enumerate(normalized_sentences):
        texts[i, :len(sent)] = [char2idx[char] for char in sent]
    return texts


class LJSpeech(Dataset):
    def __init__(self, keys, dir_name='bn_in'):
        self.keys = keys
        self.path = os.path.join("/media/nipu/works/ai/TTS_Bn/datasets", dir_name)
        self.fnames, self.text_lengths, self.texts = read_metadata(os.path.join(self.path, "line_index.tsv"))

    def slice(self, start, end):
        self.fnames = self.fnames[start:end]
        self.text_lengths = self.text_lengths[start:end]
        self.texts = self.texts[start:end]

    def __len__(self):
        return len(self.fnames)

    def __getitem__(self, index):
        data = {}
        if 'texts' in self.keys:
            data['texts'] = self.texts[index]
        if 'mels' in self.keys:
            # (39, 80)
            data['mels'] = np.load(os.path.join(self.path, 'mels', "%s.npy" % self.fnames[index]))
        if 'mags' in self.keys:
            # (39, 80)
            data['mags'] = np.load(os.path.join(self.path, 'mags', "%s.npy" % self.fnames[index]))
        if 'mel_gates' in self.keys:
            data['mel_gates'] = np.ones(data['mels'].shape[0], dtype=np.int)  # TODO: because pre processing!
        if 'mag_gates' in self.keys:
            data['mag_gates'] = np.ones(data['mags'].shape[0], dtype=np.int)  # TODO: because pre processing!
        return data
    



