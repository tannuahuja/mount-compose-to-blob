we have a docker compose file we have to mount the volume to the azure blob storage

: To store data from your Docker container in Azure Blob Storage using Blobfuse
1. install blobfuse
   sudo apt-get update
  sudo apt-get install -y blobfuse fuse

2. Configure Blobfuse
   sudo nano /etc/blobfuse_connection.cfg
in this file add:
   accountName datavideostorage
accountKey YOUR_ACCOUNT_KEY
containerName composedata

to get the account key we can run this command
 az storage account keys list --account-name datavideostorage --query '[0].value' --output tsv

3. secure the config file
  sudo chmod 600 /etc/blobfuse_connection.cfg

4. create mount point and cache directories
   sudo mkdir -p /mnt/blobfuse
sudo mkdir -p /mnt/blobfuse_cache

5. 
