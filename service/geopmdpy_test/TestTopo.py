#!/usr/bin/env python3
#
#  Copyright (c) 2015 - 2022, Intel Corporation
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#
#      * Neither the name of Intel Corporation nor the names of its
#        contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY LOG OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import absolute_import

import unittest
from importlib import reload
from geopmdpy import topo
from geopmdpy import gffi

class TestTopo(unittest.TestCase):
    def setUp(self):
        reload(gffi)
        reload(topo) # Ensures that the mocked dlopen call does not leak into this test

    def test_num_domain(self):
        num_cpu_str = topo.num_domain("cpu")
        self.assertLess(0, num_cpu_str)
        num_cpu_int = topo.num_domain(topo.DOMAIN_CPU)
        self.assertEqual(num_cpu_str, num_cpu_int)

    def test_domain_domain_nested(self):
        num_cpu = topo.num_domain("cpu")
        num_pkg = topo.num_domain("package")
        pkg_cpu_map = [[] for pkg_idx in range(num_pkg)]
        for cpu_idx in range(num_cpu):
            pkg_idx_str = topo.domain_idx("package", cpu_idx)
            pkg_idx_int = topo.domain_idx(topo.DOMAIN_PACKAGE, cpu_idx)
            self.assertEqual(pkg_idx_int, pkg_idx_str)
            pkg_cpu_map[pkg_idx_str].append(cpu_idx)
        for pkg_idx in range(num_pkg):
            self.assertEqual(pkg_cpu_map[pkg_idx], topo.domain_nested('cpu', 'package', pkg_idx))
            self.assertEqual(pkg_cpu_map[pkg_idx], topo.domain_nested(topo.DOMAIN_CPU, topo.DOMAIN_PACKAGE, pkg_idx))

    def test_domain_name_type(self):
        self.assertEqual('cpu', topo.domain_name(topo.DOMAIN_CPU))
        self.assertEqual(topo.DOMAIN_CPU, topo.domain_type('cpu'))
        with self.assertRaises(RuntimeError):
            topo.num_domain('non-domain')
        with self.assertRaises(RuntimeError):
            topo.num_domain(100)

if __name__ == '__main__':
    unittest.main()
