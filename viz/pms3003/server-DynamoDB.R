#install.packages("aws.dynamodb", repos = c(cloudyr = "http://cloudyr.github.io/drat", getOption("repos")))
#https://cran.r-project.org/web/packages/aws.ec2metadata/index.html

# load required libraries
library(shiny)
library(aws.dynamodb)
library(plotly)

# set up a server variable
server <- function(input, output, session) {
  
  # get data
  data <- get_table("pms3003")
  
  # define output object
  output$plot <- renderPlotly({
    
    # render a plot
    plot_ly(data,
            type = "scatter",
            mode = "lines", 
            x = ~dt,               
            y = ~pm1,
            name = "PM1"
    ) %>%
      
      # add pm2.5 line
      add_trace(x = ~dt,                                         
                y = ~pm25,  
                mode = "lines",
                name = "PM2,5"
      ) %>%
      
      # add pm10 line
      add_trace(x = ~dt,                                         
                y = ~pm10,  
                mode = 'lines', 
                name = "PM10"
      ) %>%
      
      # format titles
      layout(                  
        title = "Zanieczyszczenie powietrza",
        xaxis = list(         
          title = FALSE,
          type = "date"
        ),      
        yaxis = list(         
          title = "µg/m3")   
      )
  })
  
  # print latest data
  output$latest.data <- renderText({ paste("Ostatni pomiar wykonano ", 
                                           tail(data, 1)[1,1])})
  
}
