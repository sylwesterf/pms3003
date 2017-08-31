# load required libraries
library(shiny)
library(DBI)
library(plotly)

# set up an ui variable
ui <- fluidPage(

  # output a plotly plot
  plotlyOutput("plot")
  
)
