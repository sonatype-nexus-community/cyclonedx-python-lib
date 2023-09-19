# encoding: utf-8

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

__all__ = ['XmlValidator']

from abc import ABC
from typing import Any, Optional, Tuple

from ..schema._res import BOM_XML as _S_BOM
from . import MissingOptionalDependencyException, ValidationError, _BaseValidator

_missing_deps_error: Optional[Tuple[MissingOptionalDependencyException, ImportError]] = None
try:
    from lxml.etree import XMLParser, XMLSchema, fromstring as xml_fromstring  # type: ignore[import]
except ImportError as err:
    _missing_deps_error = MissingOptionalDependencyException(
        'This functionality requires optional dependencies.\n'
        'Please install `cyclonedx-python-lib` with the extra "json-validation".\n'
    ), err


class __BaseXmlValidator(_BaseValidator, ABC):
    if _missing_deps_error:
        __MDERROR = _missing_deps_error

        def validate_str(self, data: str) -> Optional[ValidationError]:
            raise self.__MDERROR[0]  # from functionality_not_implemented_error[1]
    else:
        def validate_str(self, data: str) -> Optional[ValidationError]:
            return self._validata_data(
                xml_fromstring(bytes(data, encoding='utf8'), parser=self.__xml_parser))

        def _validata_data(self, data: Any) -> Optional[ValidationError]:
            validator = self._validator  # may throw on error that MUST NOT be caught
            if not validator.validate(data):
                return ValidationError(validator.error_log.last_error)
            return None

        __validator: Optional['XMLSchema'] = None

        __xml_parser = XMLParser(
            resolve_entities=False,
            no_network=True,
            huge_tree=True,
            compact=True)

        @property
        def _validator(self) -> 'XMLSchema':
            if not self.__validator:
                schema_file = self._schema_file
                if schema_file is None:
                    raise NotImplementedError('missing schema file')
                self.__validator = XMLSchema(file=schema_file)
            return self.__validator


class XmlValidator(__BaseXmlValidator):
    @property
    def _schema_file(self) -> Optional[str]:
        return _S_BOM.get(self.schema_version)