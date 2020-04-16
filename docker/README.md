# Tranqility Base Activator for Importing Data into Google Cloud Platform (GCP)

The tb-activator-gft-datazone is a repo that facilitates the loading of data into a Google Cloud Platform environment use in specific use cases, for example as an accelerator to build a secure data science environment.

The activator provides the shared components infrastructure, and also installs terraform and project and creates service accounts.

The activator can be installed either through the docker package (recommended) or via the underlying source code. Both of these are available in the repository.

# Description
Running this package creates the following infrastructure resources in GCP:
## GCE (Google Cloud Compute) 
Virtual machines that can be used to perform ETL tasks. This activator creates 1 virtual machines. The types of machine can be
 configured at terraform apply stage using the following variable:
 
 ```
 vms_machine_type: Machine type of the virtual both machines, example 'n1-standard-2'
 ``` 

It also installs important python packages such as: 
* pandas
* numpy
* scikit-learn
* tensorflow
* keras
* pytorch
* google-cloud-storage
* google-cloud-bigquery
* google-cloud-sdk
* google-cloud-core
* gcsfs
* plotly
* pip
* pyspark  
 

## GCS (Google Cloud Storage)
In this activator, we creates two google storage buckets. 
 * landing-data-bucket: To be used for landing incoming data.
 * staging-data-bucket: To be used by Dataproc.
 
There is an example data file 'market_data.csv', which will be uploaded into
 landing-data-bucket as part of this infrastructure building, It will be
  uploaded into ```landing-data-bucket/prepared_data/```.

## BigQuery

BigQuery is a serverless, highly scalable, and cost-effective cloud data
 warehouse. In this infrastructure building task, the following resources
  will be created. 
  * google_bigquery_dataset, named market_dataset
  * google_bigquery_table, named market


## Dataproc cluster
Dataproc is a fast, easy-to-use, fully managed cloud service for running
Apache Spark and Apache Hadoop clusters. In Dataproc creation, the
following specification can be configured:

* dataproc_workers_size: Datapro worker sizes (storage) in GB, example 50.
* dataproc_workers_num_instances: Number of worker instances for dataproc
  cluster, example 3.
* dataproc_workers_machine_type: Machine type for dataproc workers, 
  example 'custom-1-6656-ext'


# Installation procedure
Please run the following commands:
get the image, please update 1.2 which is the version, check and update to latest version, at the time of writing this document the latest version is 1.2.
```
docker pull docker.pkg.github.com/tranquilitybase-io/tb-activator-gft-datazone/ml-datazone:1.2
```
Create a directory name 'data', copy your service account file into that directory, the name of file shall be 'service-account.json'
Use 'docker image ls' to get your image id. Then use your image id in the following step, in the following example the image id is f8b02511ceda
Run the following commands to run the image and then get the docker container id.
```
docker run -t -v /Users/Workspace/data:/opt/app/data/ -d f8b02511ceda
docker container ls
```
You need to execute the following steps, please note to change the container id '2e427edb7c0f' to your container id for the following commands.
Get info.json file, in info.json file there are list of mandatory and optional variable that needs to be updated. 
```
docker exec -it 2e427edb7c0f cat info.json
{
    "name": "gcp ML datazone",
    "category": "Machine Learning",
    "lastUpdated": "07-Apr-2020",
    "platforms": "GCP",
    "ci": "Jenkins",
    "cd": "Jenkins",
    "description": "Environment securely push the data into infrastructure for data science activity.",
    "Url": "git@github.com:tranquilitybase-io/tb-activator-gft-datazone.git",
    "mandatory variables": ["standard_subnetwork", "zone","host_project_id","region"],
    "optional variables": ["vms_size"]
}
```
Alternatively you can use script to list variables that needs to be updated you can run the script using the following command
```
docker exec -it 2e427edb7c0f python3 tf-utils.py -a list -in tb-activator-gft-datazone/variables.tf
[2020-04-12 23:57:22] INFO:root:  Namespace(action='list', config_file=None, in_file='tb-activator-gft-datazone/variables.tf', loglevel=None, output_file='')
[2020-04-12 23:57:22] INFO:root:  Input variable.tf file is: tb-activator-gft-datazone/variables.tf
[2020-04-12 23:57:22] INFO:root:  Variables that needs to be updated are:
[2020-04-12 23:57:22] INFO:root:  ['host_project_id', 'region', 'zone', 'standard_subnetwork']
```
tf-utils.py writes a file named update_file.txt containing list of variables that need to be updated, you can access the file as follow:
```
docker exec -it 2e427edb7c0f cat update_file.txt
host_project_id
region
zone
standard_subnetwork
```
The above list of variables need to be updated in variables.tf file,  tf-utils.py can be used to update the file. Given above list you need to create a variables.json file that has the list of variables that needs to be updated with their values. Example of variables.json is in the following box, please copy this file in to your local 'data' directory, in this example the data directory is /home/Workspace/docker/data
```
{
    "standard_subnetwork": "main-network-subnet",
    "zone": "europe-west2-b",
    "region": "europe-west2",
    "host_project_id": "activator-kubernetes"
}
```
You can use tf-utils.py to update the variables.tf file, please run it as follow:
```
exec -it 2e427edb7c0f  python3 tf-utils.py -a update -c data/variables.json -in tb-activator-gft-datazone/variables.tf
```
Your variable file has been update and now you can run the terraform code. 
```
docker exec -it 2e427edb7c0f terraform  init tb-activator-gft-datazone/
docker exec -it 2e427edb7c0f terraform validate tb-activator-gft-datazone/
docker exec -it 2e427edb7c0f terraform plan tb-activator-gft-datazone/
docker exec -it 2e427edb7c0f terraform apply tb-activator-gft-datazone/
```
