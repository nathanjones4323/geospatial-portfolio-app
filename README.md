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
- [App Tutorial](#tutorial)
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

Create a `.env` file inside of `./data-pipelines/census`
```bash
cd data-pipelines/census && touch .env
```

Paste in the following environment variables into the `.env` file
```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=
POSTGRES_HOST=
US_CENSUS_CROSSWALK_API_KEY=
```

Where `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, and `POSTGRES_HOST` are the connection values for your PostgreSQL database. `US_CENSUS_CROSSWALK_API_KEY` is the API key you can get from the [US Census Bureau](https://api.census.gov/data/key_signup.html).

The values you use here will be what your PostgreSQL database uses when it is initialized, and what you will connect with when you run the app.

Create a `.env` file inside of `./db` and use the same environment variables as above
```bash
cd .. && cd .. && cd db && touch .env
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

*  Copy the same `.env` file into the `./db` directory
```bash
cd && cd geospatial-portfolio-app && cd db && nano .env
```

* Run the data pipelines on your **local machine** to populate the database

* Run the Streamlit UI
```bash
cd && cd geospatial-portfolio-app && docker-compose up -d --build streamlit
```

* Domain and HTTPS

Point your domain to your Droplet’s IP address using your domain provider’s DNS (Namecheap) settings.

Do this by adding an A record where the host value is your subdomain and the value is your droplet IP address.

*You need to have a subdomain set up already for your application to work. You can do this by going to your domain registrar and adding an A record for your subdomain that points to your droplet IP address.*

![A record](images/subdomain.png)

*  Install and configure nginx
```bash
sudo apt update
sudo apt install nginx
```

* Check that nginx is running
```bash
systemctl status nginx
```

If the status is `active (running)`, then nginx is running. You can check by going to your droplet's IP address in your browser. You should see the nginx welcome page.

*  Set up `/etc/nginx/nginx.conf` as follows:
```bash
nano /etc/nginx/nginx.conf
```

Paste in the following:
```bash
user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
    # multi_accept on;
}

http {
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    ##
    # Basic Settings
    ##

    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # Logging Settings
    ##

    access_log /var/log/nginx/access.log;

    ##
    # Gzip Settings
    ##

    gzip on;

    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    ##
    # Virtual Host Configs
    ##

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

Hit `control + o` and then `Enter` to save and `control + x` to exit.

* Grant write permissions to the sites-available and sites-enabled folders using the following commands:
```bash
sudo chmod 777 /etc/nginx/sites-available
sudo chmod 777 /etc/nginx/sites-enabled
```

* Create a "streamlit-webservice" file for the routing configuration of Nginx
```bash
nano /etc/nginx/sites-available/streamlit-webservice
```

Paste in the following:
```bash
server {
    listen       80;
    server_name  ${droplet_ip}; # Domain name or IP address
    location / {
        proxy_pass http://0.0.0.0:8501/; # Route from HTTP port 80 to Streamlit port 8501
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
And replace `${droplet_ip}` with your droplet's IP address.

* Create a symlink
```bash
ln -s /etc/nginx/sites-available/streamlit-webservice /etc/nginx/sites-enabled/streamlit-webservice
```

* Restart nginx
```bash
sudo service nginx restart
sudo service nginx status
```

* Check that you can access the app in your browser at `http://{droplet_ip_address}:8501` and now at `http://{droplet_ip_address}` (without the port number it should be getting routed to the Streamlit app)

* Use an SSL certificate to enable HTTPS
```bash
sudo apt install certbot python3-certbot-nginx
```

```bash
sudo certbot --nginx -d ＜Domain＞
```

Replace `<Domain>` with your (sub)domain name. (ex: `geospatial.nathanjones.tech`)

* Update `/etc/nginx/sites-available/streamlit-webservice` to include your domain in the `server_name` directive.
```bash
server {
    listen       80;
    server_name  <Domain>; # Domain name or IP address
    location / {
        proxy_pass http://0.0.0.0:8501/; # Route from HTTP port 80 to Streamlit port 8501
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_http_version 1.1; # If you do not upgrade, the loading hangs
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/<Domain>/fullchain.pem; # Authenticate with a certificate from Certbot
    ssl_certificate_key /etc/letsencrypt/live/<Domain>/privkey.pem; # Authenticate with a certificate from Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

Replace `<Domain>` with your (sub)domain name. (ex: `geospatial.nathanjones.tech`)

* Modify `nginx.conf` as follows:
```bash
nano /etc/nginx/nginx.conf
```

Restart nginx
```bash
systemctl restart nginx
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


## 📚 App Tutorial <a name = "tutorial"></a>

<!-- Inline video from `images/geospatial_portfolio.mp4` -->
<video width="100%" height="100%" controls>
  <source src="images/geospatial_portfolio.mp4" type="video/mp4">



## 🗒️ TODO <a name = "todo"></a>

### In Progress

- [ ] Add `Getting Started` section to home page
- [ ] Add `Tutorials` section to home page

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

  #### Notes

  - [ ] Make Census GPT 
    - [ ] Store all of the census data in vector DB
    - [ ] Do Q/A over the data with LLM (ex: What is the most expensive Metro Area to rent in?)
    - [ ] Use the vector DB to create the maps
      - [ ] Make the LLM call the mapping functions

I followed the instructions from here to get rid of the port number in the URL
`https://www.alibabacloud.com/blog/using-lets-encrypt-to-enable-https-for-a-streamlit-web-service_600130`