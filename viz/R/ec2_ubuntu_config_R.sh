sudo apt-get update
sudo apt-get install r-base  
sudo apt-get install r-base-dev

sudo apt-get -y install libcurl4-openssl-dev
sudo apt-get -y install libssl-dev 
sudo apt-get -y install libmariadb-client-lgpl-dev

sudo su - -c "R -e \"install.packages('shiny', repos = 'http://cran.rstudio.com/')\""
sudo su - -c "R -e \"install.packages('RMySQL', repos = 'http://cran.rstudio.com/')\""
sudo su - -c "R -e \"install.packages('DBI', repos = 'http://cran.rstudio.com/')\""
sudo su - -c "R -e \"install.packages('plotly', repos = 'http://cran.rstudio.com/')\""

wget https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.4.4.807-amd64.deb
sudo dpkg -i shiny-server-1.4.4.807-amd64.deb
