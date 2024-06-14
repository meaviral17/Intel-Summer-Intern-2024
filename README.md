# Intel-Product Sentiment Analysis

## Overview
This project focuses on sentiment analysis of Intel product reviews scraped from Amazon. The sentiment analysis aims to categorize reviews as positive or negative based on the sentiment expressed in the text. The project utilizes web scraping techniques to collect the reviews, natural language processing (NLP) techniques for sentiment analysis, and data visualization for insights.

### Project Members: Garv Bhaskar, Aviral Srivastava, Dinesh Kumar
### Institution: Vellore Institute of Technology, Chennai

## Requirements
To run the project, ensure you have the following dependencies installed:
- Python 3.x
- Scrapy
- Beautiful Soup
- Pandas
- Matplotlib

## Usage
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Navigate to the `amazon` directory.
4. Run the following command to start the web scraping process:
   ```
   scrapy crawl amaze
   ```
5. The scraped data will be stored in `data.csv`.
6. Modify the `headers` variable in `amaze.py` located in the `spiders` folder if needed to ensure proper execution.
7. Analyze the sentiment distribution and trends using the provided Jupyter notebooks or Python scripts.

## File Structure
- `amazon`: Contains the Scrapy spider for web scraping.
  - `amazon/spiders/amaze.py`: Spider for scraping Amazon reviews.
- `data.csv`: CSV file containing the scraped data.
- `analysis.ipynb`: Jupyter notebook for data analysis and visualization.
- `requirements.txt`: File listing the project dependencies.

## Notes

- Verify your internet connection as Scrapy needs to access the web for scraping.

For further customization or troubleshooting, refer to the Scrapy and BeautifulSoup documentation.
