# ClassBench-ng
A tool for generation of synthetic classification rule sets for benchmarking, which is based on original (no longer maintained) [ClassBench](http://www.arl.wustl.edu/classbench/).
Format of the generated rules can be one of the following:
- IPv4 5-tuple
- IPv6 5-tuple
- OpenFlow

## Requirements
- Ruby 1.9.3+
- RubyGems
```
sudo gem install open4 ruby-ip docopt ipaddress
```
## Installation
```
git clone https://github.com/classbench-ng/classbench-ng.git
make   # Downloads, patches and compiles db_generator in ./vendor/db_generator
```

### Patching ClassBench
Original ClassBench is improved using patches in `./patches` directory and the size of its statically initialized arrays is increased, where necessary.
These changes are automatically applied on downloaded ClassBench during ClassBench-ng installation (see `./vendor/Makefile`).

## Usage
```
./classbench analyse FILE
```
Analyses FILE, expecting FILE to be in the format used by `ovs-ofctl`.
Fields extracted from FILE are:
- in_port
- dl_src, dl_dst, eth_type, dl_vlan, dl_vlan_pcp
- nw_src, nw_dst, nw_tos, nw_proto,
- tp_src, tp_dst

The output is an original ClassBench seed with an OpenFlow YAML structure as the last section.

```
./classbench generate v4 SEED [--count=<n>] [--db-generator=<path>]
```
Generates IPv4 5-tuples or OpenFlow rules following properties from SEED.
OpenFlow rules are generated only if SEED contains OpenFlow section.
- `--count=<n>` specifies the number of generated 5-tuples/rules (default: `100`)
- `--db-generator=<path>` specifies path to a ClassBench binary (default: `./vendor/db_generator/db_generator`)

The output consists of `attribute=value` pairs joined by `, `.

```
./classbench generate v6 <seed> [--count=<n>]
```
Generates IPv6 5-tuples rules following properties from SEED.
- `--count=<n>` specifies the number of generated 5-tuples (default: `100`)

The output consists of `attribute=value` pairs joined by `, `.

```
./classbench -h | --help
```
Prints deatiled usage information.
