% Trapdoor Hash Functions and Their Applications
% Jorge Martins, Filipe Marques
% 31 May 2020

In this project we implemented a TDH construction from the DDH in [DGI+19], from the project list. To demonstrate the applications of this constructions we implemented the Rate-1 OT protocol in section 5.3.

## Project Structure
 
```
 .
 |-- bOT.py
 |-- __init__.py
 |-- README.md
 `-- tdh_ddh.py
```

* `tdh_ddh.py` - code that contains the TDH.
* `bOT.py` - code that implements the OT protocol.

## Requirements

In this project we require the `pycrypto` python library. If not already installed use:

```sh
sudo python -m pip install pycrypto
```

## How to use

`bOT.py` takes in tree arguments as input:

* `sp` - security parameter
* `k` - number of bits in the secrets
* `n` - number of secrets

To execute with `sp=16`, `k=8`, `n=16` do:

```sh
python bOT.py 16 8 16
```
