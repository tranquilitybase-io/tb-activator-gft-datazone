
# Tranqility Base Activator for Importing Data into Google Cloud Platform (GCP) [Source Code Variant]

The tb-activator-gft-datazone is a repo that facilitates the loading of data into a Google Cloud Platform environment use in specific use cases, for example as an accelerator to build a secure data science environment.

The activator provides the shared components infrastructure, and also installs terraform and project and creates service accounts.

The activator can be installed either through the docker package (recommended) or via the underlying source code. Both of these are available in the repository. This README file describes installation using underlying source code.  The 'Docker' folder provides instructions for installation using the docker package.

## Installation: Deploying data landing zone (Using Source Code)

Pre-requisite to build the data science environment is to build the shared
-components infrastructures, and also terraform has been installed and project and service accounts have already been created.

After that please follow the following steps:

* Update connections.tf and add your service account file (json) to provider "google
", full directory to the your file shall be added to file("").
```hcl-terraform
provider "google" {
  credentials = file("")
  project     = var.cluster_project_id
  region      = var.region
}
```
* Update the following variable in variables.tf:
```hcl-terraform
variable "host_project_id" {
  description = "Project ID, example 'data-science-activator'"
  default     = ""
}
variable "zone" {
  description = "General zone of the project, example 'europe-west2-b'"
  default     = ""
}
variable "standard_subnetwork" {
  description = "VPC subnetwork such as main-network-subnet"
  default     = ""
}
variable "region" {
  description = "General location of the project, example 'europe-west2'"
  default     = ""
}
```

You can run terraform as follow:
```shell script
terraform init

terraform validate
 
terraform plan 

terraform apply
```

This activator builds the following components:
    
 
  
### Resources:
#### GCE (Google Cloud Compute) 
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
 

#### GCS (Google Cloud Storage)
In this activator, we creates two google storage buckets. 
 * landing-data-bucket: To be used for landing incoming data.
 * staging-data-bucket: To be used by Dataproc.
 
There is an example data file 'market_data.csv', which will be uploaded into
 landing-data-bucket as part of this infrastructure building, It will be
  uploaded into ```landing-data-bucket/prepared_data/```.

#### BigQuery

BigQuery is a serverless, highly scalable, and cost-effective cloud data
 warehouse. In this infrastructure building task, the following resources
  will be created. 
  * google_bigquery_dataset, named market_dataset
  * google_bigquery_table, named market


#### Dataproc cluster
Dataproc is a fast, easy-to-use, fully managed cloud service for running
Apache Spark and Apache Hadoop clusters. In Dataproc creation, the
following specification can be configured:

* dataproc_workers_size: Datapro worker sizes (storage) in GB, example 50.
* dataproc_workers_num_instances: Number of worker instances for dataproc
  cluster, example 3.
* dataproc_workers_machine_type: Machine type for dataproc workers, 
  example 'custom-1-6656-ext'


#### Gcpip package 
This is a python package that you can use to:
* Encrypt data 
* Upload encrypted data securely into the infrastructure using Clopud KMS
* Perform DLP 
* Load data into BQ
* Create Views in BQ
* Performing feature engineering using Daraproc

## Usage
The activator allows accelerated importation of on-premise data into a GCP environment in a standardised way.  As such it can be deployed as the first step of almost any Cloud or Machine Learning based initiative.

Some potential uses of this activator are outlined in the [wiki](https://github.com/tranquilitybase-io/tb-activator-gft-datazone/wiki) associated with this repo.

[1. Machine Learning Secure Data Solution](https://github.com/tranquilitybase-io/tb-activator-gft-datazone/wiki/1.-Machine-Learning-Secure-Data-Proposition)

[2. Banking Risk: Integrated Model Lifecycle Framework Solution](https://github.com/tranquilitybase-io/tb-activator-gft-datazone/wiki/2.-Banking-Risk:-Integrated-Model-Lifecycle-Framework)

[3. Banking: Federated Process Management Solution](https://github.com/tranquilitybase-io/tb-activator-gft-datazone/wiki/3.-Banking:-Federated-Process-Management-Solution)
