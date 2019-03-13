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


class createTenant(ACIBaseActions):
    def run(self, apic="default", tenant_name=None, credentials=None):
        self.set_connection(apic, credentials)
        post = {}

#        for tenant in tenant_name:
#            all_tenants = self.get_tenant_list()
#            tenant_dn = "uni/tn-%s" % (tenant)

	tenant_dn = "uni/tn-%s" % (tenant_name)
        all_tenants = self.get_tenant_list()    
        if tenant_dn in all_tenants:
           post[tenant_dn] = {"status": "Tenant already exists"}
        else:

           endpoint = "node/mo/%s.json" % (tenant_dn)
           payload = {}
           payload['fvTenant'] ={}
           payload['fvTenant']['attributes'] = {}
           payload['fvTenant']['attributes']['name']= tenant_name
           post[tenant_dn] = self.aci_post(endpoint, payload)
        return post

