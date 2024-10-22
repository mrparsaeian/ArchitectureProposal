import sys
import redfish

# Script to mount ESXi ISO on HP server using iLO REST API

def mount_iso(ilo_ip, ilo_user, ilo_password, iso_url):
    try:
        # Connect to iLO
        base_url = f"https://{ilo_ip}"
        session = redfish.redfish_client(base_url=base_url, username=ilo_user, password=ilo_password)
        session.login()

        # Select the virtual media URL
        virtual_media_uri = "/redfish/v1/Managers/1/VirtualMedia/CD"

        # Mount ISO
        response = session.patch(virtual_media_uri, body={"Image": iso_url, "Inserted": True})
        if response.status == 200:
            print(f"ISO successfully mounted on {ilo_ip}")
        else:
            print(f"Failed to mount ISO on {ilo_ip}: {response.status}")
            sys.exit(1)

        # Boot from the ISO
        boot_settings_uri = "/redfish/v1/Systems/1/Bios/Settings"
        boot_settings = {
            "Boot": {
                "BootSourceOverrideTarget": "Cd"
            }
        }
        response = session.patch(boot_settings_uri, body=boot_settings)
        if response.status == 200:
            print(f"Successfully set boot from ISO on {ilo_ip}")
        else:
            print(f"Failed to set boot source on {ilo_ip}: {response.status}")
            sys.exit(1)

        # Reboot the server
        reboot_uri = "/redfish/v1/Systems/1/Actions/ComputerSystem.Reset"
        response = session.post(reboot_uri, body={"ResetType": "ForceRestart"})
        if response.status == 200:
            print(f"Successfully rebooted server {ilo_ip}")
        else:
            print(f"Failed to reboot server {ilo_ip}: {response.status}")
            sys.exit(1)

        # Logout
        session.logout()

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ilo_ip = sys.argv[1]
    ilo_user = sys.argv[2]
    ilo_password = sys.argv[3]
    iso_url = sys.argv[4]

    mount_iso(ilo_ip, ilo_user, ilo_password, iso_url)
