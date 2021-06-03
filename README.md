# Project Overview
## Project Description
**Will It Fit?** starts as a group project for the Le Wagon Berlin Data Science Bootcamp, batch 606. The initial pitch can be found [here](https://docs.google.com/presentation/d/e/2PACX-1vQfbjkibq4NNs7WjbxE9bvqmIKx-KpdwnLLpAKy1qnAkRI3a2uxIX60CbqAtQXPNRaCWtsYwS38s-fd/pub?start=false&loop=true&delayms=60000#slide=id.gdc7fe3dba0_1_122).
For the purposes of creating a minimum working product, the following components will be completed first (see more details below):
- [ ] User interface
- [ ] Web scraping module for IKEA package dimensions
- [ ] Volume optimization algorithm
- [ ] 3D interactive plot
  
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

*Section last updated 31/05/2021*

# Module Description
## IKEA Web Scraper (`scrapers/IKEA.py`)
* Receives list of article codes and article counts.
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
### Minimum requirements
* Assume ```IKEA_COUNTRY_DOMAIN``` and ```IKEA_WEBSITE_LANGUAGE``` are static to begin with (set in `params.py`).
* Efficiently (do not re-scrape existing ones, use database) scrape relevant country website and return required outputs.
### Potential further enhancements
* Ability to scrape other countries' websites.
* Inch/cm and pound/kg conversions.
* Also return URL to article as well as direct URL to one picture of article.
* ...

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
### Minimum requirements:
* First test if available volume is sufficient (vs. total volume of packages as well as in any single dimension vs. max value)
* Efficiently distribute space from ```[0][0][0]``` (assume bottom left front corner of trunk)
* Potential ideas:
    * After initial fit test, sort packages by overall volume descending, then recursively fill space.
    * Consider using a loss function that minimizes the number of empty "pockets": More small pockets should produce a bigger penalty than one large one.
    * [This](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.label.html) could maybe be used to identify and count pockets.
    * Use parameters defined in `params.py` to assign space.
    * Algorithm efficiency will be key for speed - might have to minimize use of loops and rely as much as possible on numpy-native functions, where available.
    * Consider [threading](https://realpython.com/intro-to-python-threading/) to run multiple possible solutions in parallel
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
### Minimum requirements:
* Plot available space and individual packages inside.
* Zoom and tilt must be available.
* Potential ideas:
    * Consider using [voxels](https://matplotlib.org/3.1.0/gallery/mplot3d/voxels.html) for plotting.
    * Ideally packages would have distinct colors - create appropriate color map in *params.py*.
### Potential further enhancements
* Add hover labels to packages.
* Add list next to plot. When user hovers over/clicks on article its location on plot is highlighted.
* Hover labels - include article name, link to article and small preview picture (would have to be buffered).

## User interface
* Website interface allowing the following user interactions:
    * User provides list and count of articles.
    * User selects from a (short) list of pre-defined cars (whose trunk size is known).
    * Interface returns visual representation of how packages would fit in trunk.
### Inputs
* By user:
    * Car make and model from selection box 
    * Upload user's IKEA wishlist pdf
    * List of article numbers and count of each
### Outputs
* Article list and counts: ```{article_code (str): item_count (int)} (dict)```

### Minimum requirements
* User can paste in a list of article numbers and respective counts, select a predefined car model and receives a plot in return.
* To be deployed in English only.
### Potential further enhancements
* Article data collection:
    * Log into IKEA website using user login details and extract shopping basket data directly.
* Language selection:
    * Offer interface in user language.
    * Initially hardcoded (see `params.py`) but could be pre-populated based on user location/browser language, with user ability to change.
* Car selection:
    * Instead of picking from scraped list of car models (limited utility), expand range - will require implementing additional modules (see below).
  
  

**The following module ideas are *enhancements*, to be tackled once the minimum working product is deployable.**

## Web scraping module for car dimensions
* Decide on best website, or combination of websites, to extract standardized car photos (side and back), exterior dimensions and trunk volume.
* Creation of database.

## Machine learning module to estimate trunk size
* Infer trunk location from position of wheels and doors.
* Use volume provided by manufacturer to validate model assumptions.

## User interface enhancements
* Allow user to take photo of car.
* Deployment as an app.

## Other scrapers
* Wayfair, MediaMarkt, ...

*Section last updated 31/05/2021*

# Change Log
* 03/06/2021: User interface section updated (proxvision)
* 02/06/2021: Removed superfluous sections
* 31/05/2021: Added space separators and additional info on optimizer (freichel)
* 30/05/2021: Created initial document (freichel)
