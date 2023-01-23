# lot_2_report
Scripts per revisió arxius Lote 2 (NER+EL)

# Usage


```
python review_annotations.py --help
Usage: review_annotations.py [options]

Options:
  -h, --help            show this help message and exit
  -f INPUTFILE, --filetoprocess=INPUTFILE
                        input file with annotations
  -r REPORT, --report=REPORT
                        name for basic stats report and prodigy files
  -s SEARCH, --search=SEARCH
                        Search types, mentions or elinks
                        
```

## Examples

```
python review_annotations.py -f ../entregas/Lote2-Pilot_annotations_output.json - pilot_report
```

Generates a report named pilot_report.txt, in addition to files to review annotations in Prodigy:

```
prodigy ner.manual test_pilot blank:ca pilot4prodigy.json -l labels.txt -C

```
Report includes basic statistics and  most common types and Q codes, as well as incosistencies detected when a QCode receives different types

An example report is included

Also: it extracts a random sample of 10% of the documents and creates the two documents needed to review them using Prodigy:



```
prodigy ner.manual test_pilot blank:ca pilot4prodigy.json -l labels.txt -C
```

## Search types, Mentions or Q codes in Annotations:

```
python review_annotations.py -f ../entregas/Lote2-Pilot_annotations_output.json -s 1
What do you want to search?


(T) Type
(M) mention
(Q)Qcode
(any other) Exit
>> T
Which type? building-shops
Montserrat Úbeda i Pla és una llibretera i activista cultural catalana. Va treballar a la Llibreria Ona, que va estar en funcionament entre 1962 i 2010 i la va dirigir durant els darrers deu anys que va 
building-shops
 la llengua catalanes. Per la seva incansable tasca com a prescriptora cultural, duta a terme des d'Ona Llibres, llibreria especialitzada en llibres en català".
building-shops
 Aquest darrer, és una una altra zona comercial especialitzada en subcultura situada a les antigues galeries Maldà al barri Gòtic de Barcelona. Les botigues temàtiques que formen el Triangle màgic ofereixen sovint 
building-shops
Ocurrences:  3

```

