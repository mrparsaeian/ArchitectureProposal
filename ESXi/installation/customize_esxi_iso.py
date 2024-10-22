import os
import sys

def customize_esxi_iso(esxi_iso_path, output_iso_path, root_password, ip_address):
    # Run ESXi-Customizer command to modify the ISO
    command = f"ESXi-Customizer -i {esxi_iso_path} -o {output_iso_path} -p {root_password} -a {ip_address}"
    result = os.system(command)
    if result != 0:
        print(f"Failed to customize the ISO for {ip_address}")
        sys.exit(1)
    print(f"Customized ISO created for {ip_address} at {output_iso_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python customize_esxi_iso.py <esxi_iso_path> <output_iso_path> <root_password> <ip_address>")
        sys.exit(1)

    esxi_iso_path = sys.argv[1]
    output_iso_path = sys.argv[2]
    root_password = sys.argv[3]
    ip_address = sys.argv[4]

    customize_esxi_iso(esxi_iso_path, output_iso_path, root_password, ip_address)
