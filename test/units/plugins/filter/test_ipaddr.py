# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.plugins.filter.ipaddr import ipaddr, _netmask_query, nthhost, next_nth_usable, previous_nth_usable


class TestNetmask(unittest.TestCase):
    def test_netmask(self):
        address = '1.1.1.1/24'
        self.assertEqual(ipaddr(address, 'netmask'), '255.255.255.0')
        address = '1.1.1.1/25'
        self.assertEqual(ipaddr(address, 'netmask'), '255.255.255.128')
        address = '1.12.1.34/32'
        self.assertEqual(ipaddr(address, 'netmask'), '255.255.255.255')

    def test_network(self):
        address = '1.12.1.34/32'
        self.assertEqual(ipaddr(address, 'network'), '1.12.1.34')
        address = '1.12.1.34/255.255.255.255'
        self.assertEqual(ipaddr(address, 'network'), '1.12.1.34')
        address = '1.12.1.34'
        self.assertEqual(ipaddr(address, 'network'), '1.12.1.34')
        address = '1.12.1.35/31'
        self.assertEqual(ipaddr(address, 'network'), '1.12.1.34')
        address = '1.12.1.34/24'
        self.assertEqual(ipaddr(address, 'network'), '1.12.1.0')

    def test_broadcast(self):
        address = '1.12.1.34/24'
        self.assertEqual(ipaddr(address, 'broadcast'), '1.12.1.255')
        address = '1.12.1.34/16'
        self.assertEqual(ipaddr(address, 'broadcast'), '1.12.255.255')
        address = '1.12.1.34/27'
        self.assertEqual(ipaddr(address, 'broadcast'), '1.12.1.63')
        address = '1.12.1.34/32'
        self.assertEqual(ipaddr(address, 'broadcast'), None)
        address = '1.12.1.35/31'
        self.assertEqual(ipaddr(address, 'broadcast'), None)

    def test_first_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.1')
        address = '1.12.1.36/24'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.1')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'first_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.33')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.33')
        address = '1.12.1.36/31'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.36')
        address = '1.12.1.37/31'
        self.assertEqual(ipaddr(address, 'first_usable'), '1.12.1.36')
        address = '1.12.1.36/32'
        self.assertEqual(ipaddr(address, 'first_usable'), None)

    def test_last_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.254')
        address = '1.12.1.36/24'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.254')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'last_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.46')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.46')
        address = '1.12.1.36/31'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.37')
        address = '1.12.1.37/31'
        self.assertEqual(ipaddr(address, 'last_usable'), '1.12.1.37')
        address = '1.12.1.36/32'
        self.assertEqual(ipaddr(address, 'last_usable'), None)

    def test_next_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(ipaddr(address, 'next_usable'), '1.12.1.1')
        address = '1.12.1.36/24'
        self.assertEqual(ipaddr(address, 'next_usable'), '1.12.1.37')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'last_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(ipaddr(address, 'next_usable'), '1.12.1.37')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(ipaddr(address, 'next_usable'), '1.12.1.37')
        address = '1.12.1.36/31'
        self.assertEqual(ipaddr(address, 'next_usable'), '1.12.1.37')
        address = '1.12.1.37/31'
        self.assertEqual(ipaddr(address, 'next_usable'), None)
        address = '1.12.1.36/32'
        self.assertEqual(ipaddr(address, 'next_usable'), None)
        address = '1.12.1.254/24'
        self.assertEqual(ipaddr(address, 'next_usable'), None)

    def test_previous_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(ipaddr(address, 'previous_usable'), None)
        address = '1.12.1.36/24'
        self.assertEqual(ipaddr(address, 'previous_usable'), '1.12.1.35')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'last_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(ipaddr(address, 'previous_usable'), '1.12.1.35')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(ipaddr(address, 'previous_usable'), '1.12.1.35')
        address = '1.12.1.36/31'
        self.assertEqual(ipaddr(address, 'previous_usable'), None)
        address = '1.12.1.37/31'
        self.assertEqual(ipaddr(address, 'previous_usable'), '1.12.1.36')
        address = '1.12.1.36/32'
        self.assertEqual(ipaddr(address, 'previous_usable'), None)
        address = '1.12.1.254/24'
        self.assertEqual(ipaddr(address, 'previous_usable'), '1.12.1.253')

    def test_next_nth_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(next_nth_usable(address, 5), '1.12.1.5')
        address = '1.12.1.36/24'
        self.assertEqual(next_nth_usable(address, 10), '1.12.1.46')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'last_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(next_nth_usable(address, 4), '1.12.1.40')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(next_nth_usable(address, 4), '1.12.1.40')
        address = '1.12.1.36/31'
        self.assertEqual(next_nth_usable(address, 1), '1.12.1.37')
        address = '1.12.1.37/31'
        self.assertEqual(next_nth_usable(address, 1), None)
        address = '1.12.1.36/32'
        self.assertEqual(next_nth_usable(address, 1), None)
        address = '1.12.1.254/24'
        self.assertEqual(next_nth_usable(address, 2), None)

    def test_previous_nth_usable(self):
        address = '1.12.1.0/24'
        self.assertEqual(previous_nth_usable(address, 5), None)
        address = '1.12.1.36/24'
        self.assertEqual(previous_nth_usable(address, 10), '1.12.1.26')
        #address = '1.12.1.34'
        #self.assertFalse(ipaddr(address, 'last_usable'), 'Not a network address')
        address = '1.12.1.36/28'
        self.assertEqual(previous_nth_usable(address, 2), '1.12.1.34')
        address = '1.12.1.36/255.255.255.240'
        self.assertEqual(previous_nth_usable(address, 2), '1.12.1.34')
        address = '1.12.1.36/31'
        self.assertEqual(previous_nth_usable(address, 1), None)
        address = '1.12.1.37/31'
        self.assertEqual(previous_nth_usable(address, 1), '1.12.1.36')
        address = '1.12.1.36/32'
        self.assertEqual(previous_nth_usable(address, 1), None)
        address = '1.12.1.254/24'
        self.assertEqual(previous_nth_usable(address, 2), '1.12.1.252')
