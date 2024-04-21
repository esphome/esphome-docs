from os.path import join, dirname
import re

embedding_path = join(dirname(__file__), "glove-25d-reduced.txt")

embeddings = {}
for line in open(embedding_path, "r"):
    w, idf, *values = line.split(" ")
    embeddings[w] = (float(idf), [float(x) for x in values])

def tokenize(string):
    string = string.lower()
    string = re.sub(r"\n", " ", string)
    string = re.sub(r"\, ", " , ", string)
    string = re.sub(r"\. ", " . ", string)
    string = re.sub(r"['’] ", " ' ", string)
    string = re.sub(r"[\"“”] ", " '' ", string)
    string = string.replace("²", "2").replace("b-parasite", "b parasite").replace("nfc/rfid", "nfc rfid").replace("fastled", "fast led").replace("neopixelbus", "neopixel bus").replace("neopixel", "neo pixel").replace("h-bridge", "h bridge").replace("rgbw", "rgb white").replace("rgbww", "rgb cold warm").replace("rgbct", "rgb temperature brightness").replace("cannot", "can not").replace("addressable", "addressed")
    string = re.sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " <number> ", string)
    string = re.sub(r"\s+", " ", string)
    return string.strip().split(" ")

def embed(tokens):
    output = [0] * 25
    total = 0
    for token in tokens:
        if token not in embeddings:
            continue
        idf, values = embeddings[token]

        for i in range(len(values)):
            output[i] += values[i] * idf
        total += idf
    
    if total == 0:
        return None
    return [round(x / total, 4) for x in output]
