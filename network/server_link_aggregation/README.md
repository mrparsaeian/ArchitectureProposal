
### Step-by-Step Instructions

#### Overview

This documentation will guide you through:

1. Setting up HashiCorp Vault to securely store credentials.
2. Using Ansible to automate link aggregation configuration on ESXi hosts and Cisco Nexus switches.
3. Utilizing Ansible to retrieve credentials securely from Vault.

#### Step 1: Set Up HashiCorp Vault

1. **Install and Start Vault**:
    
    * Ensure HashiCorp Vault is installed and running on a server that the Ansible management server can access.
2. **Authenticate to Vault**:
    
    * Use a Vault token to authenticate. Set the token as an environment variable named `VAULT_TOKEN` for easy access during automation.
3. **Store Credentials in Vault**:
    
    * Use Vault to store sensitive credentials, such as:
        * **ESXi root password**.
        * **Cisco Nexus username and password**.
    * Store them in secure paths (e.g., `secret/esxi` for ESXi credentials, and `secret/nexus` for Cisco Nexus credentials).

#### Step 2: Create an Inventory File for Ansible

1. **Define Hosts**:
    * Create an inventory file (`hosts.ini`) to include:
        * **ESXi Hosts**: Define all 6 ESXi servers, including their IP addresses.
        * **Cisco Nexus Switch**: Define the Cisco Nexus switch with its IP address.
    * The inventory should have minimal information, excluding sensitive data such as passwords, since those are securely stored in Vault.

#### Step 3: Prepare Ansible Environment

1. **Install Required Ansible Collections**:
    
    * **VMware Collection**: Install the `community.vmware` Ansible collection, which provides modules to manage ESXi hosts.
    * **Cisco NX-OS Collection**: Install the `cisco.nxos` Ansible collection to interact with Cisco Nexus switches.
    * **HashiCorp Vault Collection**: Install `ansible.hashivault` for retrieving secrets from Vault.
2. **Install the Collections**:
    
    * Use the `ansible-galaxy collection install` command to install the necessary collections for working with VMware, Cisco Nexus, and Vault.

#### Step 4: Create an Ansible Playbook to Automate Configuration

1. **Retrieve Credentials from Vault**:
    
    * Use the **Vault Collection** (`hashivault_read` module) to securely retrieve credentials for ESXi and Cisco Nexus devices during playbook execution.
    * Store retrieved credentials as variables for subsequent use in the playbook.
2. **Configure Link Aggregation on ESXi Hosts**:
    
    * Configure **Link Aggregation** for the **2 x 10Gbps links** on each ESXi host:
        * Create a **vSwitch-LACP** virtual switch for link aggregation.
        * Set the uplink interfaces (`vmnic1` and `vmnic2`) to use **LACP in active mode**.
        * Define a Link Aggregation Group (LAG) on each ESXi server to manage the aggregated links.
3. **Configure Link Aggregation on Cisco Nexus N3K Switch**:
    
    * Set up a **Port-Channel** on the Cisco Nexus switch to match the link aggregation from the ESXi hosts.
    * Configure **Port-Channel 20** and set it to **trunk mode** for the two 10Gbps links.
    * Use **LACP active mode** to ensure the switch actively negotiates the aggregated link with the ESXi servers.
    * Add the corresponding physical interfaces (`Ethernet1/1` and `Ethernet1/2`) to the configured Port-Channel.

#### Step 5: Run the Ansible Playbook

1. **Set the Vault Token**:
    
    * Before running the playbook, export the **Vault token** to your environment:
    
    ```bash
    export VAULT_TOKEN="your-vault-token"
    ```
    
    * The token is used by the Ansible playbook to authenticate with Vault and access stored credentials.
2. **Execute the Playbook**:
    
    * Run the playbook using the inventory file you created:
    
    ```bash
    ansible-playbook -i hosts.ini link_aggregation.yml
    ```
    
    * Verify that all tasks have successfully executed and that the configuration changes are applied to both ESXi and Cisco Nexus devices.

#### Configuration Details

* **LACP (Link Aggregation Control Protocol)**:
    * **Active Mode**: Configure LACP in active mode on both ESXi and Cisco Nexus. This ensures that both devices actively participate in the negotiation of link aggregation, maximizing redundancy and throughput.
* **Port-Channel Configuration**:
    * Create a **Port-Channel** on Cisco Nexus for the interfaces connected to ESXi.
    * Set the Port-Channel in **trunk mode** to handle multiple VLANs as needed for data traffic.

#### Security Best Practices

1. **Store Credentials Securely**:
    
    * Use **HashiCorp Vault** to store sensitive information, such as passwords, securely.
    * Restrict access to Vault paths containing the credentials to only authorized personnel.
2. **Use Environment Variables for Tokens**:
    
    * Avoid hardcoding the Vault token in scripts or playbooks. Instead, use an environment variable (`VAULT_TOKEN`) for secure access during automation.
3. **Use Ansible Vault for Playbook Security**:
    
    * Optionally, use **Ansible Vault** to encrypt the playbook or sensitive parts of the configuration to add another layer of security.

#### Benefits of Using Ansible and Vault

1. **Automated, Consistent Configuration**:
    
    * Using Ansible to configure link aggregation ensures consistency across all ESXi hosts and switches, reducing the risk of human error.
2. **Secure Credential Management**:
    
    * By storing credentials in HashiCorp Vault, you ensure that passwords are not exposed in playbooks, inventory files, or in logs.
3. **Scalable Solution**:
    
    * This approach is scalable, allowing for easy addition of more ESXi hosts or further configurations on the Cisco Nexus switches as the network grows.

### Summary

1. **Vault Setup**: Store ESXi and Cisco Nexus credentials securely in HashiCorp Vault.
2. **Inventory File**: Define ESXi hosts and Cisco Nexus switches in an inventory file without sensitive information.
3. **Ansible Collections**: Install the VMware, Cisco NX-OS, and Vault collections to facilitate configurations.
4. **Playbook Creation**:
    * Retrieve credentials from Vault during playbook execution.
    * Configure link aggregation on both ESXi and Cisco Nexus switches using LACP.
5. **Execution**: Run the Ansible playbook with secure credentials to automate the entire process.
