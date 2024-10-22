
### **Ansible Inventory File Setup**

1. **Create Inventory File**: Start by creating an inventory file (`hosts.ini`) to define your hosts. This inventory file will contain the details of the server(s) where you intend to install HAProxy. In this example, we will configure HAProxy on the local host.
    
    **Steps**:
    
    * Create a file named `hosts.ini`.
    * Add the following content to the file to define the local server as the target:
        * Define a group named `haproxy_servers` with the `localhost` connection.

### **Ansible Playbook for HAProxy Installation and Configuration**

2. **Create an Ansible Playbook**: This playbook will install HAProxy, create a backup of the existing configuration, and set up load balancing between 12 VMs using the IP range `10.0.0.0`.
    
    **Steps**:
    
    * Create a playbook named `install_haproxy.yml` that contains tasks to automate the installation and configuration process.
    * The playbook should be structured as follows:
        * Update the system packages to ensure all dependencies are up to date.
        * Install HAProxy using the package manager (`apt`).
        * Create a backup of the default HAProxy configuration (`haproxy.cfg`) to allow for restoration if needed.
        * Replace the existing HAProxy configuration with a new configuration to achieve load balancing across the 12 VMs.
        * Define a handler to restart the HAProxy service once the configuration changes are applied.
3. **Playbook Configuration Details**:
    
    * **System Update**:
        * Ensure the system is updated by updating the package cache and upgrading all packages.
    * **Install HAProxy**:
        * Use the `apt` package manager to install the `haproxy` package.
    * **Backup Original Configuration**:
        * Before making changes, back up the original HAProxy configuration file (`/etc/haproxy/haproxy.cfg`) to a new location (`/etc/haproxy/haproxy.cfg.bak`).
    * **Configure HAProxy for Load Balancing**:
        * Create a new HAProxy configuration that includes:
            * **Global Settings**: Standard global settings, such as logging and user configuration.
            * **Defaults Section**: Define default options like timeouts.
            * **Frontend Definition**: Set up a frontend to listen on port `80` to receive HTTP traffic.
            * **Backend Definition**: Define a backend to manage load balancing across 12 VMs using the round-robin method.
            * **Backend Servers**: Define each of the 12 VMs using their respective IP addresses in the `10.0.0.0` range (e.g., `10.0.10.101`, `10.0.10.102`, etc.).
    * **Handler for Restarting HAProxy**:
        * After applying changes, notify a handler that restarts the HAProxy service to ensure the new configuration is loaded.
4. **Running the Ansible Playbook**:
    
    * Use the following command to execute the playbook:
        
        ```bash
        ansible-playbook -i hosts.ini install_haproxy.yml
        ```
        
    * This command will run the playbook using the specified inventory file, ensuring that HAProxy is installed and configured as per the requirements.

### **Summary of Configuration**

* **HAProxy Setup**: The playbook will install HAProxy on the server and ensure that it is configured correctly to perform load balancing across 12 VMs using a round-robin algorithm.
* **VM IP Range**: The VMs have IP addresses within the `10.0.0.0` range, which allows for efficient load distribution.
* **Configuration Backup**: The original HAProxy configuration is backed up to prevent data loss and enable recovery.
* **Automation**: Using Ansible ensures that the entire setup process is automated and repeatable, minimizing manual intervention and potential errors.