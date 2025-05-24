# FF-Industry-Parser
A lightweight Python class to parse and work with Fama-French industry classification text files, including mapping SIC codes to Fama-French industry codes.

## Features
- Parses structured industry definitions in Fama-French format

- Supports mapping of individual SIC codes to Fama-French industry codes

## Dependencies
- Python ≥ 3.7
- No external packages needed (only `re`)

## Usage
```{python}
from ff_industry_parser import FFIndustryParser

# The txt file is from https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_49_ind_port.html
with open("Siccodes49.txt", "r") as f:
    text = f.read()
parser = FFIndustryParser(text)
# Map SIC to FF industry code
ff_code = parser.map_sic(2050)
# Get full parsed structure
industry_dict = parser.get_dict()
```

