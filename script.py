import os
import subprocess
import signal
import sys

account_name = 'datavideostorage'
account_key = 'coAj1vJnf5z66BA2PKhBASeP4GbvwsO9GFv1cNpafh9l6tLEk0IW7YBhCiAdx8IbnFTwLcQMEbGB+AStPsWzAg=='  # Replace with your actual key
container_name = 'datavideo'

config_file_path = '/etc/blobfuse_connection.cfg'
mount_point = '/mnt/blobfuse'
tmp_path = '/mnt/blobfuse_cache'

def is_installed(command):
    try:
        subprocess.run([command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_azure_cli():
    print("\nInstalling Azure CLI...")
    subprocess.run(['curl', '-sL', 'https://aka.ms/InstallAzureCLIDeb', '|', 'sudo', 'bash'], check=True)
    print("Azure CLI installed successfully.\n")

def install_blobfuse():
    print("\nInstalling Blobfuse...")
    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'blobfuse'], check=True)
    print("Blobfuse installed successfully.\n")

def create_config_file():
    print("Creating configuration file for Blobfuse...")
    config_content = f"""
accountName {account_name}
accountKey {account_key}
containerName {container_name}
    """

    with open(config_file_path, 'w') as config_file:
        config_file.write(config_content)

    os.chmod(config_file_path, 0o600)
    print(f"Configuration file created at {config_file_path}\n")

def create_directories():
    print("Creating mount and cache directories...")
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
        print(f"Mount directory created at {mount_point}\n")
    else:
        print(f"Mount directory already exists at {mount_point}\n")

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
        print(f"Cache directory created at {tmp_path}\n")
    else:
        print(f"Cache directory already exists at {tmp_path}\n")

def mount_blob_storage():
    print("Mounting Blob storage...")
    mount_command = [
        'sudo', 'blobfuse', mount_point,
        '--tmp-path=' + tmp_path,
        '--config-file=' + config_file_path,
        '-o', 'attr_timeout=240',
        '-o', 'entry_timeout=240',
        '-o', 'negative_timeout=120',
        '-o', 'allow_other'
    ]
    subprocess.run(mount_command, check=True)
    print(f"Blob storage mounted at {mount_point}\n")

# def unmount_blob_storage():
#     print("\nUnmounting Blob storage...")
#     unmount_command = ['sudo', 'fusermount', '-u', mount_point]
#     subprocess.run(unmount_command, check=True)
#     print(f"Blob storage unmounted from {mount_point}\n")

# def signal_handler(sig, frame):
#     print("\nSignal received, exiting...")
#     unmount_blob_storage()
#     sys.exit(0)

def main():
    print("\nStarting setup for Azure Blob Storage mounting...\n")

    if not is_installed('az'):
        install_azure_cli()
    else:
        print("Azure CLI is already installed.\n")

    if not is_installed('blobfuse'):
        install_blobfuse()
    else:
        print("Blobfuse is already installed.\n")

    create_config_file()
    create_directories()
    mount_blob_storage()

    # Register signal handlers for clean exit
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    print(f"Setup completed successfully! Blob storage is mounted at {mount_point}.")
    # print("Press Ctrl+C to unmount and exit.\n")

    # # Keep the script running to maintain the mount
    # signal.pause()
    # unmount_blob_storage()

if __name__ == '__main__':
    main()
