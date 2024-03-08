# CS TradeR
CS Trade: Effortless Skin Trading with TradeBack.io. Trade skins seamlessly using CS Trade powered by TradeBack.io. Buy, sell, and exchange CS:GO skins effortlessly

## Table of Contents
* [Requirements](#requirements)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Setup](#setup)
  * [Customize filters.json](#customize-filters-as-needed)
  * [Install Cookie](#install-cookies)

## Requirements
* [CS Trade Account](https://cs.trade/)
* [Tradeback.io Account](https://tradeback.io/ru)


## Getting Started

### Installation
#### Install using pypi
```bash
pip install randomorph
```
or
* Clone the GitHub repository:
	```bash
	git clone https://github.com/soyll/RandoMorph.git	
	```
* Navigate to directory:
	```bash
	cd RandoMorph	
	```
* (Recommended) Create a virtual environment to manage Python packages for your project:
	```bash
	python3 -m venv venv
	```
* Activate the virtual enviropment
	* On windows:
		```bash
		.\venv\Scripts\activate
		```  
	* On linux or macOs:
		```
		source venv/bin/activate
		```
* Install the required Python packages from  `requirements.txt`:
	```bash
	pip install -r requirments.txt
	```
## Usage
```python
python controller.py
```
## Setup
#### Customize filters as needed
```json
{
    "MIN_PERCENT": ,
    "MAX_PERCENT": ,
    "MIN_PRICE": ,
    "MAX_PRICE": ,
    "MIN_COUNT": ,
    "APP_NUM": ,
    "SECOND_SERVICE": ,
    "STEAM_SALES_NUM": ,
    "CSTRADE_SALES_NUM": ,
    "AUTO_BUY": 
}
```
#### Install Cookies
* **CS-Trade** 
  * **Go to** [CS Trade](https://cs.trade/), **login** to your account, **press F12**, after opening the panel go to the "**Network**" tab, then click on "**stats.json**", open "**Headers**" and in the "**Cookie:**" list find "**PHPSESSID**" and fill **__cstrade** 
**Example**: *PHPSESSID=XXX*
* **Tradeback.io**
  * **Go to** [Tradeback.io](https://tradeback.io/), **login** to your account, **press F12**, after opening the panel go to the "**Network**" tab, then click on "**load?lang=ru**", open "**Headers**" and in the "**Cookie:**" list find "**session** and **remember_web**"  and fill **__steam** 
**Example**: *session=XXX; remember_web_XXX=YYY;*
*  **Selenium**
  * Take the remember_web_XXX values from Tradeback.io and fill in the template. 
```json
__selenium = {
  'name': 'remember_web_XXX',
  'value': 'VALUE_OF_REMEMBER_WEB_XXX'
}
```
