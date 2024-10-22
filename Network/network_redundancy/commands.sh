ansible-galaxy collection install cisco.nxos
ansible-galaxy collection install ansible.hashivault

vault login "root-token"
vault kv put secret/nexus username="admin" password="cisco_password"
export VAULT_TOKEN="vault-token"
ansible-playbook -i hosts.ini nexus_vrrp_lacp_vault.yml
