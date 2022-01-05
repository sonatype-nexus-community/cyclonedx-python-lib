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

import json
from typing import Optional

from . import BaseOutput
from .schema import BaseSchemaVersion, SchemaVersion1Dot0, SchemaVersion1Dot1, SchemaVersion1Dot2, SchemaVersion1Dot3, \
    SchemaVersion1Dot4
from .serializer.json import CycloneDxJSONEncoder
from ..model.bom import Bom


class Json(BaseOutput, BaseSchemaVersion):

    def __init__(self, bom: Optional[Bom] = None) -> None:
        super().__init__(bom=bom)
        self._json_output: str = ''

    def generate(self, force_regeneration: bool = False) -> None:
        if self.generated and not force_regeneration:
            return

        bom_json = json.loads(json.dumps(self.get_bom(), cls=CycloneDxJSONEncoder))
        bom_json = json.loads(self._specialise_output_for_schema_version(bom_json=bom_json))
        self._json_output = json.dumps({**self._create_bom_element(), **bom_json})

        self.generated = True

    def _specialise_output_for_schema_version(self, bom_json: dict) -> str:
        if not self.bom_supports_metadata():
            if 'metadata' in bom_json.keys():
                del bom_json['metadata']
        elif not self.bom_metadata_supports_tools():
            del bom_json['metadata']['tools']
        elif not self.bom_metadata_supports_tools_external_references():
            for i in range(len(bom_json['metadata']['tools'])):
                del bom_json['metadata']['tools'][i]['externalReferences']

        return json.dumps(bom_json)

    def output_as_string(self) -> str:
        self.generate()
        return self._json_output

    # Builder Methods
    def _create_bom_element(self) -> dict:
        return {
            "bomFormat": "CycloneDX",
            "specVersion": str(self.get_schema_version()),
            "serialNumber": self.get_bom().get_urn_uuid(),
            "version": 1
        }


class JsonV1Dot0(Json, SchemaVersion1Dot0):
    pass


class JsonV1Dot1(Json, SchemaVersion1Dot1):
    pass


class JsonV1Dot2(Json, SchemaVersion1Dot2):
    pass


class JsonV1Dot3(Json, SchemaVersion1Dot3):
    pass


class JsonV1Dot4(Json, SchemaVersion1Dot4):
    pass
