# load required libraries
library(shiny)
library(DBI)
library(plotly)

# set up a server variable
server <- function(input, output, session) {
  
  # set up mysql connectivity
  conn <- dbConnect(
    drv = RMySQL::MySQL(),
    host='xxx',
    user='xxx',
    password='xxx',
    dbname='xxx',
    port=3306)
  on.exit(dbDisconnect(conn), add = TRUE)
  
  # produce a query
  query <- paste0("select dt, pm1, pm25, pm10 from fct_pm")
  
  # store retrieved data
  data <- dbGetQuery(conn, query)
  
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
