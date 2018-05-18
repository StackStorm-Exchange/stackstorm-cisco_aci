
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

import requests

from st2actions.runners.pythonrunner import Action


class ACIBaseActions(Action):

    def __init__(self, config):
        super(ACIBaseActions, self).__init__(config)
        if config is None:
            raise ValueError("No Configuration details found")

        if "apic" in config:
            if config['apic'] is None:
                raise ValueError("No apics defined")
            else:
                pass
        else:
            raise ValueError("No configuration details found")

        return

    def set_connection(self, apic=None, connection_details=None):

        if apic is None:
            apic = "default"
        if apic not in self.config['apic']:
            raise ValueError("Invalid apic")
        else:
            self.apic_address = self.config['apic'][apic]['address']
            self.apic_user = self.config['apic'][apic]['user']
            self.apic_passwd = self.config['apic'][apic]['passwd']

        if connection_details is not None:
                if "user" in connection_details.keys():
                    self.apic_user = connection_details['user']
                if "passwd" in connection_details.keys():
                    self.apic_passwd = connection_details['passwd']

        self.apic_token = ""

        if all(v is not None for v in [self.apic_address,
                                       self.apic_user,
                                       self.apic_passwd]):
            return self.get_sessionid()
        else:
            raise ValueError("Incomplete Connection Details")

    def get_sessionid(self):
        endpoint = 'aaaLogin.json'
        payload = {}
        payload['aaaUser'] = {}
        payload['aaaUser']['attributes'] = {}
        payload['aaaUser']['attributes']['name'] = self.apic_user
        payload['aaaUser']['attributes']['pwd'] = self.apic_passwd

        jdata = self.aci_post(endpoint, payload)
        self.apic_token = {'APIC-Cookie': jdata['imdata'][0][
                           'aaaLogin']['attributes']['token']}

        return self.apic_token

    def get_tenants(self):
        endpoint = 'node/class/fvTenant.json'
        return self.aci_get(endpoint)

    def get_vrfs(self):
        endpoint = 'node/class/fvCtx.json'
        return self.aci_get(endpoint)

    def get_bds(self):
        endpoint = 'node/class/fvBD.json'
        return self.aci_get(endpoint)

    def get_bd_list(self):
        all_bds = []
        bds = self.get_bds()
        for item in bds['imdata']:
            all_bds.append(item['fvBD']['attributes']['dn'])
        return all_bds

    def get_aps(self):
        endpoint = 'node/class/fvAp.json'
        return self.aci_get(endpoint)

    def get_ap_list(self):
        all_aps = []
        aps = self.get_aps()
        for item in aps['imdata']:
            all_aps.append(item['fvAp']['attributes']['dn'])
        return all_aps

    def get_epgs(self):
        endpoint = 'node/class/fvAEPg.json'
        return self.aci_get(endpoint)

    def get_epg_list(self):
        epg_list = []
        epgs = self.get_epgs()
        for item in epgs['imdata']:
            epg_list.append(item['fvAEPg']['attributes']['dn'])
        return epg_list

    def get_static_bindings(self, tenant=None, app_profile=None):
        final_sb = {}
        final_sb['imdata'] = []
        dn_match = ""
        endpoint = 'node/class/fvRsPathAtt.json'
        sb_results = self.aci_get(endpoint)
        if tenant:
            dn_match = ("uni/tn-" + tenant)
            if app_profile:
                dn_match += ("/ap-" + app_profile)

            for item in sb_results['imdata']:
                if item['fvRsPathAtt']['attributes'][
                        'dn'].startswith(dn_match):
                    final_sb['imdata'].append(item)
        else:
            final_sb = sb_results
        return final_sb

    def get_domains(self):
        endpoint = 'node/class/fvDom.json'
        return self.aci_get(endpoint)

    def get_epg_domains(self, tenant, ap, epg):
        domains = []
        endpoint = "node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children"\
                   "&target-subtree-class=fvRsDomAtt" % (tenant, ap, epg)
        jdata = self.aci_get(endpoint)
        for entry in jdata['imdata']:
            domains.append(entry['fvRsDomAtt']['attributes']['tDn'])
        return domains

    def aci_get(self, endpoint):
        url = 'https://%s/api/%s' % (self.apic_address, endpoint)
        headers = {'Accept': 'application/json'}
        p = requests.get(url, headers=headers, verify=False,
                         cookies=self.apic_token)
        return p.json()

    def aci_post(self, endpoint, payload):
        url = 'https://%s/api/%s' % (self.apic_address, endpoint)
        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}

        try:
            ssl_verify = self.config['defaults']['ssl']['verify']
        except ValueError:
            ssl_verify = True

        try:
            p = requests.post(url, headers=headers, json=payload,
                              cookies=self.apic_token,
                              verify=ssl_verify)
            p.raise_for_status()
        except requests.exceptions.HTTPError:
            raise Exception("Error: %s" % (p.json()['imdata'][0]['error'][
                'attributes']['text']))

        return p.json()

    def get_port_details(self, apic):
        allocation = {}
        for pod in self.config['apic'][apic]['leafs']:
            allocation[pod] = {}
            for leaf in self.config['apic'][apic]['leafs'][pod]:
                leaf_no = self.config['apic'][apic]['leafs'][pod][leaf]['path']
                allocation[pod][leaf_no] = {}
                allocation[pod][leaf_no]['ports'] = {}
                leaf_ports_endpoint = \
                    "node/class/topology/%s/node-%s/l1PhysIf.json" % \
                    (pod, leaf_no)
                leaf_port_details = self.aci_get(leaf_ports_endpoint)
                for port in leaf_port_details['imdata']:
                    portid = port['l1PhysIf']['attributes']['id']
                    portdn = port['l1PhysIf']['attributes']['dn']
                    allocation[pod][leaf_no]['ports'][portid] = {}
                    allocation[pod][leaf_no]['ports'][portid]['dn'] = portdn

            structure = self.build_port_structure()
            for switch in structure:
                for switch_profile in structure[switch]:
                    for int_profile in structure[switch][switch_profile]:
                        for acp in structure[switch][switch_profile][
                                int_profile]:
                            for port in structure[switch][switch_profile][
                                    int_profile][acp]['ports']:
                                ethport = "eth%s" % port
                                if "policy" in structure[switch][
                                        switch_profile][int_profile][
                                        acp].keys():
                                    allocation[pod][switch]['ports'][ethport][
                                        'policy'] = structure[switch][
                                        switch_profile][int_profile][
                                        acp]['policy']
                                else:
                                    allocation[pod][switch]['ports'][ethport][
                                        'policy'] = ""
                                allocation[pod][switch]['ports'][ethport][
                                    'sp'] = switch_profile
                                allocation[pod][switch]['ports'][ethport][
                                    'ip'] = int_profile
                                allocation[pod][switch]['ports'][ethport][
                                    'ac'] = acp

        return allocation

    def build_port_structure(self):
        infraNodeBlk = self.aci_get('node/class/infraNodeBlk.json')
        infraRsAccPortP = self.aci_get('node/class/infraRsAccPortP.json')
        infraRsAccBaseGrp = self.aci_get('node/class/infraRsAccBaseGrp.json')
        infraPortBlk = self.aci_get('node/class/infraPortBlk.json')
        structure = {}

        for nodeblk in infraNodeBlk['imdata']:
            nodes = []
            first_node = int(nodeblk['infraNodeBlk']['attributes']['from_'])
            last_node = int(nodeblk['infraNodeBlk']['attributes']['to_'])
            if first_node == last_node:
                nodes.append(first_node)
            else:
                i = first_node
                while i <= last_node:
                    nodes.append(i)
                    i += 1
            for node in nodes:
                if node not in structure.keys():
                    structure[node] = {}
                structure[node]["/".join(nodeblk['infraNodeBlk']['attributes'][
                    'dn'].split("/", 3)[:3])] = {}

        for accport in infraRsAccPortP['imdata']:
            for node in structure:
                for dn in structure[node]:
                    if accport['infraRsAccPortP']['attributes'][
                            'dn'].startswith(dn):
                        structure[node][dn][accport['infraRsAccPortP'][
                            'attributes']['tDn']] = {}

        for accgrp in infraRsAccBaseGrp['imdata']:
            for node in structure:
                for spdn in structure[node]:
                    for lp in structure[node][spdn]:
                        if accgrp['infraRsAccBaseGrp']['attributes'][
                                'dn'].startswith(lp):
                            acc_dn = accgrp['infraRsAccBaseGrp']['attributes'][
                                'dn'].split("/rsacc")[0]
                            structure[node][spdn][lp][acc_dn] = {}
                            structure[node][spdn][lp][acc_dn]['policy'] = \
                                accgrp['infraRsAccBaseGrp']['attributes'][
                                    'tDn']
                            structure[node][spdn][lp][acc_dn]['ports'] = []

        for portblk in infraPortBlk['imdata']:
            for node in structure:
                for spdn in structure[node]:
                    for lp in structure[node][spdn]:
                        for acg in structure[node][spdn][lp]:
                            if portblk['infraPortBlk']['attributes'][
                                    'dn'].startswith(acg):
                                fromport = int(portblk['infraPortBlk'][
                                    'attributes']['fromPort'])
                                toport = int(portblk['infraPortBlk'][
                                    'attributes']['toPort'])
                                i = fromport
                                c = int(portblk['infraPortBlk'][
                                    'attributes']['fromCard'])
                                while i <= toport:
                                    structure[node][spdn][lp][acg][
                                        'ports'].append("%s/%s" % (c, i))
                                    i += 1

        return structure
