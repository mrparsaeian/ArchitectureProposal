# 01
ansible-galaxy collection install community.vmware
ansible-playbook -i inventory esxi_config.yml
# 02
ansible-playbook -i hosts.ini install_dhcp.yml
ansible-playbook -i hosts.ini install_bind9.yml
# 03
# 04
pip install hpilo
ansible-galaxy collection install community.general
ansible-galaxy collection install community.hpilo
# 041
ansible-playbook -i hosts.ini install_vault.yml
# 05
vault server -dev
vault kv put secret/server1 ilo_user="ilo_user1" ilo_password="ilo_password1"
vault kv put secret/server2 ilo_user="ilo_user2" ilo_password="ilo_password2"
ansible-galaxy collection install community.hashi_vault
ansible-vault create ilo_credentials.yml
cat 05-add_to_ilo_credentials.yml >> ilo_credentials.yml
ansible-playbook -i hosts.ini install_esxi.yml --ask-vault-pass
# 06
ansible-playbook -i hosts.ini configure_dhcp.yml