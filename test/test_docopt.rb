require "docopt"
doc = <<DOCOPT
Classbench utility
  Firewall/openflow rule generator.

Usage:
  #{__FILE__} analyse FILE [--output=FILE]
  #{__FILE__} -h | --help
  #{__FILE__} --version

Options:
  -h --help          Show this screen.
  -o --output=FILE   Output file
  --version          Show version.

DOCOPT

begin
  require "pp"
  pp Docopt::docopt(doc)
rescue Docopt::Exit => e
  puts e.message
end
