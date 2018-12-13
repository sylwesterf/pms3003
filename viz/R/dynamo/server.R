# load required libraries
library(shiny)
library(aws.dynamodb)
library(plotly)
library(rPython)

# set up a server variable
server <- function(input, output, session) {
  
  # get data
  python.load("dynamodb-python.py")
  data <- as.data.frame(python.get('df'))
  
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
