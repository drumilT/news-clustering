from sklearn.feature_extraction.text import TfidfVectorizer

import json
import os
import jsonlines

try:
  os.mkdir('dataset/sub_data2')
except OSError as error:
  print("Dir exists")

with open('dataset/og_data/dataset.dev.json') as f:
    data = json.load(f)

out = []
for i in data:
    if i["lang"] =="eng":
        out.append(i)

train_corpus = [i["text"] for i in out]
vectorizer = TfidfVectorizer()
vectorizer = vectorizer.fit(train_corpus)
print("Fit Complete")
print(len(vectorizer.vocabulary_))
for typ in ["test","dev"]:
    counter= 0
    with open('dataset/og_data/dataset.{}.json'.format(typ)) as f:
        data = json.load(f)
    out = []
    for i in data:
        if i["lang"] =="eng":
            out.append(i)
    corpus = [i["text"] for i in out]
    Y = vectorizer.transform(corpus)
    print("Transformed {}".format(typ))
    print(Y.shape)
    print(len(out))
    with jsonlines.open('dataset/sub_data2/clustering.{}.json'.format(typ), mode='w') as writer:
        for a,b in zip(out,Y):
            line = dict({"ci":counter,"features":{"Tokens_all":dict({})},"id":a["id"],"timestamp":a["date"].replace(" ","T").replace(":","")+".000000"})
            counter+=1
            #print(b.shape)
            for word in a["text"].split():
                if word in vectorizer.vocabulary_.keys():
                    line["features"]["Tokens_all"]["t_"+word]=b.toarray()[0][vectorizer.vocabulary_[word]]

            writer.write(line)
    with open('dataset/sub_data2/dataset.{}.json'.format(typ), 'w') as json_file:
        json.dump(out, json_file,indent=4)