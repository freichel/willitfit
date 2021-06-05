# Project Overview
## Project Description
**Will It Fit?** starts as a group project for the Le Wagon Berlin Data Science Bootcamp, batch 606. The initial pitch can be found [here](https://docs.google.com/presentation/d/e/2PACX-1vQfbjkibq4NNs7WjbxE9bvqmIKx-KpdwnLLpAKy1qnAkRI3a2uxIX60CbqAtQXPNRaCWtsYwS38s-fd/pub?start=false&loop=true&delayms=60000#slide=id.gdc7fe3dba0_1_122).
For the purposes of creating a minimum working product, the following components will be completed first (see more details below):
- [X] User interface
- [X] Web scraping module for IKEA package dimensions
- [X] Volume optimization algorithm
- [X] 3D interactive plot
  
After the minimum working product is complete, the above components will be refined further, both for speed and versatility. In addition, other potential components include (non-exhaustive list):
- [ ] Web scraping module (text and images) for car dimensions
- [ ] Machine Learning module to estimate car trunk size
- [ ] User interface enhancement allowing user to take photo of own vehicle (as opposed to manually inputing make and model)
- [ ] Inclusion of providers other than IKEA

## Links
* [Trello Board](https://trello.com/b/XFtR8y8M/willitfit)

## Team Members
* [Katarzyna Cieslik](https://github.com/KasiaCieslik)
* [Tzu-Fan Tang](https://github.com/proxvision)
* [Dominik Wagner](https://github.com/domzae)
* [Florian Reichel](https://github.com/freichel)

# Module Description
## User interface (`frontend/frontend.py`)
* Streamlit interface allowing the following user interactions:
    * User provides list and count of articles.
    * User selects from a list of pre-defined cars (whose trunk size is known).
    * Interface returns visual representation of how packages would fit in trunk after performing the following steps:
        * Parse PDF or article list into dictionary.
        * Obtain trunk volume array from car model database.
        * Pass article dict to IKEA website, get package dimensions for each article in a list returned.
        * Pass article dict and trunk space to optimizer, get filled trunk space and list of package coordinates returned.
        * Pass filled trunk space and list of package coordinates to plotter, receive plot.
### Inputs
* By user:
    * Car make and model from selection boxes
    * Upload user's IKEA wishlist pdf or specify article codes and counts
    * Choose if trunk should be plotted too
### Outputs
* 3D interactive plot in user interface. 
### Potential further enhancements
* Article data collection:
    * Log into IKEA website using user login details and extract shopping basket data directly.
* Language selection:
    * Offer interface in user language.
    * Initially hardcoded (see `params.py`) but could be pre-populated based on user location/browser language, with user ability to change.
* Car display:
    * Show picture of chosen car.

## IKEA Web Scraper (`scrapers/IKEA.py`)
* Receives dict of article codes and article counts.
* For existing articles:
  * Obtain relevant data from database.
* For new articles:
  * Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
  * Exports new articles into database.
* Returns list of package dimensions and weights.

![IKEA sample image](/resources/IKEA_sample_image.PNG)
### Inputs
* Article list and counts: ```{article_code (str): item_count (int)} (dict)```
* Country domain: ```IKEA_COUNTRY_DOMAIN (str)```
* Website language: ```IKEA_WEBSITE_LANGUAGE (str)```
### Outputs
* List of package dimensions and weights:
```
[(
    article_code (str),
    item_count (int),
    [(
        package_id (int),
        package_length (int),
        package_width (int),
        package_height (int),
        package_weight (float)
    )]
)] (list)
```
### Potential further enhancements
* Ability to scrape other countries' websites.
* Inch/cm and pound/kg conversions.
* Also return URL to article as well as direct URL to one picture of article.
* Non-cuboid packages.

## Volume Optimization Algorithm (`optimizers/volumeoptimizer.py`)
* Receives list of package dimensions, weights and counts
* Receives available volume
* Optimizes stacking of packages in available volume
* Returns 3D numeric representation of occupied space as well as article coordinates
### Inputs
* List of package dimensions and weights:
```
[(
    article_code (str),
    item_count (int),
    [(
        package_id (int),
        package_length (int),
        package_width (int),
        package_height (int),
        package_weight (float)
    )]
)] (list)
```
* Available volume: 3-dimensional numpy array, each element is 1cm (see `params.py`)
### Outputs
* Filled volume: 3-dimensional numpy array, each element is 1cm (see `params.py`)
* Article coordinates:
```
[
    article_code (str),
    article_id (int),
    package_id (int)
    x_start (int),
    y_start (int),
    z_start (int),
    x_end (int),
    y_end (int),
    z_end (int)
] (list)
```
### Potential further enhancements
* Train a machine learning model on a set of already-optimized configurations, eliminating the requirement for individual further optimizations.
* Include weight as a factor - heavier items should sit near the bottom.

## 3D Interactive Plot (`plotting/plotter.py`)
* Receives 3D numeric representation of occupied space as well as article coordinates
* Returns interactive 3D plot of packages
### Inputs
* Filled volume: 3-dimensional numpy array, each element is 1cm (see `params.py`)
* Article coordinates:
```
[
    article_code (str),
    article_id (int),
    package_id (int),
    x_start (int),
    y_start (int),
    z_start (int),
    x_end (int),
    y_end (int),
    z_end (int)
] (list)
```
### Outputs
* 3D interactive plot which can be displayed through user interface
### Potential further enhancements
* Add hover labels to packages.
* Add list next to plot. When user hovers over/clicks on article its location on plot is highlighted.
* Hover labels - include article name, link to article and small preview picture (would have to be buffered).

# Useful Commands
* `make install_requirements` resets Python virtual environment to only the packages defined in requirements.txt. It **removes all other packages**.
* `make start_app` starts the front-end on port 8501.
* `make docker_build img=IMAGE_NAME` builds a Docker image with the specified *IMAGE_NAME*.
* `make docker_run img=IMAGE_NAME` runs a Docker image locally with the specified *IMAGE_NAME*.
  
To be added:
  
* `make docker_build_run_deploy img=IMAGE_NAME mode=MODE` builds and then runs (*mode=local*) or deploys (*mode=GC*) the image with the specified *IMAGE_NAME*.

# Change Log
* 05/06/2021: Clean-up and added useful commands section (freichel)
* 03/06/2021: User interface section updated (proxvision)
* 02/06/2021: Removed superfluous sections
* 31/05/2021: Added space separators and additional info on optimizer (freichel)
* 30/05/2021: Created initial document (freichel)