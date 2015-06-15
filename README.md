# First-two-characters input method #

## Requirements ##
* KyTea (0.4.6)
* English Gigaword Corpus

## Setup ##
```
mkdir data
ln -s <corpus_txt> data/
```
For example,
```
mkdir data
ln -s /text/EnglishGigaword/text/nyt_eng/nyt_eng_201012.txt.gz data/
```
Next, convert it into KyTea format:
```
python convert.py data/nyt_eng_201012.txt.gz data/converted
```
Divide it into traning data and testing data:
```
head -n 100000 data/converted > data/train
tail -n 100 data/converted > data/test
```
Create raw texts for KyTea:
```
python prepare_kytea_test.py data/test > data/test.raw
```

## Run ##

### KyTea ###
Following [KyTea](http://www.phontron.com/kytea/),
```
train-kytea -full data/train -model data/model.kytea
kytea -model data/model.kytea < data/test.raw > data/pred.kytea
```

### HMM ###
```
python train.py data/train --model data/model.hmm -v
python test.py data/test --model data/model.hmm -o data/pred.hmm -v
```

## Evaluation ##
Compute F-measure by:
```
python evaluate.py data/pred.kytea --answer data/test
python evaluate.py data/pred.hmm --answer data/test
```
