import jsonlines
import os
from collections import defaultdict as dd
out = dd(list)



try:
  os.mkdir('dataset/sub_data')
except OSError as error:
  print("Dir exists")
  
for typ in ["dev","test"]:
  with jsonlines.open('dataset/sub_data/clustering.{}.json'.format(typ), mode='w') as writer:  
    with jsonlines.open('dataset/og_data/clustering.{}.json'.format(typ)) as f:
      for line in f.iter():
        for j in ["Entities_all","Entities_body","Entities_title","Lemmas_all","Lemmas_body","Lemmas_title"]:
          if j in line["features"].keys():
            line["features"].pop(j)
        
        writer.write(line)

