# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from lib.aci import ACIBaseActions


class createSnapshot(ACIBaseActions):
    def run(self, apic="default", description=None, credentials=None):
        self.set_connection(apic, credentials)
        post = {}

        snapshot_dn = "uni/fabric/configexp-defaultOneTime"

        endpoint = "/node/mo/uni/fabric/configexp-defaultOneTime.json"
        payload = {}
        payload['configExportP'] = {}
        payload['configExportP']['attributes'] = {}
        payload['configExportP']['attributes']['descr'] = description
        payload['configExportP']['attributes']['adminSt'] = "triggered"

        post[snapshot_dn] = self.aci_post(endpoint, payload)
        return post
