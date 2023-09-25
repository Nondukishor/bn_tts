from datasets.lj_speech import LJSpeech
from audio import preprocess


print("pre processing...")
lj_speech = LJSpeech([])
# print(lj_speech)
# print(dataset_path, lj_speech)
preprocess("/media/nipu/works/ai/TTS_Bn/datasets/bn_in", lj_speech)