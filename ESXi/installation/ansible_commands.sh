#!/bin/bash

# ansible_commands.sh: This script runs the Ansible playbook for installing ESXi on HP servers.
# It includes the use of Ansible Vault to protect sensitive information.

# Check if the vault password file is provided
if [ -z "$1" ]; then
    echo "Usage: ./ansible_commands.sh <vault_password_file>"
    exit 1
fi

VAULT_PASS_FILE=$1

# Run the Ansible playbook using the vault password file
echo "Running Ansible playbook to install ESXi on HP servers..."
ansible-playbook -i hosts.ini install_esxi.yml --vault-password-file $VAULT_PASS_FILE

if [ $? -eq 0 ]; then
    echo "Ansible playbook ran successfully."
else
    echo "Error: Failed to run the Ansible playbook. Please check the logs for more details."
    exit 1
fi
