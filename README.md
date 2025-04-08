# **Eniac Sales Optimization via Strategic Discounts**


## **Purpose**
As part of Eniac’s ongoing effort to boost revenue through data-driven strategies, this project explores the **impact of discounts and product categorization on sales performance**. With a total revenue of **€7.8M** and strong seasonal spikes in demand, the goal is to develop a **discounting and product segmentation framework** that enhances sales performance without eroding margins.


### **Problem Statement:**
Eniac has observed fluctuations in sales that align more with seasonal events than with its discounting strategy. This raised the need to evaluate:

- How effective discounts are across different product types and price segments.
- Whether categorization by product type or price basket yields better strategic insight.
- How to structure data pipelines to monitor and optimize performance.


### **Solution:**
This analysis utilized sales data to:

- Categorize products by **price baskets** and **product types**.
- Quantify the impact of **seasonality** and **discount** levels on sales.
- Identify data pipeline improvements for better tracking of discounts, returns, and inventory.

The insights inform targeted marketing, pricing, and inventory strategies for sales optimization.



## **Summary**
This project evaluates Eniac’s discount strategy and categorization approaches using structured sales data. It provides insights into **revenue drivers**, highlights **seasonality trends**, and offers recommendations for refining the data pipeline to support smarter pricing and promotions.



## **Data Analysis & Findings**
### **1. Sales Performance by Price Basket**
  - All the products which were sold were grouped into different price baskets for effective categorization of products. 
  - Top 3 price baskets (Mid-range, Upper Mid-range, Premium) generated **~€6.2M**, about **79%** of total revenue.
  - Basket 4 (Upper Mid-range) alone generated **~€2.6M**, accounting for **31.6%** of total revenue.
  - Combined average discount for top baskets was around **17.0%**. 

  ![](/assets/Total_Revenue_Per_Price_Basket.png)


### **2. Sales Performance by Product Type**
  - **Categorizing sold products based on product type revealed patterns like:**
    - Higher responsiveness to discounts in some categories (e.g., accessories).
    - Others (e.g., laptops) showed volume stability independent of discounting.

  ![](/assets/Total_Revenue_Per_ProductType.png)


### **3.  Impact of Seasonality**
  - **Black Week** and **Christmas** dominate sales surges.
  - **Overall discounts showed limited effect** on revenue increases — external events were primary drivers.
  - However, within specific product categories, **targeted discounting drove high volumes**.

  ![](/assets/Impact_on_season.png)


### **4. Correlation Analysis**
To understand interdependencies between discount levels, product categories, seasonality, and revenue, a Pearson correlation matrix was used.
- **Key Observations**:
  - Revenue positively correlates with seasonal events, indicating event-driven sales surges.
  - Discount percentage shows a moderate correlation with sales volume but not with total revenue, suggesting discounts may be attracting buyers but not necessarily maximizing earnings.
  - Product type categories show distinct correlation patterns with revenue and discounts, reinforcing the value of segmentation.

  ![](/assets/corelation.png)

This analysis supports the need for targeted discount strategies rather than blanket promotions, emphasizing the role of category-specific behavior in strategic planning.


### **5.  Data Pipeline & Operational Gaps**
- **Current Issues Identified:**
  - Lack of defined product categories.
  - No tracking of promo prices or customer returns.
  - Poor metadata and inventory visibility.
- **Proposed Enhancements:**
  - Track discounts & promotions explicitly.
  - Centralize product metadata and category definitions.
  - Implement return/reason logging for customer feedback.
 


## **Key Learnings**
- **Strategic Categorization** is essential for actionable insights — both price and product type should be used in tandem.
- **Seasonality outweighs** discounting as a sales driver; however, **targeted discounting still boosts volume** in key areas.
- **Clean, structured data pipelines** are critical to support real-time marketing and inventory decisions.



## **Challenges Overcame**
- Lack of initial product categorization and promo tracking resolved via custom data processing.
- Revenue attribution by category required data joins and basket creation logic.
- Needed to infer discount effectiveness from fragmented metadata.
- Enhanced the framework for measuring sales impact per basket & category.



## **Additional Reflections**
- Greater automation of data enrichment (e.g., auto-categorization) would improve scalability.
- Strong product metadata hygiene is required to sustain ongoing performance analysis.
- Long-term benefit lies in centralized analytics dashboards tracking promo efficacy, seasonal peaks, and product-level ROI.


## **Repository Contents**
- **Presentation Slides:** Summary of findings, visualizations, and strategic takeaways.
- **Data Analysis Reports:** Data processing logic and metrics calculation.
- **README File:** Executive summary and key learnings.



## **Deployment & Contribution**
### **How to Use This Repository:**
1. Clone the repository:
   ```sh
   git clone https://github.com/hsjoi0214/eniac-discount-analysis.git
   ```
2. Navigate to the project folder:
   ```sh
   cd eniac-discount-analysis
   ```
3. View the presentation and analysis reports.


### **Contributions:**
- Suggestions on improving categorization logic or discount effectiveness models are welcome.
- Pull requests and issues are encouraged to further enrich the project.



## **Languages and Libraries Used**
- **Programming Languages:** Python
- **Tools:** VScode, Google Slides



## **Credits**
- **Data Sources:**
  - Eniac sales data.
- **Analysis Conducted by:** [Prakash Joshi]



## **Acknowledgements**

Thanks to my mentors for supporting the initiative and contributing to the refinement of discounting strategy and analytics pipeline.




