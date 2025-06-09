# Weibo Public Opinion Analysis: Sudden Event Case Study

This repository contains the code and resources for a study on **public opinion dynamics and topic shifts** in social media during sudden events.  
The case study focuses on the "**October 3 Thailand shooting**" and analyzes related Weibo posts collected within 24 hours before and after the event.

## Project Overview

The project explores how social media users respond to sudden events by analyzing:

- The **volume of discussion**
- **Emotional trends** over time
- **Topic transitions** during the incident

Data was collected using Python web crawlers and processed using text mining techniques, sentiment analysis, and dimensionality reduction for visualization.

## Key Methods

- **Data Collection and Preprocessing**
  - Crawled Weibo posts from 24 hours before and after the event
  - Cleaned and labeled using `pandas`

- **Text Mining and Analysis**
  - Sentiment analysis to track emotional changes over time
  - Topic trend tracking using TF-IDF and keyword extraction
  - Text vectorization with **TF-IDF**, followed by:
    - **Principal Component Analysis (PCA)**
    - **t-SNE** for dimensionality reduction and visualization



