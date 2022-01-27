Programming for Data Science

# **Real Estate Analysis**

Gonçalo Bastos1, Manuel Pinheiro2, Pedro Davide3 &amp; Ricardo Leça4

120201738; m20201738@novaims.unl.pt

220201742; m20201742@novaims.unl.pt

320201739; m20201739@novaims.unl.pt

420201747; m20201747@novaims.unl.pt

**Abstract**** :** The aim of this project was to better understand the Portuguese Real Estate Market. To accomplish this goal, data was collected from different sources, Real Estate data was scraped from SapoCasa and sociodemographic data from PorData. Data analysis techniques were performed to clean and transform the collected data, followed by a process of exploration and visualization of the data, which resulted in a geospatial analysis of data distribution across the country. Results confirmed &quot;common-sense&quot; understanding of the market (Lisbon, Porto and Faro as the most expensive districts; Littoral being generally more expensive than the Interior), but also provided some new insights such as Grândola being the Municipality where the ratio between property prices and average remuneration is the highest. Our analysis also revealed that Real Estate Market does not seem to be slowing down.

**Keywords** : Portuguese Real Estate; Web Scraping; Data Analysis; Geospatial Analysis.
**Statement of Contribution** : Every group member contributed to all work stages. However, Manuel Pinheiro was the main actor in Web Scraping; Pedro Davide was the responsible for data collection and cleaning from PorData; Gonçalo Bastos contributed for Data Transformation and Geospatial Analysis; Ricardo Leça explored visually the dataset. Regarding report writing, results and discussion, all group members contributed equally.

# a.Introduction

