#!/usr/bin/env python
"""Module containing definition of class FilterRule."""

from .enums.filter_rule_part_location import FilterRulePartLocation
from .enums.port_class import PC
from .enums.port_pair_class import PPC
from .enums.protocol_numbers import Protocol
import ipaddress


class FilterRule:
    """
    Class representing filter rule.
    """

    def __init__(self):
        """
        Constructor initialize all filter rule attributes with wildcard values.
        """
        self.protocol = Protocol.ANY
        """Protocol number defined by IANA."""
        self.src_port_class = PC.WC
        """Source port class."""
        self.src_port = None
        """Source port value."""
        self.dst_port_class = PC.WC
        """Destination port class."""
        self.dst_port = None
        """Destination port value."""
        self.src_ip_add_bin = '*'
        """Source IP address in binary form."""
        self.src_ip_add_prefix_length = 0
        """Source IP address prefix length."""
        self.dst_ip_add_bin = '*'
        """Destination IP address in binary form."""
        self.dst_ip_add_prefix_length = 0
        """Destination IP address prefix length."""

    def get_ppc_class(self):
        """
        Function returns enum value representing port pair class (PPC) of this filter rule.

        :return:  Enum value representing PPC of this filter rule.
        """
        if self.src_port_class == PC.WC and self.dst_port_class == PC.WC:
            return PPC.WC_WC

        elif self.src_port_class == PC.WC and self.dst_port_class == PC.HI:
            return PPC.WC_HI

        elif self.src_port_class == PC.HI and self.dst_port_class == PC.WC:
            return PPC.HI_WC

        elif self.src_port_class == PC.HI and self.dst_port_class == PC.HI:
            return PPC.HI_HI

        elif self.src_port_class == PC.WC and self.dst_port_class == PC.LO:
            return PPC.WC_LO

        elif self.src_port_class == PC.LO and self.dst_port_class == PC.WC:
            return PPC.LO_WC

        elif self.src_port_class == PC.HI and self.dst_port_class == PC.LO:
            return PPC.HI_LO

        elif self.src_port_class == PC.LO and self.dst_port_class == PC.HI:
            return PPC.LO_HI

        elif self.src_port_class == PC.LO and self.dst_port_class == PC.LO:
            return PPC.LO_LO

        elif self.src_port_class == PC.WC and self.dst_port_class == PC.AR:
            return PPC.WC_AR

        elif self.src_port_class == PC.AR and self.dst_port_class == PC.WC:
            return PPC.AR_WC

        elif self.src_port_class == PC.HI and self.dst_port_class == PC.AR:
            return PPC.HI_AR

        elif self.src_port_class == PC.AR and self.dst_port_class == PC.HI:
            return PPC.AR_HI

        elif self.src_port_class == PC.WC and self.dst_port_class == PC.EM:
            return PPC.WC_EM

        elif self.src_port_class == PC.EM and self.dst_port_class == PC.WC:
            return PPC.EM_WC

        elif self.src_port_class == PC.HI and self.dst_port_class == PC.EM:
            return PPC.HI_EM

        elif self.src_port_class == PC.EM and self.dst_port_class == PC.HI:
            return PPC.EM_HI

        elif self.src_port_class == PC.LO and self.dst_port_class == PC.AR:
            return PPC.LO_AR

        elif self.src_port_class == PC.AR and self.dst_port_class == PC.LO:
            return PPC.AR_LO

        elif self.src_port_class == PC.LO and self.dst_port_class == PC.EM:
            return PPC.LO_EM

        elif self.src_port_class == PC.EM and self.dst_port_class == PC.LO:
            return PPC.EM_LO

        elif self.src_port_class == PC.AR and self.dst_port_class == PC.AR:
            return PPC.AR_AR

        elif self.src_port_class == PC.AR and self.dst_port_class == PC.EM:
            return PPC.AR_EM

        elif self.src_port_class == PC.EM and self.dst_port_class == PC.AR:
            return PPC.EM_AR

        elif self.src_port_class == PC.EM and self.dst_port_class == PC.EM:
            return PPC.EM_EM

    def set_protocol_number(self, protocol):
        """
        Function takes network protocol abbreviation as parameter and sets instance variable protocol_number as
        enum value of that protocol.

        :param protocol: Network protocol abbreviation.
        """
        if protocol == 'any':
            self.protocol = Protocol.ANY

        elif protocol == 'tcp':
            self.protocol = Protocol.TCP

        elif protocol == 'udp':
            self.protocol = Protocol.UDP

        elif protocol == 'icmp':
            self.protocol = Protocol.ICMP

        elif protocol == 'igmp':
            self.protocol = Protocol.IGMP

        elif protocol == 'ggp':
            self.protocol = Protocol.GGP

        elif protocol == 'st':
            self.protocol = Protocol.ST

        elif protocol == 'egp':
            self.protocol = Protocol.EGP

        elif protocol == 'gre':
            self.protocol = Protocol.GRE

        elif protocol == 'esp':
            self.protocol = Protocol.ESP

        elif protocol == 'ah':
            self.protocol = Protocol.AH

        elif protocol == 'eigrp':
            self.protocol = Protocol.EIGRP

        elif protocol == 'ospfigp':
            self.protocol = Protocol.OSPFIGP

    def set_port(self, port, location):
        """
        Function takes port value as parameter and sets instance variables source or destination port and port_class
        with parameter value and port class of parameter.

        :param port: Port or port range value.

        :param location: Location of port or port range value (source/destination).
        """
        if location == FilterRulePartLocation.SOURCE:
            if port == 'any':
                self.src_port_class = PC.WC
            elif port == '0:1023':
                self.src_port = port
                self.src_port_class = PC.LO
            elif port == '1024:65535':
                self.src_port = port
                self.src_port_class = PC.HI
            elif len(port.split(':')) == 2:
                self.src_port = port
                self.src_port_class = PC.AR
            else:
                self.src_port = port + ':' + port
                self.src_port_class = PC.EM

        elif location == FilterRulePartLocation.DESTINATION:
            if port == 'any':
                self.dst_port_class = PC.WC
            elif port == '0:1023':
                self.dst_port = port
                self.dst_port_class = PC.LO
            elif port == '1024:65535':
                self.dst_port = port
                self.dst_port_class = PC.HI
            elif len(port.split(':')) == 2:
                self.dst_port = port
                self.dst_port_class = PC.AR
            else:
                self.dst_port = port + ':' + port
                self.dst_port_class = PC.EM

    def set_ip_add(self, ip_address, location, is_ipv6):
        """
        Function takes parameter ip address and sets instance variable source or destination ip_add_bin
        as binary form of that ip address. It also sets instance variable source or destination ip_add_prefix_length
        with ip address prefix length.

        :param ip_address: Ip address with prefix length.

        :param location: Location of ip address (source/destination).

        :param is_ipv6: True, if it is IPv6 address.
        """
        if location == FilterRulePartLocation.SOURCE:
            if ip_address == 'any':
                self.src_ip_add_bin = '*'
                self.src_ip_add_prefix_length = 0
            else:
                ip_address = ip_address.split('/')
                prefix_length = int(ip_address[1])
                self.src_ip_add_prefix_length = prefix_length

                if not is_ipv6:
                    bin_ip_address = bin(int(ipaddress.IPv4Address(ip_address[0])))
                    bin_ip_address = bin_ip_address[2:].zfill(32)
                else:
                    bin_ip_address = bin(int(ipaddress.IPv6Address(ip_address[0])))
                    bin_ip_address = bin_ip_address[2:].zfill(128)

                binary_ip_address_cut = bin_ip_address[:prefix_length]
                self.src_ip_add_bin = binary_ip_address_cut

        elif location == FilterRulePartLocation.DESTINATION:
            if ip_address == 'any':
                self.dst_ip_add_bin = '*'
                self.dst_ip_add_prefix_length = 0
            else:
                ip_address = ip_address.split('/')
                prefix_length = int(ip_address[1])
                self.dst_ip_add_prefix_length = prefix_length

                if not is_ipv6:
                    bin_ip_address = bin(int(ipaddress.IPv4Address(ip_address[0])))
                    bin_ip_address = bin_ip_address[2:].zfill(32)
                else:
                    bin_ip_address = bin(int(ipaddress.IPv6Address(ip_address[0])))
                    bin_ip_address = bin_ip_address[2:].zfill(128)

                binary_ip_address_cut = bin_ip_address[:prefix_length]
                self.dst_ip_add_bin = binary_ip_address_cut
