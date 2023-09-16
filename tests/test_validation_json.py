# encoding: utf-8

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

from glob import iglob
from os.path import join
from unittest import TestCase

from ddt import data, ddt, idata, unpack

from cyclonedx.schema import SchemaVersion
from cyclonedx.validation.json import JsonValidator

from . import TESTDATA_DIRECTORY

RELEVANT_TESTDATA_DIRECTORY = join(TESTDATA_DIRECTORY, 'schemaTestData')

UNSUPPORTED_SCHEMA_VERSIONS = (SchemaVersion.V1_0, SchemaVersion.V1_1,)


@ddt
class TestJsonValidator(TestCase):

    @data(*UNSUPPORTED_SCHEMA_VERSIONS)
    def test_throws_with_unsupported_schema_version(self, schema_version: SchemaVersion) -> None:
        with self.assertRaisesRegex(NotImplementedError, 'not implemented for schema'):
            JsonValidator(schema_version)

    @idata((sv, tf) for sv in SchemaVersion if sv not in UNSUPPORTED_SCHEMA_VERSIONS for tf in
           iglob('valid-*.json', root_dir=join(RELEVANT_TESTDATA_DIRECTORY, sv.to_version())))
    @unpack
    def test_validate_no_none(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(RELEVANT_TESTDATA_DIRECTORY, schema_version.to_version(), test_data_file), 'r') as tdfh:
            test_data = tdfh.read()
        error = validator.validate_str(test_data)
        self.assertIsNone(error)

    @idata((sv, tf) for sv in SchemaVersion if sv not in UNSUPPORTED_SCHEMA_VERSIONS for tf in
           iglob('invalid-*.json', root_dir=join(RELEVANT_TESTDATA_DIRECTORY, sv.to_version())))
    @unpack
    def test_validate_expected_error(self, schema_version: SchemaVersion, test_data_file: str) -> None:
        validator = JsonValidator(schema_version)
        with open(join(RELEVANT_TESTDATA_DIRECTORY, schema_version.to_version(), test_data_file), 'r') as tdfh:
            test_data = tdfh.read()
        error = validator.validate_str(test_data)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error.data)
