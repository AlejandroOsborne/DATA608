library(shiny)
library(ggplot2)
library(dplyr)
library(plyr)
library(data.table)

data <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", stringsAsFactors = FALSE)

server <- function(input, output) {
  
  agdata <- aggregate(data$Population, by=list(data$ICD.Chapter,data$Year), FUN=sum)
  names(agdata) <-c("ICD.Chapter","Year","NatPopulation")
  
  data <- inner_join(data, agdata)
  data$NatAvg <- (data$Deaths/data$NatPopulation)*100000
  
  output$StateOutput <- renderUI({
    selectInput("StateInput", "State", sort(unique(data$State)), selected = "AL")  })
  
  output$diseaseOutput <- renderUI({
    selectInput("diseaseInput", "Disease", sort(unique(data$ICD.Chapter)), selected = "Certain infectious and parasitic diseases")  })
  
  filtered <- reactive({
    if (is.null(input$StateInput)) {return(NULL) }    
    if (is.null(input$diseaseInput)) {return(NULL) }    
    
    data %>%
      filter(
        State == input$StateInput, ICD.Chapter == input$diseaseInput
      )
  })

  output$coolplot <- renderPlot({
    if (is.null(filtered())) {
      return()
    }
    
    ggplot(filtered(), aes(x=(Year), y=NatAvg)) + 
      geom_bar(stat="identity", aes(fill=NatAvg), fill = "#FF6666") 
    
  })
  
  output$results <- renderTable({  filtered() })
  
}