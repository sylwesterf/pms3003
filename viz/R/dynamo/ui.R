# load required libraries
library(shiny)
library(plotly)

# set up an ui variable
ui <- fluidPage(
  
  br(),
  # output a plotly plot
  plotlyOutput("plot"),
  
  br(),
  h6(textOutput('latest.data'))
  
)
