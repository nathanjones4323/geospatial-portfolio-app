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

<p align="center"> PROJECT DESCRIPTION
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Running the App](#usage)
- [TODO](#todo)

## 🧐 About <a name = "about"></a>


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

## 🗒️ TODO <a name = "todo"></a>

### In Progress

- [ ] Build out Streamlit UI / functionality
  - [ ] Fix choropleth color scale => All geographies look the same color, but we should be able to see the difference between them
  - [ ] Add interpretation of the 3D map => What does the height/color of the buildings represent?
  - [ ] Either make the user filter when ZCTA is selected, or simplify the polygon data so that it can be loaded into the UI without crashing it.
  - [ ] Add `st.dataframe` tables to accompany the maps
  - [ ] Add the rest of the metrics (might depend on fixing the truncating column name error)
  - [ ] Make the pydeck tooltip parameter dynamic based on UI selections

### Future

- [ ] Fix truncating column name error ==> Postgres can only handle 63 characters for column names and this is causing duplicate column names
- [ ] Add query parameters so users can share links to specific views of the app
- [ ] Make a tutorial on how to use the app
- [ ] Speed up the data pipelines using threading
- [ ] Clean up Dockerfiles and .env files ==> shouldn't have to specify the same environment variables in multiple places

### Completed

- [x] Add CBSA data to the data pipelines
- [x] Add a check to the data pipelines to see if the data has already run and if so, don't run it again
- [x] Fix memory error ==> the data pipelines are running out of memory when trying to load the ZCTA boundary data into the database
  - Fixed by writing the writing the data in chunks instead of all at once
- [x] Rewrite `mapping.py` module
