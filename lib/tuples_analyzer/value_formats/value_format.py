#!/usr/bin/env python
"""Module containing definition of class Format."""


class Format:
    """
    Class contains functions for formatting different types of values to specified form.
    """

    @staticmethod
    def decimal(decimal_value):
        """
        Function formats decimal value to form with 8 decimal numbers.

        :param decimal_value: Decimal value.

        :return: Decimal value with 8 decimal numbers.
        """
        return format(decimal_value, '.8f')
