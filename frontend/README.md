## What is this

A normal react app created by vite, visualizing the data analysis for comp90024 team80.

## Setup
To run the app locally, first run ```cd my-app```.

If you have not installed nodejs and yarn, please install nodejs and then run ```npm install -g yarn```.

Run ```yarn``` to install all the dependences.

Run ```yarn dev``` to start the web page locally.

Run ```yarn build``` to build the app.

## File Description
- **my-app/src/components**: Some reuseable components including chart and map.
- **my-app/src/stores/dataStore.js**: All the relavent methods for fetching data and global ui states.
- **my-app/utils/chartOptions.js**: All the relavent chart options for plotting charts and maps with Echarts.
- **my-app/dist**: The built app ready for deployment.
