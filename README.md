we have a docker compose file we have to mount the volume to the azure blob storage
Mount Azure BLOB Storage as File System on Docker container


: :    
To store data from your Docker container in Azure Blob Storage using Blobfuse

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

5. mount the azure blob storage
   sudo blobfuse /mnt/blobfuse --tmp-path=/mnt/blobfuse_cache --config-file=/etc/blobfuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 -o allow_other

verify the mount
ls /mnt/blobfuse

6. update the docker compose file

```version: "3"
services:
    shinobi:
        image: registry.gitlab.com/shinobi-systems/shinobi:dev
        container_name: Shinobi
        environment:
           - PLUGIN_KEYS={}
           - SSL_ENABLED=false
        volumes:
           - /home/azureuser/Shinobi/config:/config
           - /home/azureuser/Shinobi/customAutoLoad:/home/Shinobi/libs/customAutoLoad
           - /home/azureuser/Shinobi/database:/var/lib/mysql
           - /mnt/blobfuse:/home/Shinobi/videos  # Mount Azure Blob storage for video data
           - /home/azureuser/Shinobi/plugins:/home/Shinobi/plugins
           - /dev/shm/Shinobi/streams:/dev/shm/streams
        ports:
           - 8080:8080
        restart: unless-stopped```

7. docker-compose up -d
run docker compose 



links: 
(main)
https://www.srcecde.me/posts/2022/09/mount-azure-blob-storage-as-file-system-on-docker-container/



https://medium.com/@mariusz_kujawski/how-to-mount-azure-storage-in-docker-container-ac0a81b64e2e
