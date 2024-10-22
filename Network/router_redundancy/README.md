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


### Overview

1. **Link Aggregation**: Combining four `10G` Ethernet links to increase throughput and redundancy.
2. **VRRP (Virtual Router Redundancy Protocol)**: Establishing a virtual router with multiple physical routers to ensure failover capabilities.
3. **HSRP (Hot Standby Router Protocol)**: Adding redundancy for routers, providing high availability by automatically switching to a standby router.
4. **Ansible Playbook**: Automate the entire configuration process.
5. **HashiCorp Vault**: Used to securely store the Cisco Nexus device passwords.

### Step-by-Step Instructions

#### 1. **Prerequisites**

* **Cisco Nexus N3K Switch**: Ensure Cisco Nexus switches are reachable over the network.
* **Ansible**: Install Ansible on your management server.
* **Ansible Cisco NX-OS Collection**: Install the Cisco NX-OS collection with:
    
    ```bash
    ansible-galaxy collection install cisco.nxos
    ```
    
* **HashiCorp Vault**: Make sure HashiCorp Vault is set up, and passwords are securely stored.

#### 2. **Set Up Environment Variables**

* Create an environment file (`env.yml`) to store configuration variables:
    * `nexus_host`: IP address of the Cisco Nexus switch.
    * `interface_links`: A list of the four 10G interfaces to be bundled.
    * `vrrp_group_id`: The VRRP group identifier.
    * `hsrp_group_id`: The HSRP group identifier.
    * `virtual_ip`: The virtual IP address used by both VRRP and HSRP.
    * `primary_router_priority` and `standby_router_priority`: Priority values for determining primary and standby routers.

#### 3. **Create an Ansible Playbook**

Create an Ansible playbook to automate the configuration of link aggregation, VRRP, and HSRP.

* **Vault Integration**: Use Ansible to retrieve the Cisco Nexus password from Vault securely.
* **Link Aggregation**:
    * Configure **link aggregation** by bundling four interfaces into a **port-channel**.
    * Set the mode for the link aggregation to `active`.
* **Port-Channel Configuration**:
    * Set up a **port-channel** interface (`port-channel1`) that aggregates the four 10G links.
    * Configure **Layer 3** settings on the `port-channel` to allow routing.
* **VRRP Configuration**:
    * Configure **VRRP** on the `port-channel` interface.
    * Set the **VRRP group ID**, **virtual IP address**, and **router priority** to determine the primary router.
* **HSRP Configuration**:
    * Configure **HSRP** on the `port-channel` interface.
    * Set the **HSRP group ID**, **virtual IP address**, and **router priority** to ensure a failover mechanism.

#### 4. **Using HashiCorp Vault for Passwords**

* **Password Storage**: Store the Cisco Nexus password securely in HashiCorp Vault under a specific path (e.g., `secret/network_device_passwords`).
* **Password Retrieval**:
    * The Ansible playbook must have a task to connect to Vault and retrieve the stored password using the **Vault token**.
    * Set the Vault token in the environment before running the playbook to allow secure retrieval.

#### 5. **Running the Playbook**

* **Vault Token**:
    * Export the Vault token to the environment so that the playbook can authenticate with Vault:
        
        ```bash
        export VAULT_TOKEN="your-vault-token"
        ```
        
* **Run the Playbook**:
    * Execute the playbook to configure VRRP, HSRP, and link aggregation on the Cisco Nexus N3K:
        
        ```bash
        ansible-playbook configure_vrrp_hsrp_linkagg.yml
        ```
        
* **Verification**:
    * Ensure all tasks complete successfully.
    * Check the configuration on the Cisco Nexus N3K switches to verify that the VRRP, HSRP, and link aggregation settings are correctly applied.

### Summary

1. **Link Aggregation Configuration**:
    * Combine four `10G` interfaces to create a **port-channel** for redundancy and higher throughput.
2. **VRRP Setup**:
    * Configure **VRRP** on the `port-channel` to ensure router redundancy.
    * Set priority values to determine the **primary router**.
3. **HSRP Setup**:
    * Configure **HSRP** to complement VRRP for additional redundancy and failover.
    * Set up the **standby router** with appropriate priorities.
4. **Secure Password Management**:
    * Use **HashiCorp Vault** to securely store and retrieve the Cisco Nexus device password.
5. **Automate with Ansible**:
    * Create an Ansible playbook that integrates with Vault to automate the entire process.
