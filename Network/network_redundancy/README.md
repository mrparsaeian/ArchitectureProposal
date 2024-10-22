Below is a step-by-step instructional guide for using Ansible to configure VRRP (Virtual Router Redundancy Protocol) and Link Aggregation (LACP) on Cisco Nexus N3K switches, while securely managing sensitive credentials with HashiCorp Vault.

### Overview

This guide will cover the following steps:

1. Setting up HashiCorp Vault to securely store Cisco Nexus credentials.
2. Configuring Ansible to retrieve credentials from Vault.
3. Creating an Ansible playbook to configure VRRP and Link Aggregation on Cisco Nexus switches.

### Steps to Configure Cisco Nexus Switches with Ansible and HashiCorp Vault

#### Step 1: Store Cisco Nexus Credentials in HashiCorp Vault

1. **Start HashiCorp Vault**: Make sure Vault is running and accessible from your Ansible management server.
    
2. **Login to Vault**: Authenticate to Vault using a token, which can be set as an environment variable (`VAULT_TOKEN`). This token allows interaction with the Vault server.
    
3. **Store Credentials in Vault**:
    
    * Store sensitive credentials such as the Cisco Nexus switch username and password in Vault under a secure path (e.g., `secret/nexus`).
    * Ensure that the password is encrypted and protected by Vault policies to restrict access to only those who need it.

#### Step 2: Set Up Ansible Inventory File

1. **Create an Inventory File**: Create an Ansible inventory file (`hosts.ini`) that includes minimal information about the Cisco Nexus switches.
    * Use IP addresses for the `ansible_host`.
    * Exclude sensitive information (e.g., passwords) from the inventory file since they will be retrieved securely from Vault.

#### Step 3: Prepare Ansible Environment

1. **Install Cisco NX-OS Collection**:
    * Install the **Cisco NX-OS Ansible collection** (`cisco.nxos`) using Ansible Galaxy. This collection contains the modules necessary for managing Cisco Nexus switches.
2. **Install HashiCorp Vault Ansible Collection**:
    * Install the **HashiCorp Vault Ansible collection** (`ansible.hashivault`) to allow integration between Ansible and Vault.
    * This collection provides modules to read secrets from Vault during the execution of playbooks.

#### Step 4: Configure Ansible Playbook

1. **Create an Ansible Playbook**:
    
    * Create an Ansible playbook that will:
        * **Retrieve credentials from Vault**: Use the `hashivault_read` module to securely read the Cisco Nexus username and password.
        * **Set retrieved credentials as variables** (`nexus_username` and `nexus_password`).
2. **Configure VRRP and Link Aggregation**:
    
    * Use tasks in the playbook to:
        * **Create VLANs** for VRRP.
        * **Configure Port-Channel** interfaces for link aggregation using **LACP**.
        * **Add physical interfaces** to the Port-Channel for the 4 x 10Gbps links.
        * **Configure VRRP** on the SVI interface, setting different priorities to create active and standby redundancy.
3. **Apply Credentials Securely**:
    
    * Use the credentials retrieved from Vault as Ansible variables (`ansible_user` and `ansible_password`) for each task interacting with the switches.
    * This ensures sensitive information is not exposed in the playbook, keeping it secure.

#### Step 5: Run the Ansible Playbook

1. **Set the Vault Token**:
    
    * Before running the playbook, set the **Vault token** in the environment to allow the playbook to authenticate with Vault:
        
        ```bash
        export VAULT_TOKEN="your-vault-token"
        ```
        
    * This token should have read access to the secret path containing the Cisco Nexus credentials.
2. **Execute the Playbook**:
    
    * Run the playbook using Ansible to apply the configuration to the Cisco Nexus switches.
    * Verify that all the tasks execute successfully, and the desired configuration is applied.

#### Summary of Steps

1. **HashiCorp Vault Setup**:
    
    * Store the Cisco Nexus credentials securely in Vault under a specific path.
    * Authenticate to Vault using a token stored in an environment variable.
2. **Ansible Inventory and Collections**:
    
    * Use a minimal inventory file (`hosts.ini`) without sensitive information.
    * Install **Cisco NX-OS** and **HashiCorp Vault** Ansible collections to enable the necessary modules.
3. **Create and Execute Ansible Playbook**:
    
    * **Retrieve Credentials from Vault**: The playbook retrieves Cisco Nexus credentials during execution to ensure secure usage.
    * **Configure VRRP and LACP**:
        * Configure VRRP on VLANs for high availability.
        * Create Link Aggregation using 4 x 10Gbps links with LACP on Cisco Nexus N3K switches.
    * **Run Securely**: Set the Vault token and execute the playbook securely to configure the network switches.

#### Security Best Practices

* **Vault Token**: Store the Vault token securely and provide it only when needed for execution.
* **Access Control**: Use Vault policies to restrict access to the credentials based on roles.
* **Environment Variables**: Avoid hardcoding sensitive information in playbooks or inventory files. Instead, leverage environment variables and Vault for secure handling.

### Benefits of This Approach

1. **Secure Management of Credentials**:
    
    * By using HashiCorp Vault, credentials are never exposed in plaintext, enhancing security.
2. **Automated and Consistent Configuration**:
    
    * Ansible ensures that VRRP and link aggregation configurations are applied consistently across multiple devices, reducing manual errors.
3. **Scalable and Repeatable**:
    
    * The use of Ansible allows the configuration to be easily scaled to additional Cisco Nexus switches, ensuring a repeatable and automated approach to network configuration.
