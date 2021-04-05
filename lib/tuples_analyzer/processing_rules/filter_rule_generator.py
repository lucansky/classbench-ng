#!/usr/bin/env python
"""Module containing definition of class FilterRuleGenerator."""

from ..processing_errors.enums.Error import Error
from ..processing_errors.error_process import ErrorProcess
from .enums.filter_rule_part_location import FilterRulePartLocation
from .enums.filter_rule_part_processing_result import FilterRulePartProcessingResult
from .enums.filter_rule_part_type import FilterRulePartType
from .filter_rule import FilterRule
from .supported_values import *
import ipaddress


class FilterRuleGenerator:
    """
    Class containing only static functions for creating generator of FilterRule instances from filter set file and
    specified rule format.
    """

    @staticmethod
    def create_generator(lines_generator, rule_format, is_stderr_on):
        """
        Function creates FilterRule class instances generator from all filter rules in filter set file.
        Format of rules is needed for processing rules into instances.

        :param lines_generator: Generator of lines from file with filter rules.

        :param rule_format: String with rule format.

        :param is_stderr_on: If variable is true, printing error logs to stderr during parsing is enabled.

        :return: Generator of FilterRule instances.
        """
        format_words = FilterRuleGenerator.split_line(rule_format)
        format_length = len(format_words)
        mandatory_words_count = FilterRuleGenerator.how_many_mandatory(format_words)
        successful_yields = 0

        # going through all lines
        for line in lines_generator:

            # empty line check
            if not line:
                continue

            rule_parts = FilterRuleGenerator.split_line(line)
            filter_rule = FilterRule()

            format_position = 0
            mandatory_processed = 0
            successful_assigment = 0

            missing_mandatory = False
            standalone_question_mark = False

            # going through all parts of line
            for part in rule_parts:

                if part == '?':
                    standalone_question_mark = True
                    break

                # going through format parameters and keywords
                while format_position != format_length:

                    expected_part_type = format_words[format_position]
                    result = FilterRuleGenerator.part_processing(expected_part_type, part, filter_rule, format_words)

                    if result == FilterRulePartProcessingResult.MANDATORY_PART_PROCESSED:
                        mandatory_processed += 1

                        if expected_part_type in format_parameters:
                            successful_assigment += 1

                        format_position += 1
                        break

                    elif result == FilterRulePartProcessingResult.MANDATORY_PART_MISSING:
                        missing_mandatory = True
                        break

                    elif result == FilterRulePartProcessingResult.OPTIONAL_PART_PROCESSED:

                        if expected_part_type[:-1] in format_parameters:
                            successful_assigment += 1

                        format_position += 1
                        break

                    elif result == FilterRulePartProcessingResult.OPTIONAL_PART_MISSING:
                        format_position += 1

                # if condition is true, stop iterating through parts of filter rule
                if format_position == format_length or missing_mandatory:
                    break

            # processing errors or yielding instance of FilterRule class
            if (missing_mandatory or mandatory_processed != mandatory_words_count or successful_assigment == 0
                or standalone_question_mark) and not is_stderr_on:
                pass

            elif missing_mandatory:
                ErrorProcess.print_warning(f'Mandatory part: \'{expected_part_type}\' was expected '
                                           f'instead of: \'{str(FilterRuleGenerator.get_type(part, format_words).name)}'
                                           f': {part}\', following rule is ignored: \'{line}\'.')

            elif mandatory_processed != mandatory_words_count:
                ErrorProcess.print_warning(f'Not all mandatory parts of rule have been processed, '
                                           f'following rule is ignored: \'{line}\'.')

            elif successful_assigment == 0:
                ErrorProcess.print_warning(f'Rule has not valuable content, '
                                           f'following rule is ignored: \'{line}\'.')

            elif standalone_question_mark:
                ErrorProcess.print_warning(f'Character \'?\' can not be standalone part of rule, '
                                           f'following rule is ignored: \'{line}\'.')

            else:
                successful_yields += 1
                yield filter_rule

        if successful_yields == 0:
            ErrorProcess.process_error(Error.NO_VALUE_FILTER_SET_ERROR)

    @staticmethod
    def part_processing(expected_part_type, part, filter_rule, format_words):
        """
        If expected part (from format) matches with real part (from filter rule line), function sets one of attributes
        in FilterRule instance to value of part and returns enum telling that mandatory or optional part was
        processed. If mandatory or optional part is missing, function returns corresponding enum.

        :param expected_part_type: Parameter or keyword from rule format file.

        :param part: Part from filter rule line.

        :param filter_rule: Instance of FilterRule class.

        :param format_words: List with all format words.

        :return: Result type of processing filter rule part.
        """
        part_type = FilterRuleGenerator.get_type(part, format_words)

        if part_type == FilterRulePartType.ANY:
            part = "any"

        if part_type == FilterRulePartType.IPV4_ADDRESS:
            part += '/32'

        if part_type == FilterRulePartType.IPV6_ADDRESS:
            part += '/128'

        if ((expected_part_type == "PROTOCOL" or expected_part_type == "PROTOCOL?") and
                (part_type == FilterRulePartType.ANY or part_type == FilterRulePartType.PROTOCOL)):

            filter_rule.set_protocol_number(part)

        elif ((expected_part_type == "PROTOCOL" or expected_part_type == "PROTOCOL?") and
              (part.isdigit() and int(part) in [e.value for e in Protocol])):

            filter_rule.set_protocol_number(Protocol(int(part)).name.lower())

        elif ((expected_part_type == "SRC_PORT" or expected_part_type == "SRC_PORT?") and
              (part_type == FilterRulePartType.ANY or part_type == FilterRulePartType.PORT or
               part_type == FilterRulePartType.PORT_RANGE)):

            filter_rule.set_port(part, FilterRulePartLocation.SOURCE)

        elif ((expected_part_type == "DST_PORT" or expected_part_type == "DST_PORT?") and
              (part_type == FilterRulePartType.ANY or part_type == FilterRulePartType.PORT or
               part_type == FilterRulePartType.PORT_RANGE)):

            filter_rule.set_port(part, FilterRulePartLocation.DESTINATION)

        elif ((expected_part_type == "SRC_IP" or expected_part_type == "SRC_IP?") and
              (part_type == FilterRulePartType.ANY or part_type == FilterRulePartType.IPV4_ADDRESS_MASK
               or part_type == FilterRulePartType.IPV6_ADDRESS or part_type == FilterRulePartType.IPV6_ADDRESS_MASK
               or part_type == FilterRulePartType.IPV4_ADDRESS)):

            is_ipv6 = part_type == FilterRulePartType.IPV6_ADDRESS or part_type == FilterRulePartType.IPV6_ADDRESS_MASK
            filter_rule.set_ip_add(part, FilterRulePartLocation.SOURCE, is_ipv6)

        elif ((expected_part_type == "DST_IP" or expected_part_type == "DST_IP?") and
              (part_type == FilterRulePartType.ANY or part_type == FilterRulePartType.IPV4_ADDRESS_MASK
               or part_type == FilterRulePartType.IPV6_ADDRESS or part_type == FilterRulePartType.IPV6_ADDRESS_MASK
               or part_type == FilterRulePartType.IPV4_ADDRESS)):

            is_ipv6 = part_type == FilterRulePartType.IPV6_ADDRESS or part_type == FilterRulePartType.IPV6_ADDRESS_MASK
            filter_rule.set_ip_add(part, FilterRulePartLocation.DESTINATION, is_ipv6)

        elif ((expected_part_type == "NUMBER" or expected_part_type == "NUMBER?") and
              (part_type == FilterRulePartType.NUMBER or part_type == FilterRulePartType.PORT)):
            pass

        elif ((expected_part_type == "WILDCARD" or expected_part_type == "WILDCARD?") and
              (part_type == FilterRulePartType.WORD)):
            pass

        elif ((expected_part_type == part or expected_part_type == part + '?') and
              part_type == FilterRulePartType.KEYWORD):
            pass

        elif FilterRuleGenerator.is_word_mandatory(expected_part_type):
            return FilterRulePartProcessingResult.MANDATORY_PART_MISSING

        else:
            return FilterRulePartProcessingResult.OPTIONAL_PART_MISSING

        if FilterRuleGenerator.is_word_mandatory(expected_part_type):
            return FilterRulePartProcessingResult.MANDATORY_PART_PROCESSED

        else:
            return FilterRulePartProcessingResult.OPTIONAL_PART_PROCESSED

    @staticmethod
    def how_many_mandatory(rule_format):
        """
        Function counts how many words are mandatory in rule format definition.

        :param rule_format: String with rule format.

        :return: Count of mandatory words in format.
        """
        count = 0
        for part in rule_format:
            if FilterRuleGenerator.is_word_mandatory(part):
                count = count + 1
        return count

    @staticmethod
    def is_word_mandatory(word):
        """
        Every parameter or keyword in format is holding information, if part in filter rule is mandatory or optional.
        Part is optional, if its definition in format ends with character '?', otherwise part is mandatory.

        :param word: Parameter or keyword from format.

        :return: Function returns true, if parameter word ends with '?'.
        """
        string_length = len(word)

        if word[string_length - 1] != '?':
            return True
        else:
            return False

    @staticmethod
    def get_type(part, format_words):
        """
        Function determines type of part of filter rule. Decision is made by acceptable format of part.
        E.g. function knows it is a port, if part of rule is number between 0-65535.

        :param part: String with filter rule part.

        :param format_words: List with all format words.

        :return: Type of filter rule part.
        """
        if FilterRuleGenerator.is_wildcard(part):
            return FilterRulePartType.ANY

        elif FilterRuleGenerator.is_protocol(part):
            return FilterRulePartType.PROTOCOL

        elif FilterRuleGenerator.is_ipv4_address(part):
            return FilterRulePartType.IPV4_ADDRESS

        elif FilterRuleGenerator.is_ipv4_address_with_mask(part):
            return FilterRulePartType.IPV4_ADDRESS_MASK

        elif FilterRuleGenerator.is_ipv6_address(part):
            return FilterRulePartType.IPV6_ADDRESS

        elif FilterRuleGenerator.is_ipv6_address_with_mask(part):
            return FilterRulePartType.IPV6_ADDRESS_MASK

        elif FilterRuleGenerator.is_port(part):
            return FilterRulePartType.PORT

        elif part.isdigit():
            return FilterRulePartType.NUMBER

        elif FilterRuleGenerator.is_port_range(part):
            return FilterRulePartType.PORT_RANGE

        elif FilterRuleGenerator.is_keyword(part, format_words):
            return FilterRulePartType.KEYWORD

        else:
            return FilterRulePartType.WORD

    @staticmethod
    def is_wildcard(value):
        """
        Function returns true, if parameter value is wildcard.

        :param value: String with possible wildcard.

        :return: True, if parameter is representation of wildcard, otherwise false.
        """

        if not isinstance(value, str):
            return False

        value = value.lower()

        if value in supported_wildcard_list:
            return True
        else:
            return False

    @staticmethod
    def is_protocol(protocol):
        """
        Function returns true, if parameter is network protocol abbreviation (TCP, UDP, ip, ...).

        :param protocol: String with possible network protocol abbreviation.

        :return: True, if parameter is network protocol abbreviation, otherwise false.
        """
        if not isinstance(protocol, str):
            return False

        case_insensitive_protocol = protocol.lower()

        if case_insensitive_protocol in supported_protocols:
            return True
        else:
            return False

    @staticmethod
    def is_port(port):
        """
        Function finds out, if parameter is port (number between 0-65535).

        :param port: String with possible port.

        :return: Function returns true, if parameter of function is port.
        """
        if port.isdigit() and 0 <= int(port) < 65536:
            return True
        else:
            return False

    @staticmethod
    def is_port_range(port_range):
        """
        Function finds out, if parameter is port range (two ports with ':'as delimiter).

        :param port_range: String with possible port range.

        :return: Function returns true, if parameter of function is port range.
        """
        port_range = port_range.split(':')

        if (len(port_range) == 2 and
                FilterRuleGenerator.is_port(port_range[0]) and
                FilterRuleGenerator.is_port(port_range[1]) and
                int(port_range[0]) < int(port_range[1])):
            return True
        else:
            return False

    @staticmethod
    def is_keyword(keyword, format_words):
        """
        Function finds out, if parameter keyword is part of rule format definition.

        :param keyword: String with possible keyword.

        :param format_words: List with all format words.

        :return: True, if parameter of function is keyword in format.
        """
        if keyword in format_words or keyword + '?' in format_words:
            return True
        else:
            return False

    @staticmethod
    def is_ipv4_address(ip_address):
        """
        Function returns true, if parameter of function is IPv4 address in decimal form without mask (prefix length).

        :param ip_address: String with possible IPv4 address in decimal form.

        :return: True, if parameter of function is IPv4 address.
        """
        try:
            ipaddress.IPv4Address(ip_address)
        except ipaddress.AddressValueError:
            return False

        return True

    @staticmethod
    def is_ipv4_address_with_mask(ip_address):
        """
        Function returns true, if parameter of function is IPv4 address in decimal form with mask (prefix length).

        :param ip_address: String with possible IPv4 address with mask in decimal form.

        :return: True, if parameter of function is IPv4 address with mask.
        """
        possible_address = ip_address.split('/')

        if len(possible_address) != 2 or not possible_address[1].isdigit() or int(possible_address[1]) < 0 or int(
                possible_address[1]) > 32 or not FilterRuleGenerator.is_ipv4_address(possible_address[0]):
            return False

        return True


    @staticmethod
    def is_ipv6_address(ip_address):
        """
        Function returns true, if parameter of function is IPv6 address without mask (prefix length).

        :param ip_address: String with possible IPv6 address.

        :return: True, if parameter of function is IPv6 address.
        """
        try:
            ipaddress.IPv6Address(ip_address)
        except ipaddress.AddressValueError:
            return False

        return True

    @staticmethod
    def is_ipv6_address_with_mask(ip_address):
        """
        Function returns true, if parameter of function is IPv6 address with mask (prefix length).

        :param ip_address: String with possible IPv6 address with mask.

        :return: True, if parameter of function is IPv6 address with mask.
        """
        possible_address = ip_address.split('/')

        if len(possible_address) != 2 or not possible_address[1].isdigit() or int(possible_address[1]) < 0 or int(
                possible_address[1]) > 128 or not FilterRuleGenerator.is_ipv6_address(possible_address[0]):
            return False

        return True

    @staticmethod
    def split_line(line):
        """
        Function firstly replaces line characters  ',' and '=' with empty space. Then split the line by whitespace
        into parts and returns list with splitted parts from line.

        :param line: String which will be splitted to parts.

        :return: List with splitted parts by whitespace from line.
        """
        line = line.replace("=", " ")
        line = line.replace(",", " ")
        return line.split()
