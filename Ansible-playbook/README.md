# COMP90024 Project

## Introduction

The team is developing a Cloud-based solution exploiting cloud instances on MRC for harvesting data by Mastodon, storing data by CouchDB, processing data by frontend, and visualizing data by frontend.

## Project Structure

- **Ansible-playbook**: Contains the Ansible Playbooks automating the setup and configuration of our server.

- **Backend**: Includes the server-side logic and API for our scenarios.

- **SUDO_Data**: Stores and handles SUDO data for system-level tasks and permissions.

- **crawler**: Web crawling component for harvesting Mastodon data.

- **frontend/my-app**: Handles user interactions and data presentation.

- **node_modules**: Contains all dependencies and sub-dependencies of the project.

- **.DS_Store**: Stores custom attributes of its containing folder.

- **README.md**: Initial file serving as an introductory and instructional guide to the project.

- **package-lock.json**: Auto-generated and updated by NPM containing the exact dependency tree.

- **package.json**: Key file for managing dependencies and other project metadata.

## System Deployment

The project is deployed using Ansible, automating the process of applications deployment across four instances.

### Ansible Playbook Overview
![image](https://github.com/CarrickC/COMP90024-23S1-A2/assets/131973111/16bef5b7-3281-4c23-95a1-3235f447a482)

1. Establish four new instances with appropriate storage volume and security groups.
2. Mount and configure storage volumes on the instances.
3. Clone necessary script files from GitHub.
4. Install required dependencies and software packages.
5. Deploy and configure CouchDB within Docker on instances.
6. Deploy Mastodon harvest within Docker on instance 4.
7. Deploy data analytics scripts and backend infrastructure within Docker on instance 1.
8. Implement Docker Swarm, designating instance 1 as the manager and others as workers.

## Visualization

Visit [Project Visualization](http://172.26.133.136:8081) to see our project's visualization.
