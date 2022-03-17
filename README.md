# Teradata Plugin

A collection of recipes that interface Teradata Vantage in-Database analytic tools to Dataiku users.


## Scope Of The Plugin

The Teradata plugin enhances Dataiku's built-in interaction capabilities with Teradata Vantage systems. The plugin provides visual recipes for scaled, in-Database Analytics with your Vantage data. The present version of the plugin features the following recipes:

* Analytic Functions - Data Transformation
* Analytic Functions - Time Series Analysis
* BYOM - Model Export to Vantage
* BYOM - Scoring
* SCRIPT Table Operator Analysis


## Requirements

Please see the [official plugin page](https://www.dataiku.com/product/plugins) for complete details.

To use the Teradata plugin:

* You will need access credentials to establish a connection to a target Vantage Advanced SQL Engine.
* To connect to a Vantage Advanced SQL Engine, the [Teradata JDBC Driver](https://downloads.teradata.com/download/connectivity/jdbc-driver). Version 16.20 or later is required.


## Installation

Please see the [official plugin page](https://www.dataiku.com/product/plugins) for complete details.

To install the Teradata plugin for Dataiku from a zip file on your client, perform the following:

1. Access the Dataiku Settings page through the **Admin Tools** button, and select the **Plugins** tab.
2. On the plugins page, go to the **ADD PLUGIN** menu on the top right, and click on the option **Upload**.
3. Click and navigate to the location of the plugin zip file in your local filesystemon **Choose File** and browse to the location of the present plugin zip file in your local filesystem.
4. If a previous installation of present plugin exists, then check the button next to the note about installing an update for an installed plugin.
5. Click on **UPLOAD** button.
6. Upon a successful upload, continue with building the plugin code environment. When the plugin is installed, you typically need to refresh the environment so that changes take effect. One way is to return to the plugins page and select the **INSTALLED** tab on the resulting screen. Then, push the **RELOAD ALL** button on the top right corner of the screen. Another way is to do a hard refresh by pushing (Ctrl + F5) on all open Dataiku browsers.


## References

For additional information, see the following links on docs.teradata.com:

1. [Teradata Vantage User Guide](https://docs.teradata.com/r/Teradata-VantageTM-User-Guide/March-2022).
2. [Advanced SQL Engine Analytic Functions Overview](https://docs.teradata.com/r/Teradata-VantageTM-Advanced-SQL-Engine-Analytic-Functions/July-2021/Introduction-to-Teradata-Vantage/Advanced-SQL-Engine-Analytic-Functions-Overview).
3. [Teradata Vantage Advanced SQL Engine Analytic Functions](https://docs.teradata.com/r/Teradata-VantageTM-Advanced-SQL-Engine-Analytic-Functions/July-2021).
4. [BYOM Documentation](https://docs.teradata.com/r/dLArVI09J62c8byzVbHMtw/9o1NRFSFme5IT151mSs2gw).
5. Teradata Orange Book Series: “R And Python Analytics with the SCRIPT Table Operator”. The direct [PDF link](https://docs.teradata.com/v/u/Orange-Book/R-and-Python-Analytics-with-SCRIPT-Table-Operator-Orange-Book-4.3.2) has restricted access to Teradata customers and partners; sign-in is needed.
