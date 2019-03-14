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


class createInterfaceGroupPolicy(ACIBaseActions):
    def run(self, apic="default", credentials=None, Group_Policy_Name=None, STP_Interface_Policy=None, Ingress_Data_Plane_Policing_Policy=None,
            Storm_Control_Interface_Policy=None, Egress_Data_Plane_Policing_Policy=None, Slow_Drain_Policy=None, Monitoring_Policy=None, MCP_Policy=None,
            CDP_Policy=None, L2_Interface_Policy=None, CoPP_Policy=None, LLDP_Policy=None,
            Fibre_Channel_Interface_Policy=None, Priority_Flow_Control_Policy=None, Link_Level_Policy=None, Port_Security_Policy=None, dot1x_Port_Authentication_Policy=None):

        self.set_connection(apic, credentials)
        post = {}

        policy_dn = "uni/infra/funcprof/accportgrp-%s" % (Group_Policy_Name)
        endpoint = "node/mo/%s.json" % (policy_dn)
        payload = {}
        payload['infraAccPortGrp'] = {}
        payload['infraAccPortGrp']['attributes'] = {}
        payload['infraAccPortGrp']['attributes']['name'] = Group_Policy_Name
        payload['infraAccPortGrp']['children'] = []

        stp_interface_policy = {}
        stp_interface_policy['infraRsStpIfPol'] = {}
        stp_interface_policy['infraRsStpIfPol']['attributes'] = {}
        stp_interface_policy['infraRsStpIfPol']['attributes']['tnStpIfPolName'] = STP_Interface_Policy

        payload['infraAccPortGrp']['children'].append(stp_interface_policy)

        ingress_data_plane_policing_policy = {}
        ingress_data_plane_policing_policy['infraRsQosIngressDppIfPol'] = {}
        ingress_data_plane_policing_policy['infraRsQosIngressDppIfPol']['attributes'] = {}
        ingress_data_plane_policing_policy['infraRsQosIngressDppIfPol']['attributes']['tnQosDppPolName'] = Ingress_Data_Plane_Policing_Policy

        payload['infraAccPortGrp']['children'].append(ingress_data_plane_policing_policy)

        storm_control_interface_policy = {}
        storm_control_interface_policy['infraRsStormctrlIfPol'] = {}
        storm_control_interface_policy['infraRsStormctrlIfPol']['attributes'] = {}
        storm_control_interface_policy['infraRsStormctrlIfPol']['attributes']['tnStormctrlIfPolName'] = Storm_Control_Interface_Policy

        payload['infraAccPortGrp']['children'].append(storm_control_interface_policy)

        egress_data_plane_policing_policy = {}
        egress_data_plane_policing_policy['infraRsQosEgressDppIfPol'] = {}
        egress_data_plane_policing_policy['infraRsQosEgressDppIfPol']['attributes'] = {}
        egress_data_plane_policing_policy['infraRsQosEgressDppIfPol']['attributes']['tnQosDppPolName'] = Egress_Data_Plane_Policing_Policy

        payload['infraAccPortGrp']['children'].append(egress_data_plane_policing_policy)

        slow_drain_policy = {}
        slow_drain_policy['infraRsQosSdIfPol'] = {}
        slow_drain_policy['infraRsQosSdIfPol']['attributes'] = {}
        slow_drain_policy['infraRsQosSdIfPol']['attributes']['tnQosSdIfPolName'] = Slow_Drain_Policy

        payload['infraAccPortGrp']['children'].append(slow_drain_policy)

        monitoring_policy = {}
        monitoring_policy['infraRsMonIfInfraPol'] = {}
        monitoring_policy['infraRsMonIfInfraPol']['attributes'] = {}
        monitoring_policy['infraRsMonIfInfraPol']['attributes']['tnMonInfraPolName'] = Monitoring_Policy

        payload['infraAccPortGrp']['children'].append(monitoring_policy)

        mcp_policy = {}
        mcp_policy['infraRsMcpIfPol'] = {}
        mcp_policy['infraRsMcpIfPol']['attributes'] = {}
        mcp_policy['infraRsMcpIfPol']['attributes']['tnMcpIfPolName'] = MCP_Policy

        payload['infraAccPortGrp']['children'].append(mcp_policy)

        cdp_policy = {}
        cdp_policy['infraRsCdpIfPol'] = {}
        cdp_policy['infraRsCdpIfPol']['attributes'] = {}
        cdp_policy['infraRsCdpIfPol']['attributes']['tnCdpIfPolName'] = CDP_Policy

        payload['infraAccPortGrp']['children'].append(cdp_policy)

        ltwo_interface_policy = {}
        ltwo_interface_policy['infraRsL2IfPol'] = {}
        ltwo_interface_policy['infraRsL2IfPol']['attributes'] = {}
        ltwo_interface_policy['infraRsL2IfPol']['attributes']['tnL2IfPolName'] = L2_Interface_Policy

        payload['infraAccPortGrp']['children'].append(ltwo_interface_policy)

        copp_policy = {}
        copp_policy['infraRsCoppIfPol'] = {}
        copp_policy['infraRsCoppIfPol']['attributes'] = {}
        copp_policy['infraRsCoppIfPol']['attributes']['tnCoppIfPolName'] = CoPP_Policy

        payload['infraAccPortGrp']['children'].append(copp_policy)

        lldp_policy = {}
        lldp_policy['infraRsLldpIfPol'] = {}
        lldp_policy['infraRsLldpIfPol']['attributes'] = {}
        lldp_policy['infraRsLldpIfPol']['attributes']['tnLldpIfPolName'] = LLDP_Policy

        payload['infraAccPortGrp']['children'].append(lldp_policy)

        fibre_channel_interface_policy = {}
        fibre_channel_interface_policy['infraRsFcIfPol'] = {}
        fibre_channel_interface_policy['infraRsFcIfPol']['attributes'] = {}
        fibre_channel_interface_policy['infraRsFcIfPol']['attributes']['tnFcIfPolName'] = Fibre_Channel_Interface_Policy

        payload['infraAccPortGrp']['children'].append(fibre_channel_interface_policy)

        priority_flow_control_policy = {}
        priority_flow_control_policy['infraRsQosPfcIfPol'] = {}
        priority_flow_control_policy['infraRsQosPfcIfPol']['attributes'] = {}
        priority_flow_control_policy['infraRsQosPfcIfPol']['attributes']['tnQosPfcIfPolName'] = Priority_Flow_Control_Policy

        payload['infraAccPortGrp']['children'].append(priority_flow_control_policy)

        link_level_policy = {}
        link_level_policy['infraRsHIfPol'] = {}
        link_level_policy['infraRsHIfPol']['attributes'] = {}
        link_level_policy['infraRsHIfPol']['attributes']['tnFabricHIfPolName'] = Link_Level_Policy

        payload['infraAccPortGrp']['children'].append(link_level_policy)

        port_security = {}
        port_security['infraRsL2PortSecurityPol'] = {}
        port_security['infraRsL2PortSecurityPol']['attributes'] = {}
        port_security['infraRsL2PortSecurityPol']['attributes']['tnL2PortSecurityPolName'] = Port_Security_Policy

        payload['infraAccPortGrp']['children'].append(port_security)

        dotonex_port_auth_policy = {}
        dotonex_port_auth_policy['infraRsL2PortAuthPol'] = {}
        dotonex_port_auth_policy['infraRsL2PortAuthPol']['attributes'] = {}
        dotonex_port_auth_policy['infraRsL2PortAuthPol']['attributes']['tnL2PortAuthPolName'] = dot1x_Port_Authentication_Policy

        payload['infraAccPortGrp']['children'].append(dotonex_port_auth_policy)

        post[policy_dn] = self.aci_post(endpoint, payload)
        return post
