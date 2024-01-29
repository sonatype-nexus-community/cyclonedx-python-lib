# This file is part of CycloneDX Python Lib
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

from unittest import TestCase

from ddt import ddt, named_data

from cyclonedx.model.bom_ref import BomRef
from tests import reorder


@ddt
class TestBomRef(TestCase):

    def test_sort(self) -> None:
        # expected sort order: (value)
        expected_order = [0, 1, 2, 4, 3]
        refs = [
            BomRef('a'),
            BomRef('b'),
            BomRef('c'),
            BomRef('f'),
            BomRef('d'),
        ]
        sorted_refs = sorted(refs)
        expected_refs = reorder(refs, expected_order)
        self.assertListEqual(sorted_refs, expected_refs)

    @named_data(
        ('A-A', BomRef('A'), BomRef('A')),
    )
    def test_equal(self, a: BomRef, b: BomRef) -> None:
        self.assertEqual(a, b)

    @named_data(
        ('None-None', BomRef(), BomRef()),
        ('X-None', BomRef('X'), BomRef()),
        ('None-X', BomRef(), BomRef('X')),
        ('A-B', BomRef('A'), BomRef('B')),
    )
    def test_unequal(self, a: BomRef, b: BomRef) -> None:
        self.assertNotEqual(a, b)
