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
- [ ] Machine Learning module to model car trunk size
- [ ] User interface enhancement allowing user to take photo of own vehicle (as opposed to manually inputing make and model)
- [ ] Inclusion of providers other than IKEA

## Team Members
* [Katarzyna Cieslik](https://github.com/KasiaCieslik)
* [Tzu-Fan Tang](https://github.com/proxvision)
* [Dominik Wagner](https://github.com/domzae)
* [Florian Reichel](https://github.com/freichel)

*Section last updated 30/05/2021*

# Module Description
## IKEA Web Scraper (*scrapers/IKEA.py*)
* Receives list of article codes and article counts.
* Scrapes IKEA website to obtain package dimensions (rounded up to next cm), weights (in kg rounded up 2 decimals) and counts.
* Returns list of package dimensions and weights.
![IKEA sample image](/resources/IKEA_sample_image.PNG)
### Inputs
* Dict: ```{article_code (str): item_count (int)}```
### Outputs
* List of tuples: ```[(
    article_code (str),
    item_count (int),
    [(
        package_id (int),
        package_length (int),
        package_width (int),
        package_height (int),
        package_weight (float)
    )]
    )]```

# Change Log
* 30/05/2021: Created initial document

<span style="color:red">The below was auto-created...will selectively remove soon.</span>

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