Real Estate markets are very complex systems. The price of Real Estate assets can be influenced by different factors such as location, area, number of bedrooms, sun exposure, construction date, and so on. This project was developed to better understand the dynamics and situation of the Portuguese Real Estate Market. Our analysis is focused on the two main residential property types: detached houses and apartments. To achieve this goal, first, web scraping techniques were applied to [SapoCasa](https://casa.sapo.pt/) using _Python_. Later, additional demographic data from [PorData](https://www.pordata.pt/)grouped by municipality was added to help complement the scraped data and create a more robust dataset. Data analysis techniques were applied to retrieve a clean dataset from raw data and lastly, visual exploration and geospatial analysis were conducted to better visualize and understand the dataset and extract new insights from it.

# b.Data

## c.Description

The data used in this project was collected from three main sources: SapoCasa website, PorData website and [Portal de Dados Abertos da Administração Pública](https://dados.gov.pt/pt/datasets/concelhos-de-portugal/). The following table, details the data used from the different sources:

| **Provider / Description** | **Content** |
| --- | --- |
| **SapoCasa** Real Estate data from municipalitiesFilename: alldata.csv | _link, municipality\_url, page\_num, condition, construction\_area, net\_area, district\_id, estate\_agent, municipality, price, floor\_area, type, municipality\_id, district_ |
| **PorData** Demographic data from municipalitiesFilename: pordata.csv | Purchasing Power, Population, Average Remuneration and Surface Area. |
| **Portal de Dados Abertos da Administração Pública** Filename: concelhos-shapefile.zip | Shapefile with geographic delimitation of Portuguese municipalities. |

The SapoCasa dataset contains properties details available when the scrapping was made in March 2021. After this procedure, the final dataset was filled with almost 130,000 properties for 278 municipalities. Demographic data from PorData was also included in this project with the main goal to enrich information about the municipalities beyond the properties. For the geospatial analysis, the two datasets were merged by _municipality\_id_, to obtain potential insights or relations between each municipality using demographic data.

## d.Extraction

Data extraction relied on two _Python_ scripts (_processing.py_ and _utils.py_). These scripts made use of a JSON file we obtained from SapoCasa&#39;s AJAX API which listed meta-data for all municipalities. The _utils.py_ file contains the main logic, while_processing.py_allowed us to control the flow of web scraping. This was necessary since we were scraping a large enough quantity of data that we ran into throttling and issues with being blocked by SapoCasa servers. In fact, this was a major impediment – we initially had a more elaborate scraping methodology (&#39;Plan A&#39;) implemented where we could get individual details for every listing, which resulted in a very rich dataset, with over a hundred features (many were categorical) for each listing. This process was, however, very intensive and performed one request per listing, which resulted in 25 times more requests than if we were to only scrape basic details (price, typology, areas and real estate agency), where we could get data on up to 25 records with a single request (&#39;Plan B&#39;). While we wanted to go through with Plan A, and tried several workarounds (different IP&#39;s, user-agents, etc.) the throttling was so intensive that the time each request was taking (north of 50 seconds at times) would not allow us to gather all data in a timely manner – this is when we were not being blocked. We ended up pivoting, and going with Plan B. This also played a role in the change of nature of our analysis to being on a more macro level (District/Municipality instead of single properties), which we complemented with additional geographical and demographical data (from PorData). Running the scripts mentioned above eventually resulted in over 5,000 .csv documents (one per scraped page), with most of them having information on 25 properties. These were then consolidated onto a single .csv file using a purpose-built Python function.

## e.Transformation

Data cleaning processes and techniques using the Python _Pandas_ library in a Jupyter Notebook were applied to the dataset obtained above. This stage allowed us to work the raw dataset, converting it into clean data which allowed us to better analyse and visualize it. Each feature was individually inspected for inconsistencies such as _Not a Number_ (NaN) values or simplifications. All transformations applied are depicted in the following table:

| **Transformation Target** | **Transformation Description** |
| --- | --- |
| Condition Variable | State of each property. Besides fixing some misclassifications, assumptions were made to obtain only four types of condition classification (Novo, Em construção, Usado, Renovado). |
| Link Variable | Despite us scraping only &#39;for sale&#39; properties, some rentals ended up in our dataset (misclassification errors by SapoCasa). These properties (496 instances) were dropped from the dataset. |
| Type Variable | We focused our analysis on properties of type between T0 and T6. All properties that are of type T#+# were converted to total number of divisions (for example, T1+1 was converted to a T2). |
| NaN Values | For numerical values, three main assumptions were made. 1) Properties with no price were dropped;2) all instances that have no area variables were dropped; 3) area missing values were filled with relative difference of median values (eg, if floor\_area&#39;s median value is 20% higher than net\_area&#39;s median value, then all NaN for those features were populated based on that median relative difference). |
| Outliers | Since kurtosis values were high, a measure of statistical dispersion was applied to drop extreme values. The measure applied was IQR and all instances that are outside of 1.5 x IQR scope are considered outliers, and, thus, removed. After removing outliers, we decided to cut off properties that are priced under 10,000 € and that have area variables under 20 m2, as these did not seem of interest for our analysis. |
| Dropped Variables | As a final step, and to obtain a final clean dataset to work with, we dropped some features that won&#39;t be used in our analysis: link, municipality\_url, page\_num, district\_id and estate\_agent. |

# f.Results and Discussion

We started with a global analysis in order to obtain insight on the Portuguese Real Estate Market based on several properties&#39; features such as price, construction area, typology, condition, etc. We started with a bar graph showing the number of properties available, to better understand the activity of the Real Estate Market in each district:

![](RackMultipart20220127-4-19i65h4_html_60e95f09a59a4a8b.png)

As expected, we verified that Lisboa, Porto and Faro have high Real Estate Market activity as each district has more than 20,000 properties for sale. In the first two districts, this number is explained because they are urban centers with high population density. In the Faro district, the high number of properties for sale could be related with high tourism activity/&quot;second-home&quot; properties. It was also noted that the Setúbal district is similar to the last ones, with a high number of properties. This might be justified by large urban areas within the Setúbal District in the &quot;Lisbon South Bay&quot;. In the opposite direction, the districts of Portalegre, Vila Real and Bragança have a small number of properties, suggesting little activity in the market. This could be explained because they are in Portugal&#39;s inland and have low population density and aged people. As for the properties condition, most are in used (_Usado_) condition:

| ![](RackMultipart20220127-4-19i65h4_html_35ca526e30ec4c9.png) | ![](RackMultipart20220127-4-19i65h4_html_ac8a0aad6c499564.png) |
| --- | --- |

It was interesting to note that there are almost as many properties marked as new (_Novo_) or in development (_Em construção_) in the market as there are properties marked as used or recovered (_Usado_ or _Recuperado_). This hints that there is a lot of activity in the housing market, as the stock of used properties (the cumulative construction of the last decades/centuries) would be expected to be much greater than that of new developments. The number of properties in _Recuperado_ condition is quite small when compared to the previous ones.

To finish this global overview, we analysed the distribution of typologies. We found there is a high number of properties with T2 and T3 typology and the values of T1 and T4 are very similar, as are the T0 and T5.

A trend was identified for property prices to increase as the number of divisions also increased. However, when the number of divisions reaches 4 (T4), the price starts to decrease. In fact, T5 and T6 are cheaper than T4, on average.

Regarding property prices, an analysis was made using a histogram and it was concluded that the largest number of properties is between 150,000€ and 200,000€. The obtained histogram suggested a right skewed representation.

It was also noticed, as expected, that where was a direct correlation between the net area and the construction area, with most properties having a construction area between 80m2 and 110m2.To finish this global analysis, a visual representation that joins the price of properties, their condition and their typology was made:

![](RackMultipart20220127-4-19i65h4_html_254985f0da96a431.png)

From the previous figure, it could be concluded (also as expected) that the used (_Usado)_ condition is cheaper on average. Conditions that are new or in construction (_Novo_ or _Em construção_) have identical prices on average. Properties that were in recovered (_Recuperado_) condition are slightly expensive than used properties. It&#39;s also interesting to note that T4 typology properties, particularly if they are recovered, are at a premium compared to all other property types, even newer or T5 and T6 typology properties.

We&#39;ll now focus our analysis on the districts previously identified as having the most or lest properties for sale (Lisboa, Faro, Porto and Portalegre, Vila Real and Bragança). The property condition in these districts also has a large number of used (_Usado_) condition. In the District of Lisboa, there were 24,839 properties on the market with an interval of prices between 100,000€ and 800,000€. Analysing all computed scatterplots, it was possible to infer that in Lisboa the mainly property types are T2 and T1 which are very homogenous in property condition in terms of price and net area, the latter being essentially between 50m2 and 120m2. In the district of Porto, the price range follows the minimum value for the Lisboa district, but the maximum value falls to 450,000€. The net area interval is essentially between 40m2 and 150m2. Another insight is that the _price_ bands for properties with the same _net area_ but different typologies seem to be more well defined in Porto than Lisboa, suggesting that the market in Porto is still not as pricey as in Lisbon (we&#39;d expect these to be very well defined in a balanced market). This might also hint that the prices in Porto are more homogenous and less sensitive to other factors such as location. Finally, in Faro district the price range of properties to sell is mainly between 150,000€ and 500,000€. The net area interval is between 50m2 and 150m2.Regarding the districts with lower Real Estate offer, we verified that: the Vila Real district has only 153 registered properties. The price range for the properties in this district is between 30,000€ and 220,000€, and the net area interval is between 80m2 and 200m2;The Portalegre district also has a low number of properties to sell - in this district, the properties price is essentially below 100,000€ with construction areas higher than the other districts; finally, in the district of Bragança, the properties are included in the price range between 25,000€ and 150,000€ with useful areas between 50m2 and 220m2. To summarize, we conclude that there is a difference between the number of properties to sell, price and areas between the coastal and inland districts.

To geo-visualise data, Portuguese municipalities delimitation through shapefiles and the PorData information were merged into a final dataset. Some heatmaps were plotted to visualise variables distribution across the country:

![](RackMultipart20220127-4-19i65h4_html_c96fc7e748f64e10.png) ![](RackMultipart20220127-4-19i65h4_html_5dac6a211ef6438e.png) ![](RackMultipart20220127-4-19i65h4_html_1fcac64045df2d90.png) ![](RackMultipart20220127-4-19i65h4_html_f8bf0e85176e05a0.png) ![](RackMultipart20220127-4-19i65h4_html_9e4f82e60dbfeafc.png)

Municipalities near the coast are more expensive than the ones located in the interior. Lisbon, Porto, and Faro districts are the ones that have higher average prices. Setubal is also one of the districts with highest values because it is influenced by luxury regions such as Troia and Comporta. Regarding_net area_, properties that have higher values are in the north and interior, such as Bragança and Portalegre districts. Regarding the price of a square meter, Lisbon shows the most valuable one, with 5,000€/m2, while municipalities in the interior are under 1,000€/m2. Grândola municipality shows a ratio between property price and monthly income above 500, which means, on average, a property price is 500 times higher than average monthly income. On the other hand, this ratio is lower in the interior of the country. Finally, Grândola municipality and municipalities surrounding it seem to have higher ratios between property price and population density (25,000€/px/km2), meaning that are wider territories with less population and high prices. On the contrary, all territories above Lisbon have a smaller ratio, meaning that there are more people living in smaller territories.

# g.Conclusions

This work allowed us to have a brief image of the current state of the Portuguese Real Estate market, as we applied web scraping techniques to collect data as of March 2021. Dealing with raw data directly from the web proved challenging because cleaning and transforming the dataset is not a linear process and we ended up with more than one hundred thousand records. The depth of our analysis was limited by the small number of features in our dataset. Despite this, we were still able to &quot;corroborate&quot; most obvious and common-sense results (e.g., Lisbon, Porto and Faro are the most expensive real estate markets; Littoral is more expensive than Interior – Aveiro and Viseu provide an interesting example). We also derived less obvious insights (e.g., Grândola has the highest PropertyPrice/Income ratio in the country due to the Comporta and Troia regions; in the North properties have larger net area values). We feel that this analysis could be improved by obtaining more features in the scraped data and potentially applying supervised and unsupervised learning methods to help derive new insights.
