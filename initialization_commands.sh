#!/bin/bash

# initialization_commands.sh: This script initializes the system for configuring a Cisco 3750 switch, HP iLO, and VMware using Ansible.
# It includes checking for an internet connection, verifying Ansible installation, and installing specific versions of the necessary Ansible collections.

# Function to check if the internet connection is available
check_internet_connection() {
    echo "Checking internet connection..."
    if ping -c 1 8.8.8.8 &> /dev/null; then
        echo "Internet connection is available."
    else
        echo "Error: No internet connection. Please check your network settings."
        exit 1
    fi
}

# Function to check if Ansible is installed
check_ansible_installation() {
    echo "Checking if Ansible is installed..."
    if ! command -v ansible &> /dev/null; then
        echo "Error: Ansible is not installed. Please install Ansible and run this script again."
        exit 1
    else
        echo "Ansible is installed."
    fi
}

# Function to install hpilo Python package (specific version)
install_hpilo_package() {
    echo "Checking if hpilo package is installed..."
    if dpkg -l | grep -q "python3-hpilo"; then
        echo "hpilo package is already installed."
    else
        echo "hpilo package not found. Installing version 4.4.2..."
        if sudo apt update && sudo apt install -y python3-hpilo=4.4.2-1; then
            echo "hpilo package version 4.4.2 installed successfully."
        else
            echo "Error: Failed to install hpilo package. Please check your configuration."
            exit 1
        fi
    fi
}

# Function to check if the cisco.ios collection is installed, and install it if necessary
check_cisco_ios_collection() {
    echo "Checking if cisco.ios collection is installed..."
    if ! ansible-galaxy collection list | grep -q "cisco.ios"; then
        echo "cisco.ios collection not found. Installing version 3.3.0..."
        if ansible-galaxy collection install cisco.ios:3.3.0; then
            echo "cisco.ios collection version 3.3.0 installed successfully."
        else
            echo "Error: Failed to install cisco.ios collection. Please check your configuration."
            exit 1
        fi
    else
        echo "cisco.ios collection is already installed."
    fi
}

# Function to check if the community.vmware collection is installed, and install it if necessary
check_vmware_collection() {
    echo "Checking if community.vmware collection is installed..."
    if ! ansible-galaxy collection list | grep -q "community.vmware"; then
        echo "community.vmware collection not found. Installing version 1.12.0..."
        if ansible-galaxy collection install community.vmware:1.12.0; then
            echo "community.vmware collection version 1.12.0 installed successfully."
        else
            echo "Error: Failed to install community.vmware collection. Please check your configuration."
            exit 1
        fi
    else
        echo "community.vmware collection is already installed."
    fi
}


# Function to check if the community.hashi_vault collection is installed, and install it if necessary
check_hashi_vault_collection() {
    echo "Checking if community.hashi_vault collection is installed..."
    if ! ansible-galaxy collection list | grep -q "community.hashi_vault"; then
        echo "community.hashi_vault collection not found. Installing version 3.1.0..."
        if ansible-galaxy collection install community.hashi_vault:3.1.0; then
            echo "community.hashi_vault collection version 3.1.0 installed successfully."
        else
            echo "Error: Failed to install community.hashi_vault collection. Please check your configuration."
            exit 1
        fi
    else
        echo "community.hashi_vault collection is already installed."
    fi
}

# Main script execution
check_internet_connection
check_ansible_installation
install_hpilo_package
check_cisco_ios_collection
check_vmware_collection
check_hashi_vault_collection

echo "All checks passed. System is ready for configuring the Cisco 3750 switch, VMware, HP iLO, and HashiCorp Vault integration using Ansible."
