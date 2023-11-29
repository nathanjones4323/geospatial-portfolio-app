<p align="center">
  <a href="" rel="noopener">
  <!-- Use the image stored in this relative path `images/logo.png` as the src attribute of the img tag. -->
  <img width=500px height=300px src="images/logo.png" alt="Project logo"></a>
</p>

<h3 align="center">US Census Interactive GIS Application</h3>

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Explore a number of housing metrics from US Census data in an interactive GIS application
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Running the App](#usage)
- [Deployment](#deployment)
- [TODO](#todo)

## 🧐 About <a name = "about"></a>

This project is an interactive GIS application that allows users to explore a number of housing metrics from US Census data. The app is built using [Streamlit](https://streamlit.io/) and [Deck.gl](https://deck.gl/). The application uses a PostgreSQL backend to store the data. The data is sourced from the [US Census Bureau](https://www.census.gov/).


## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

Docker ([Docker Desktop comes with Docker](https://www.docker.com/products/docker-desktop/))

## 🏃 Running the App <a name = "usage"></a>

Clone the repoisitory
```
git clone https://github.com/nathanjones4323/geospatial-portfolio-app.git
```

Navigate to the app's directory
```
cd geospatial-portfolio-app
```

Run the following in your terminal:
```
docker-compose up -d
```

> :warning: If you need to rebuild and run the container run this command
```
docker-compose up --force-recreate --build -d && docker image prune -f
```

If this is the first time you are running the app, it will take a few minutes for the data pipelines to finish running. You can check the status of the pipelines by running the following command:

```bash
docker-compose logs -f
```

Once the pipelines have finished running (or if you are restarting the app), you can access the Streamlit UI at http://localhost:8501

## 🚀 Deployment <a name = "todo"></a>

This app is deployed on AWS using ECS and RDS (PostgreSQL).

Here are the steps to deploy the app on AWS:

#### Push the containers to Docker Hub (do this for data pipelines and Streamlit app)

Login to Docker

```
docker login
```

Build the containers

```
docker build -t {image_name}:$(git rev-parse --short HEAD) . --platform linux/amd64
```

Tag the containers

```
docker tag {image_name}:$(git rev-parse --short HEAD) {docker_hub_username}/{image_name}:$(git rev-parse --short HEAD)
```

Push the containers to Docker Hub

```
docker push {docker_hub_username}/{image_name}:$(git rev-parse --short HEAD)
```




## 🗒️ TODO <a name = "todo"></a>

### In Progress

- [ ] Build out Streamlit UI / functionality
  - [ ] Add the rest of the metrics (might depend on fixing the truncating column name error)
  - [ ] Update the metric descriptions on the homepage (Datast Description)
  - [ ] Either make the user filter when ZCTA is selected, or simplify the polygon data so that it can be loaded into the UI without crashing it.
  - [ ] Add drill down functionality to the map for CBSA --> ZCTA on click

### Future

- [ ] Fix truncating column name error ==> Postgres can only handle 63 characters for column names and this is causing duplicate column names
- [ ] Add query parameters so users can share links to specific views of the app
- [ ] Make a tutorial on how to use the app
- [ ] Speed up the data pipelines using threading
- [ ] Clean up Dockerfiles and .env files ==> shouldn't have to specify the same environment variables in multiple places
- [ ] Make a function for adding a new metric
  - Current process:
    - Find the truncated column name for the metric using `standardize_column_name` from `transform.py`
    - Add the metric internal name (and rename if neeed) to filter from data pipeline in `run_acs_2021_cbsa_pipeline` and `run_acs_2021_zcta_pipeline` from `pipelines.py`
    - Add mapping inside of `get_metric_internal_name` from `utils.py` using the metric display name as the key and the internal name as the values
    - Add the metric internal name inside of `queries.py`
    - Define metric display name inside of the `options` for the multiselect widget in `siebar.py`

### Completed

- [x] Add CBSA data to the data pipelines
- [x] Add a check to the data pipelines to see if the data has already run and if so, don't run it again
- [x] Fix memory error ==> the data pipelines are running out of memory when trying to load the ZCTA boundary data into the database
  - Fixed by writing the writing the data in chunks instead of all at once
- [x] Rewrite `mapping.py` module
- [ ] Build out Streamlit UI / functionality
  - [x] Fix choropleth color scale => All geographies look the same color, but we should be able to see the difference between them
  - [x] Add interpretation of the 3D map => What does the height/color of the buildings represent?
  - [x] Add `st.dataframe` tables to accompany the maps
  - [x] Make the pydeck tooltip parameter dynamic based on UI selections

  #### Notes
