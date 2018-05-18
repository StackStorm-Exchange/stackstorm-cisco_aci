# Cisco ACI

## Description
A basic pack for working with Cisco ACI systems using the RestFul API. Most of the actions are coded to take the same input and just actions their associated part. This is for 2 reasons.
* keeps the input simpler and cleaner
* all the required information such as Tenant, AP etc are always included.

## Connection Configuration
Copy the sample file [cisco_aci.yaml.sample] into the config folder and make any necessarily adjustments.
The config file requires details for connecting to an APIC, Address, username and password.
It is recommended that a read only account be setup and used for these tasks. This allows any of the get actions to be performed without requiring a dedicated user.
It is recommended that for any set/create actions that suitable accounts be passed in the `credentials` parameter. This allows for an audit trail within ACI.


## Actions
* 'cisco_aci.create_ap' - Create a Application Profile under a Tenant
* 'cisco_aci.create_bd' -  Create a Bridge Domain under a Tenant
* 'cisco_aci.create_epg' - Create a EPG
* 'cisco_aci.create_static_binding' -  Create a Static Binding
* 'cisco_aci.get_aps' -  Retrieve all Application Profiles
* 'cisco_aci.get_assigned_ports' -  Retrieve list of Ports and details about their assignment
* 'cisco_aci.get_bds' -  Retrieve all Bridge Domains
* 'cisco_aci.get_epgs' - Retrieve all EPGs
* 'cisco_aci.get_sessionid' -  Retrive a Session ID
* 'cisco_aci.get_static_bindings' -  Retrieve list of Static Bindings
* 'cisco_aci.get_tenants' - Retrieve list of Tenants
* 'cisco_aci.get_vrfs' -  Retrieve list of VRFs
* 'cisco_aci.link_domain' - Associate an EPG with a given Domain
* 'test_endpoint.yaml - retrieve output froma custom Endpoint on the API

## Workflows
* 'cisco_aci.setup_epg' - Setup an EPG with all associated Application Profiles, Bridge Domians, Static Bindings and Domain Links

## Sample Input
As stated most create states use the same format of input. here is a sample of how that input should look
```
{"tenant1":  - Tenant name
  {
  "tenant1-AP1": { - Application Profile
    "tenant1-BD102": { - Bridge Domain
      "vrf": "tenant1-VRF1", - VRF name
      "epgs": {
        "tenant1-EPG102": { - EPG name
          "desc": "Tenant 1 EPG 102", - EPG description
          "domains": ["VM1","PHYS"],- Domains to associate with
          "static_bindings": {
            "103": - VLAN number
              [{"leaf1": 46}, {"leaf2": 46}] - Leaf/ports to associate
            }
          },
        "tenant1-EPG103": {
          "desc": "Tenant 1 EPG 103",
          "domains": ["VM1","PHYS"],
          "static_bindings": {
            "104":
              [{"leaf1": 46}, {"leaf2": 46}]
          }
        }
      }
    }
  },
  "tenant1-AP2": {
    "tenant1-BD202": {
      "vrf": "tenant1-VRF1",
      "epgs": {
        "tenant1-EPG202": {
          "desc": "Tenant 1 EPG 202",
          "domains": ["VM1","PHYS"],
          "static_bindings": {
            "103":
              [{"leaf1": 46}, {"leaf2": 46}]
            }
          },
        "tenant1-EPG203": {
          "desc": "Tenant 1 EPG 203",
          "domains": ["VM1","PHYS"],
          "static_bindings": {
            "104":
              [{"leaf1": 47}, {"leaf2": 47}]
          }
        }
      }
    }
  }
  }    
}
```

## ACI Setup Assumptions:
### Naming conventions
* Application Profile - <Tenant>-AP<unique number> eg. tenant1-AP1
* Bridge Domain - <Tenant>-BD<app number><unique number> eg. tenant1-BD102
* EPG - <Tenant>-EPG<app number><unique number> eg. tenant1-EPG102
* VRF - <Tenant>-VRF<unique number> eg. tenant1-VRF1

very few of these naming conventions are enforced within the ACI actions although they are the basis on which the actions were made.


### Only Create New
The first incarnation fo this pack will only create that which does not exist. If any of the elemtns are found to be there the action will just contine without performing any tasks.

### Static bindings
The create static binding action makes the assumption that the following associations have been put in place
* Leaves are associated with a Switch Policy > Profile > Leaf Profile
* This is then associated with an Interface Selector Profile (Interface Policies > Profiles > Leaf Profile)
* The port is added to a Access Port Selector under the Interface Policy
* The Policy Group for the Access Port Selector contains the Tenant within the name

### VRF
Within the input the VRF parameter is optional.. if this is ommited the default fallback is "tenant"-VRF1.

### Physical Domain String for static bindings
When definign a domain you can specify a tdn that will be used during the static binding creation.
However if the domain type is `PHYS` and no tdn is provided it will use the following format to create one
`uni/phys-Managed-Hosting-<tenant>-Domain<number at end of Ap>


## TODO

