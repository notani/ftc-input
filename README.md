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

# Example #

## Input ##
First two characters are input to the HMM model.
```
An/Analysts/blank ha/have/blank be/been/blank sa/saying/blank fo/for/blank mo/months/blank th/that/blank th/they/blank ex/expect/blank Ch/China/blank to/to/blank ra/raise/blank in/interest/blank ra/rates/blank th/throughout/blank 20/2011./blank
```

## Output ##
```
An/Analysts/blank ha/have/blank be/been/blank sa/sacked/blank fo/for/blank mo/more/blank th/than/blank th/the/blank ex/extensive/blank Ch/Chinese/blank to/to/blank ra/raise/blank in/interest/blank ra/rate/blank th/through/blank 20/2020./blank
```
The words in the center are predictions by the HMM model.
