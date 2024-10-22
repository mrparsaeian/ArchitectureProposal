ansible-galaxy collection install community.vmware cisco.nxos ansible.hashivault
vault kv put secret/esxi root_password="esxi_password"
vault kv put secret/nexus username="admin" password="nexus_password"
export VAULT_TOKEN="vault-token"
ansible-playbook -i hosts.ini link_aggregation.yml

