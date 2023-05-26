## Ansible Playbook Overview

### Intorduction

\item Establish four new instances, each with the appropriate selection of storage volume and security groups.
\item Mounting and conﬁguration of storage volumes on the relative instances.
\item Clone the necessary script files from GitHub, such as Dockerfiles and YAML files.
\item Install required dependencies and software packages, including but not limited to pip and Docker.
\item Deploy and configure CouchDB within Docker on instances 2, 3, and 4, designating instance 4 as the master node, and integrate the remaining instances into the CouchDB cluster.
\item Deploy the Mastodon harvest within Docker on instance 4.
\item Deploy data analytics scripts (for example, sentiment analysis) and the backend infrastructure within Docker on instance 1.
\item Implement Docker Swarm, designating instance 1 as the manager and instances 2, 3, and 4 as workers. Utilize Docker Swarm to create a frontend service.

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

