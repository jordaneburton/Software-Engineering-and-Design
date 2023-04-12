# Say It Ain't Genes - Jordan Burton
For this assignment, we gather data from the Human Genome Organization(HUGO). HUGO is a non-profit organzation which oversees the HUGO Gene Nomenclature Committee(HGNC). The HGNC sorts and identifies names for genes. This program will download their entire set of HGNC data into a Redis database through a Flask interface. This assignment helps us to get acquainted with the Redis databases and how to integrate them with our use of Flask and Docker. 
## Included Files
`gene_api.py` - is the main python script that executes our Flask API. It retrieves data from HUGO's website utilizing various http requests. These requests are sent using the routes built into the script.

`docker-compose.yml` - allows the user to skip a few steps in the process of running the docker image. It allows us to use a single command to both create an image and run it.

`Dockerfile` - allows us to create the docker image as well as containerize our program. Through containerizing the script, we can install all the necessary libraries and requirements needed to run the program as intended. This allows a user to not worry about making sure they have the correct version of certain libraries. Instead the Dockerfile takes care of that for us.
## Installation
Install the project by cloning the repository. Docker is required to operate this project. In turn, all necessary libraies are handled via Docker's containerization. When the program is run through a docker image, all necessary libraries will be accounted for.
## Program Descriptions
### Gene API
`gene_api.py`, is an API with three distinct routes. These routes allow us to query information on HGNC data from the Human Genome Organization ([HUGO](https://www.genenames.org/download/archive/)). Here is a list of the routes along with brief descriptions:
| Route | Method | Description |
|---|---|---|
|`/data`| GET | Return all data from the Redis database |
|`/data`| POST | Put data into the Redis database from the HUGO website |
|`/data`| DELETE | Delete data from the Redis database |
|`/genes`| GET | Returns json-formatted list of all hgnc\_ids in the database |
|`/genes/<hgnc_id>`| GET | Return all data associated with specified \<hgnc\_id\> |
## Using Existing Docker Image
Before you can run the application, you will need to pull the repository for this project off of GitHub using `git pull` or any other preferred method. In your command terminal, you will need to pull my docker image using the following command:
```
$ docker pull jordaneburton/gene_api.py:1.0
```
You can check to see if the image was pulled using `docker images`. Once pulled, you can run Redis and Flask on ports 6379 and 5000 by using the following command:
```
$ docker-compose up -d
```
If the need to stop any containers arises, you can use the command, `docker-compose down`.
## Building a New Docker Image
In your linux environment, you will first pull the necessary files from my Github. This can be done using `git pull` or whichever preferred method. Then you can build your own image using the following command:
```
$ docker build -t <username>/gene_api.py:<tag> .
```
You can edit the command and insert your own username and tag as you wish. Once built, you can run your image using:
```
$ docker-compose up
```
If you need to stop any containers, you can also use `docker-compose down`.
## Using the Code
In order to properly use the program, you will need to run your image in one terminal window and input commands in another. The first thing you would want to do in the program is post data to the database. This can be done as follows:
```
$ curl -X POST localhost:5000/data
```
This same route, `/data`, can also be used to delete or get the data from the database by changing the method used in your command.
Once you have data posted in the database, you can use the route, `/genes/<hgnc_id>` to get data on a specific HGNC ID. If used, the route should produce a result like such:
```
{
  "_version_": ...,
  "agr": "HGNC:...",
  "ccds_id": [
    "..."
  ]
...
...
  "gene_group": [
    "Zyxin family",
    "MicroRNA protein coding host genes"
  ],
...
...
}
```
## Data Interpretation
Most of the data is in the form of ID(used for database identification), but the following data is the most interesting:
| Key | Data |
|---|---|
| hgnc\_id | HGNC ID. A unique ID created by the HGNC for every approved symbol |
| locus\_group | A group name for a set of related locus types as defined by the HGNC (e.g. non-coding RNA) |
| locus\_typ | The locus type as defined by the HGNC (e.g. RNA, transfer) |
| location | Cytogenetic location of the gene (e.g. 2q34) |
## Sources
- [The Human Genome Organization(HUGO)](https://www.genenames.org/download/archive/)
