### Overview

In this guide, we will cover the process of:

1. Configuring an Ansible playbook to integrate Prometheus with Grafana.
2. Adding dashboards to Grafana with PromQL queries to detect anomalies.
3. Using HashiCorp Vault to securely manage the Grafana password.
4. Using environment files to manage other configuration variables.

### Steps to Configure Grafana using Ansible

1. **Set Up Required Variables**
    
    * Create an **environment variable file** (e.g., `env.txt`) to store configuration values like:
        * `grafana_host` (e.g., localhost)
        * `grafana_username` (e.g., admin)
        * `prometheus_url` (e.g., `http://localhost:9090`)
    * Store the **Grafana password** securely in HashiCorp Vault under a secret path (e.g., `secret/grafana`).
2. **Install Grafana and Prometheus**
    
    * Ensure that **Grafana** and **Prometheus** are installed and running.
    * Grafana can be installed using the official APT repository, and Prometheus can be downloaded and installed as a binary.
3. **Create an Ansible Playbook**
    
    * Create an **Ansible playbook** to automate the process of adding the Grafana dashboards.
    * Ensure the playbook has tasks for:
        * Reading the environment file (`env.txt`) for the variables.
        * Retrieving the Grafana password securely from Vault.
4. **Retrieve Grafana Password from Vault**
    
    * Use the **Vault token** to authenticate with HashiCorp Vault.
    * Retrieve the Grafana password using an Ansible task that integrates with Vault.
    * Store the retrieved password in a variable that will be used for Grafana configuration.
5. **Install Grafana Ansible Collection**
    
    * Install the `community.grafana` Ansible collection, which provides modules to interact with Grafana.
    * This collection will be used to create data sources and dashboards programmatically.
6. **Create Prometheus Data Source in Grafana**
    
    * Add a **Prometheus data source** to Grafana using Ansible.
    * Set the Prometheus URL using the variable from the environment file (e.g., `prometheus_url`).
    * Authenticate to Grafana with the `grafana_username` and the retrieved `grafana_password`.
7. **Define Z-Score Queries and Create Grafana Dashboard**
    
    * Use the **PromQL queries** for calculating Z-scores, for example:
        * **CPU Usage Z-Score**: Compares average current CPU usage to historical averages.
        * **Memory Usage Z-Score**: Compares current available memory to historical averages.
        * **Network Ingress Z-Score**: Compares current network ingress rates with historical averages.
    * Create a Grafana dashboard with **multiple panels**:
        * Each panel should include a PromQL query for calculating a Z-score.
        * The queries should be defined as targets for Grafana panels using the Ansible playbook.
8. **Apply Security and Access Management**
    
    * Ensure that sensitive information (e.g., Grafana password) is stored securely in Vault.
    * For secure deployment, run the playbook with environment variables containing the Vault token (`VAULT_TOKEN`).
9. **Run the Ansible Playbook**
    
    * Set the Vault token as an environment variable.
    * Run the Ansible playbook to configure Grafana, create the dashboards, and integrate Prometheus.
    * Verify that all tasks have executed correctly, ensuring the dashboards are visible and properly configured.

### Key Concepts

* **HashiCorp Vault**: Vault is used to store sensitive information such as the Grafana password. This ensures that the password is not stored in plaintext within the Ansible playbook.
* **Environment File (`env.txt`)**: Variables like Grafana's host, username, and Prometheus URL are stored here for easy configuration. This helps separate code from configuration.
* **Ansible Playbook**: The playbook automates the configuration tasks, ensuring consistent setup across different environments. The use of the `community.grafana` collection simplifies dashboard creation.

### PromQL Queries for Anomaly Detection

* The **Z-score** is used to determine how far current data points deviate from historical averages.
* **PromQL** queries are defined to calculate Z-scores for key metrics like CPU, memory, and network.
* The Ansible playbook adds these PromQL queries to specific **Grafana panels** for anomaly detection.

### Security Considerations

* Store the **Vault token** securely and provide it as an environment variable (`VAULT_TOKEN`) to prevent exposure.
* Always use secure passwords and access management practices when managing Grafana, Prometheus, and Vault.

### Summary

* Use Ansible to automate the process of adding Prometheus as a data source in Grafana.
* Retrieve secure information (e.g., password) from HashiCorp Vault to ensure sensitive data is not exposed.
* Configure PromQL queries as panels in Grafana to monitor infrastructure metrics using anomaly detection methods such as **Z-score analysis**.
* Store configuration variables in an external file (`env.txt`) to keep them easily manageable.

This approach ensures an efficient, automated, and secure configuration for monitoring infrastructure with **Grafana and Prometheus** using **Ansible** and **HashiCorp Vault**.