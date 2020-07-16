### PMTOKE - Paper Mario: The Origami King Editor

A script to modify PMTOK saves

**BACK UP YOUR SAVES**

You can grab your save using [JKSM](https://github.com/J-D-K/JKSM)

Usage is as follows:
```
usage: PMTOKE.py [-h] [-o OFILE] [-d] [--coins COINS] [--hp HP]
                 [--confetti CONFETTI] [--repair]
                 input

A script to modify PMTOK saves

positional arguments:
  input                 The file to read from

optional arguments:
  -h, --help            show this help message and exit
  -o OFILE, --ofile OFILE
                        The file to output to
  -d, --disable-checks  Disable initial checksum check

modifications:
  --coins COINS         The number of coins you want
  --hp HP               The max HP you want
  --confetti CONFETTI   The max confetti you want
  --repair              Repair all damaged items
```