# ClassBench-ng
A tool for generation of synthetic classification rule sets for benchmarking, which is based on original (no longer maintained) [ClassBench](http://www.arl.wustl.edu/classbench/).
The format of the generated rules can be one of the following:
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
make   # Downloads, patches and compiles original ClassBench in ./vendor/db_generator
       # Downloads the parameter files of original ClassBench to ./vendor/parameter_files
```

### Patching ClassBench
Original ClassBench is improved using patches in `./patches` directory and the size of its statically initialized arrays is increased, where necessary.
These changes are automatically applied on downloaded original ClassBench during ClassBench-ng installation (see `./vendor/Makefile`).

## Usage
```
./classbench analyse FILE
```
Analyses FILE, expecting FILE to be in the format used by `ovs-ofctl`.
Fields extracted from FILE are:
- in_port,
- dl_src, dl_dst, eth_type, dl_vlan, dl_vlan_pcp,
- nw_src, nw_dst, nw_tos, nw_proto,
- tp_src, tp_dst

The output is an original ClassBench seed with an OpenFlow YAML structure as the last section.

```
./classbench generate v4 SEED [--count=<n>] [--db-generator=<path>]
```
Generates IPv4 5-tuples following the properties from SEED.
- `--count=<n>` specifies the number of 5-tuples to be generated (default: `100`)
- `--db-generator=<path>` specifies the path to an original ClassBench binary (default: `./vendor/db_generator/db_generator`)

The output format is the same as of original ClassBench outputs.

```
./classbench generate v6 SEED [--count=<n>] [--db-generator=<path>]
```
Generates IPv6 5-tuples following the properties from SEED.
- `--count=<n>` specifies the number of 5-tuples to be generated (default: `100`)
- `--db-generator=<path>` specifies the path to an original ClassBench binary (default: `./vendor/db_generator/db_generator`)

The output format is the same as of original ClassBench outputs.

```
./classbench generate of SEED [--count=<n>] [--db-generator=<path>]
```
Generates OpenFlow rules following the properties from SEED that has to contain an OpenFlow section.
- `--count=<n>` specifies the number of rules to be generated (default: `100`)
- `--db-generator=<path>` specifies the path to an original ClassBench binary (default: `./vendor/db_generator/db_generator`)

The output consists of `attribute=value` pairs joined by `, `.

```
./classbench -h | --help
```
Prints deatiled usage information.
