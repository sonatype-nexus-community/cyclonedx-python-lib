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

import toml

from . import BaseParser
from ..model import ExternalReference, ExternalReferenceType, HashType
from ..model.component import Component


class PoetryParser(BaseParser):

    def __init__(self, poetry_lock_contents: str) -> None:
        super().__init__()
        poetry_lock = toml.loads(poetry_lock_contents)

        for package in poetry_lock['package']:
            component = Component(
                name=package['name'], version=package['version']
            )

            for file_metadata in poetry_lock['metadata']['files'][package['name']]:
                component.add_external_reference(ExternalReference(
                    reference_type=ExternalReferenceType.DISTRIBUTION,
                    url=component.get_pypi_url(),
                    comment=f'Distribution file: {file_metadata["file"]}',
                    hashes=[
                        HashType.from_composite_str(file_metadata['hash'])
                    ]
                ))

            self._components.append(component)


class PoetryFileParser(PoetryParser):

    def __init__(self, poetry_lock_filename: str) -> None:
        with open(poetry_lock_filename) as r:
            super(PoetryFileParser, self).__init__(poetry_lock_contents=r.read())
        r.close()
