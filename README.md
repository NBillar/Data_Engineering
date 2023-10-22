# Data_Engineering
This repo will be used to keep track of our code for the Data Engineering course at Jads


Container notes


Make API container first, then UI, because ENV of UI links to API

MAKE UI DOCKER IMAGE AND CONTAINER:
sudo docker build -t prediction-ui:0.0.1

sudo docker run -p 5001:5000  -d —name=prediction-ui prediction-ui:0.0.1





MAKE API DOCKER IMAGE AND CONTAINER:

sudo docker build -t prediction-api:0.0.1

sudo docker run -p 5000:5000  -d —name=prediction-api prediction-api:0.0.1

