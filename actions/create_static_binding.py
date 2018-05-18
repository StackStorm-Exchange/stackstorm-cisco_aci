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


class createStaticBinding(ACIBaseActions):
    def run(self, apic="default", data=None, credentials=None):
        self.set_connection(apic, credentials)
        post = {}
        allocated_ports = self.get_port_details(apic)

        for tenant in data:
            for app_profile in data[tenant]:
                for bridge_domain in data[tenant][app_profile]:

                    for epg in data[tenant][app_profile][
                            bridge_domain]['epgs']:
                        epg_dn = "uni/tn-%s/ap-%s/epg-%s" %\
                            (tenant, app_profile, epg)
                        endpoint = "node/mo/uni/tn-%s/ap-%s/epg-%s.json" %\
                            (tenant, app_profile, epg)

                        for vlan in data[tenant][app_profile][bridge_domain][
                                'epgs'][epg]['static_bindings']:
                            in_use = False
                            in_use = self.check_vlan_used_elsewhere(
                                vlan, tenant, app_profile, epg_dn)

                            for leaf_port in data[tenant][app_profile][
                                    bridge_domain]['epgs'][epg][
                                    'static_bindings'][vlan]:
                                for leaf in leaf_port:
                                    for pod in self.config['apic'][apic][
                                            'leafs']:
                                        if leaf in self.config['apic'][apic][
                                                'leafs'][pod].keys():
                                            leaf_path = self.config['apic'][
                                                apic]['leafs'][pod][
                                                leaf]['path']
                                    encap = "vlan-%s" % vlan
                                    ethport = "eth1/%s" % (leaf_port[leaf])
                                    sb_tDn = "topology/%s/paths-%s/pathep-"\
                                             "[%s]" % (pod, leaf_path, ethport)
                                    sb_dn = "%s/rspathAtt-[%s]" % (
                                        epg_dn, sb_tDn)
                                    payload = {}
                                    payload['fvRsPathAtt'] = {}
                                    payload['fvRsPathAtt']['attributes'] = {}
                                    payload['fvRsPathAtt']['attributes'][
                                        'encap'] = encap
                                    payload['fvRsPathAtt']['attributes'][
                                        'tDn'] = sb_tDn
                                    payload['fvRsPathAtt']['attributes'][
                                        'status'] = "created"
                                    payload['fvRsPathAtt']['children'] = []
                                    post_dn = "%s-%s-vlan-%s" % \
                                        (epg, sb_tDn, vlan)
                                    if not self.sb_exists(sb_dn):
                                        if not in_use:
                                            if "policy" in allocated_ports[
                                                    pod][leaf_path]['ports'][
                                                    ethport].keys():
                                                if tenant in allocated_ports[
                                                        pod][leaf_path][
                                                        'ports'][ethport][
                                                        'policy']:
                                                    post[post_dn] = \
                                                        self.aci_post(
                                                            endpoint, payload)
                                                else:
                                                    post[post_dn] = \
                                                        {"status": "Port Not "
                                                         "assigned to Tenant "
                                                         "Policy"}
                                            else:
                                                post[post_dn] = \
                                                    {"status": "Port Not "
                                                     "assigned to Tenant "
                                                     "Policy"}
                                        else:
                                            post[post_dn] = {"status": "Vlan "
                                                             "used with "
                                                             "another EPG"}
                                    else:
                                        post[post_dn] = {"status": "Static "
                                                         "Binding already "
                                                         "exists"}

        return post

    def sb_exists(self, sb_dn):
        all_sb = self.get_static_bindings()
        for binding in all_sb['imdata']:
            if binding['fvRsPathAtt']['attributes']['dn'] == sb_dn:
                return True

        return False

    def check_vlan_used_elsewhere(self, vlan, tenant, app_profile, epg_dn):
        all_sb = self.get_static_bindings(tenant, app_profile)
        if all_sb['imdata']:
            for binding in all_sb['imdata']:
                if ("vlan-" + vlan) == \
                        binding['fvRsPathAtt']['attributes']['encap']:
                    if not binding['fvRsPathAtt']['attributes'][
                            'dn'].startswith(epg_dn):
                        return True
        return False
