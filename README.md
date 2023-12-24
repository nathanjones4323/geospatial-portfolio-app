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
- [Running the App Locally](#usage)
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

> **If you need to rebuild and run the container run this command**

```
docker-compose up --force-recreate --build -d && docker image prune -f
```

If this is the first time you are running the app, it will take a few minutes for the data pipelines to finish running. You can check the status of the pipelines by running the following command:

```bash
docker-compose logs -f
```

Once the pipelines have finished running (or if you are restarting the app), you can access the Streamlit UI at http://localhost:8501

## 🚀 Deployment <a name = "deployment"></a>

This app is deployed on Digital Ocean using a droplet and their managed PostgreSQL offering.

Here are the steps to deploy the app on Digtial Ocean after you have created an account:

*  Install the Digital Ocean CLI
```bash
brew install doctl
```

*  Login with the Digital Ocean CLI
```bash
doctl auth init
```

*  Create a managed PostgreSQL database
```bash
doctl databases create portfolio --engine pg --region sfo2 --size db-s-1vcpu-1gb
```

*  Generate an SSH key
```bash
ssh-keygen
```

*  Add the SSH key to your Digital Ocean account
```bash
doctl compute ssh-key import do_ssh --public-key-file ~/.ssh/id_rsa.pub
```


*  Create a droplet
```bash
doctl compute droplet create geospatial-streamlit-portfolio --tag-names portfolio --image ubuntu-23-10-x64 --region sfo2 --size s-2vcpu-2gb --ssh-keys ${ssh_key_md5_fingerprint} --enable-ipv6 --enable-monitoring --enable-private-networking
```
Where `${ssh_key_md5_fingerprint}` is the MD5 fingerprint of the SSH key you created in the previous step. You can find this by running the following command:
```bash
doctl compute ssh-key list
```

*  SSH into the droplet
```bash
doctl compute ssh geospatial-streamlit-portfolio
```

*  Install docker-compose
```bash
sudo apt update && sudo apt install docker-compose && docker-compose --version
```

*  Clone the repository
```bash
git clone https://github.com/nathanjones4323/geospatial-portfolio-app.git
```

*  Navigate to the app's directory
```bash
cd geospatial-portfolio-app
```

*  Create a `.env` file inside of `./data-pipelines/census`
```bash
cd data-pipelines/census && nano .env
```

*  Paste in the following environment variables into the `.env` file
```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=
POSTGRES_HOST=
US_CENSUS_CROSSWALK_API_KEY=
```

Where `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, and `POSTGRES_HOST` are the same values you used when creating the managed PostgreSQL database. `US_CENSUS_CROSSWALK_API_KEY` is the API key you can get from the [US Census Bureau](https://api.census.gov/data/key_signup.html).

*  Install and configure nginx
```bash
sudo apt install nginx &&
sudo ufw allow "Nginx Full" &&
sudo nano /etc/nginx/sites-available/geospatial-portfolio-app.conf
```

*  Paste in the following configuration into the `geospatial-portfolio-app.conf` file
```bash
server { listen 80; listen [::]:80; server_name ${dropet_ipv4_address};

    access_log  /var/log/nginx/geospatial-portfolio-app.access.log;
    error_log   /var/log/nginx/geospatial-portfolio-app.error.log;

    location / {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Proto https;
      proxy_pass http://localhost:8501;
  }
}

server {
    listen       80;
    listen       [::]:80;
    server_name  ${your_subdomain}.${your_domain};

    access_log  /var/log/nginx/geospatial-portfolio-app.access.log;
    error_log   /var/log/nginx/geospatial-portfolio-app.error.log;

    location / {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Proto https;
      proxy_pass http://localhost:8501;
  }
}
```
Replace `${dropet_ipv4_address}` with the IP address of your droplet and `${your_subdomain}.${your_domain}` with the subdomain and domain you want to use for your app.

`${your_subdomain}.${your_domain}` is the URL you will use to access the app instead of the droplet IP address.

Hit `control + O` and then `ENTER` to save. Press `control + X` to exit

Link the configuration file `sudo ln -s /etc/nginx/sites-available/geospatial-portfolio-app.conf /etc/nginx/sites-enabled/`

Check that the config file syntax is correct `sudo nginx -t`

Reload nginx with new config `sudo systemctl reload nginx.service`

Check that app is able to be opened now in your browser at `http://{droplet_ip_address} & http://{your_subdomain}.{your_domain}`

*  Installing Certbot and Setting Up TLS Certificates (HTTPS instead of HTTP)

```bash
sudo apt install certbot python3-certbot-nginx &&
sudo certbot --nginx -d ${your_subdomain}.${your_domain}
```

Hit `control + d` to exit droplets and end ssh session


<!-- #### Push the containers to Docker Hub (do this for data pipelines and Streamlit app)

Login to Docker

```
docker login
```

Build the containers

```
docker build -t {image_name}:$(git rev-parse --short HEAD) . --platform linux/amd64

docker build -t {image_name}:$(git rev-parse --short HEAD) . --platform linux/amd64
docker run pipelines . --platform linux/amd64
```

Tag the containers

```
docker tag {image_name}:$(git rev-parse --short HEAD) {docker_hub_username}/{image_name}:$(git rev-parse --short HEAD)
```

Push the containers to Docker Hub

```
docker push {docker_hub_username}/{image_name}:$(git rev-parse --short HEAD)
``` -->




## 🗒️ TODO <a name = "todo"></a>

### In Progress

- [ ] Build out Streamlit UI / functionality
  - [ ] Update the metric descriptions on the homepage (Datast Description)
- [ ] Add deployment instructions for Digital Ocean

### Future

- [ ] Fix truncating column name error ==> Postgres can only handle 63 characters for column names and this is causing duplicate column names
  - For now, just filter for a subset of columns in the data pipelines
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
  - [x] Add drill down functionality to the map for CBSA --> ZCTA on click

  #### Notes
