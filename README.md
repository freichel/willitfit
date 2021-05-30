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

## Team Members
* [Katarzyna Cieslik](https://github.com/KasiaCieslik)
* [Tzu-Fan Tang](https://github.com/proxvision)
* [Dominik Wagner](https://github.com/domzae)
* [Florian Reichel](https://github.com/freichel)

*Section last updated 30/05/2021*

# Module Description
## IKEA Web Scraper (`scrapers/IKEA.py`)
* Receives list of article codes and article counts.
* Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
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
* Efficiently scrape relevant country website and return required outputs.
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
    x_start (int),
    y_start (int),
    z_start (int)
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
    x_start (int),
    y_start (int),
    z_start (int)
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
```diff
! Further alignment is needed in this section.
```
* Website interface allowing the following user interactions:
    * User provides list and count of articles.
    * User selects from a (short) list of pre-defined cars (whose trunk size is known).
    * Interface returns visual representation of how packages would fit in trunk.
### Inputs
* By user:
    * List of article numbers and count of each
    * Car
### Outputs
* Article list and counts: ```{article_code (str): item_count (int)} (dict)```
* Available volume: 3-dimensional numpy array (see `params.py`)
### Minimum requirements
* User can paste in a list of article numbers and respective counts, select a predefined car model and receives a plot in return.
* To be deployed in English only.
### Potential further enhancements
* Article data collection:
    * Instead of pasting in article data, allow user to upload printed PDF of shopping basket to parse using Regex.
    * Log into IKEA website using user login details and extract shopping basket data directly.
* Location/language selection:
    * Offer interface in user language.
    * Initially hardcoded (see `params.py`) but could be pre-populated based on user location/browser language, with user ability to change.
* Car selection:
    * Instead of picking from short list of car models (limited utility), expand range - will require implementing additional modules (see below).

**The following module ideas are *enhancements*, to be tackled once minimum working product is deployable.**

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

*Section last updated 30/05/2021*

# Change Log
* 30/05/2021: Created initial document

```diff
- The below was auto-created...will selectively remove soon.
```

# Data analysis
- Document here the project: willitfit
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for willitfit in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/willitfit`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "willitfit"
git remote add origin git@github.com:{group}/willitfit.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
willitfit-run
```

# Install

Go to `https://github.com/{group}/willitfit` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/willitfit.git
cd willitfit
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
willitfit-run
```
