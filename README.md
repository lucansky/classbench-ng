# Classbench

Utility for generation of firewall/OpenFlow rules based on original (no longer maintained) [Classbench](http://www.arl.wustl.edu/classbench/).

## Requirements
- Ruby 1.9.3+
- RubyGems

```
gem install open4 ruby-ip docopt
```
## Installation
```
git clone git://github.com/classbench-ng/classbench-ng
make   # Downloads and compiles db_generator in ./vendor/db_generator/db_generator
```

## Usage
```
./classbench analyse FILE
```
Analyses file, expecting FILE to be ovs-ofctl dump.
Fields extracted from dump are:
- dl_dst, dl_src, dl_type, dl_vlan, dl_vlan_pcp,
- eth_type, in_port,
- nw_dst, nw_proto, nw_src, nw_tos,
- tp_dst, tp_src

Output's original Classbench seed with openflow YAML structure as last section.

```
./classbench generate v4 SEED [--count=100] [--db-generator=<path>]
```
Generates --count of OpenFlow rules.
If seed without OpenFlow section is provided, regular 5-tuples are generated.
Output format is "attribute=value", joined by ", ".

