## Ansible Demos

Ansible has won the 'hearts and minds' of configuration management for network automation. Ansible provides roles and and modules which are like plugins. A role (unsurprisingly) is available for Junos.

Ansible provides the ability to link the concept of `tasks` together in a `playbook` which is an atomic unit of configuration task by Ansible.

First, let's get operational.

```bash
sudo pip install ansible==2.4.2.0
pip install jxmlease
ansible-galaxy install Juniper.junos
```

Next we populate the `hosts` file and place some `group_vars`.

```bash
# /etc/ansible/hosts
[junos_all:children]
vMX

[vMX]
vMX01    junos_host=10.42.0.130
```

```bash
# /etc/ansible/group_vars/junos_all/credentials.yml
# core modules from Ansible 2.1 with the argument provider
credentials:
  host: "{{ junos_host }}"
  username: netconf
  password: Passw0rd
timeout: 20

# /etc/ansible/group_vars/junos_all/common_settings.yml
---
login_message: This is the banner put in by Ansible
time_zone: Europe/London
name_servers:
- 8.8.8.8
- 8.8.8.4
```

Examples can be taken from [here](https://www.juniper.net/documentation/en_US/junos-ansible/information-products/pathway-pages/junos-ansible.pdf)

## Testing the Basics

This set of demos is split in to five different directories:

```bash
├── 1_get_facts
│   └── pb_collect_facts.yml
├── 2_get_config
│   ├── configs
│   └── pb_collect_config.yml
├── 3_rpc_calls
│   └── pb_make_rpc_calls.yml
├── 4_compare_configs
│   └── pb_compare_configs.yml
├── 5_configure
│   ├── build_conf
│   │   └── vMX01
│   │       └── interfaces-mpls.j2
│   ├── pb_configure_merge.yml
│   ├── pb_configure_private_set.yml
│   └── pb_template_config.yml
├── inventory
```

Run through each demo and observe changes.

Run each playbook from the Ansible root directory and ensure that `/etc/ansible` has been populated with group_vars and host information. 

It's also easy to inspect what variables are available to Ansible for a host by running the following command. It's a great trouble shooting step!

```bash
ansible -m debug -a "var=hostvars['vMX01']" localhost
```

```bash
cd /demos/ansible/
ansible-playbook <dir>/pb*.yaml
```
