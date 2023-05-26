## Ansible Playbook Overview

- **Common** Common files which used for other ansible-playbook.
- **create_instance_and_volume** Establish four new instances with appropriate storage volume and security groups.
- **mount_volume** Mount and configure storage volumes on the instances.
- **git_clone** Clone necessary script files from GitHub.
- **install_docker** Install required dependencies and software packages.
- **create_couchdb** Deploy and configure CouchDB within Docker on instances.
- **couchdb_cluster** Deploy couchdb cluster, designating instance 4 as masternode.
- **deploy_mastodon** Deploy Mastodon harvest within Docker on instance 4.
- **deploy_backend** Deploy data analytics scripts and backend infrastructure within Docker on instance 1.
- **docker_swarm** Implement Docker Swarm, designating instance 1 as the manager and others as workers.
- **deploy_frontend** Create frontend service by using Docker swarm.

