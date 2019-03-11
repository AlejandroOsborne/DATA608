#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggplot2)
library(dplyr)
library(googleVis)

data <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", stringsAsFactors = FALSE)


ui <- fluidPage(
  
  titlePanel("Mortality Rate"),
  sidebarLayout(
    sidebarPanel(
      uiOutput("YearOutput"),
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
