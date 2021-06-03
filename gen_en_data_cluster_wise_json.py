import json
import os

try:
  os.mkdir('dataset/en_data')
except OSError as error:
  print("Dir exists")

for typ in ["test","dev"]:
  with open('dataset/og_data/dataset.{}.json'.format(typ)) as f:
    data = json.load(f)

  from collections import defaultdict as dd
  out = dd(list)
  for i in data:
      if i["lang"] =="eng":
          out[i["cluster"]].append(i)

  with open('dataset/en_data/dataset.{}.json'.format(typ), 'w') as json_file:
    json.dump(out, json_file,indent=4, sort_keys=True)


