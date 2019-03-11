library(shiny)
library(ggplot2)
library(dplyr)
library(plyr)
library(data.table)


data <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", stringsAsFactors = FALSE)

ui <- fluidPage(

  titlePanel("Mortality Rate"),
  sidebarLayout(
    sidebarPanel(
      uiOutput("StateOutput"),
      uiOutput("diseaseOutput")
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Plot", plotOutput("coolplot")),
        tabPanel("Table", tableOutput("results"))
      )
    )
  )
)
