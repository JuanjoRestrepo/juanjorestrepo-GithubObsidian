
VAAQSA6AYBC3MW6LJFMT6XLM



# Qversity Telecom Analytics Report

  

## Table of Contents

1. [Introduction](#introduction)

2. [Customer Demographics](#customer-demographics)

- [Customer Status Distribution](#customer-status-distribution)

- [Geographic Distribution](#geographic-distribution)

- [Operator Distribution](#operator-distribution)

- [Age Distribution](#age-distribution)

3. [Financial Analysis](#financial-analysis)

- [Revenue by Plan Type](#revenue-by-plan-type)

- [Credit Score Segments](#credit-score-segments)

- [Revenue Distribution by Geography](#revenue-distribution-by-geography)

- [Top Customer Segments](#top-customer-segments)

4. [Product Analysis](#product-analysis)

- [Device Brand Popularity](#device-brand-popularity)

- [Service Popularity](#service-popularity)

- [Service Combinations](#service-combinations)

5. [Customer Behavior](#customer-behavior)

- [Credit vs Payment Behavior](#credit-vs-payment-behavior)

- [Pending Payments](#pending-payments)

6. [Acquisition Trends](#acquisition-trends)

- [Customer Acquisition by Operator](#customer-acquisition-by-operator)

- [New Customer Trends](#new-customer-trends)

7. [Conclusion](#conclusion)

8. [Appendix: SQL Queries](#appendix-sql-queries)

  

## Introduction

  

This report presents a comprehensive analysis of telecom customer data, processed through a medallion architecture (bronze → silver → gold) ETL pipeline. The data contains information about mobile customers including demographics, device usage, payment history, and service subscriptions. The analyses presented here are derived from the gold layer tables, which represent business-ready, aggregated data.

  

## Customer Demographics

  

### Customer Status Distribution

  

The customer base is fairly evenly distributed across three main status categories:

  

| Status | Customers | Percentage |

|-----------|-----------|------------|

| SUSPENDED | 1,589 | 33.69% |

| INACTIVE | 1,552 | 32.90% |

| ACTIVE | 1,533 | 32.50% |

| UNKNOWN | 43 | 0.91% |

  

```sql

SELECT * FROM gold.gold_customer_status_distribution;

```

  

**Analysis**: The distribution suggests that active customers represent only about a third of the total customer base. The high percentage of suspended and inactive customers (collectively 66.59%) indicates a significant opportunity for reactivation campaigns and churn prevention initiatives.

  

### Geographic Distribution

  

#### Distribution by Country

  

Customers are evenly distributed across five Latin American countries:

  

| Country | Customers |

|-----------|-----------|

| COLOMBIA | 964 |

| MEXICO | 962 |

| PERU | 953 |

| ARGENTINA | 920 |

| CHILE | 918 |

  

```sql

SELECT * FROM gold.gold_customer_distribution_by_country;

```

  

#### Distribution by City

  

The top 5 cities by customer count:

  

| City | Customers |

|----------|-----------|

| Cali | 636 |

| Lima | 280 |

| Arequipa | 252 |

| Bogota | 267 |

| Medellin | 265 |

  

```sql

SELECT * FROM gold.gold_customer_distribution_by_city ORDER BY customer_count DESC LIMIT 5;

```

  

**Analysis**: While the country distribution is fairly even, there's a significant concentration of customers in Cali, Colombia. This city represents 66% of all Colombian customers and approximately 12.7% of total customers. This suggests a stronghold in this market that could be leveraged for targeted promotions or as a test market for new services.

  

### Operator Distribution

  

Customers are distributed across four major operators:

  

| Operator | Customers |

|----------|-----------|

| CLARO | 1,211 |

| TIGO | 1,193 |

| WOM | 1,191 |

| MOVISTAR | 1,122 |

  

```sql

SELECT * FROM gold.gold_customer_distribution_by_operator;

```

  

**Analysis**: The market share is relatively balanced among the four operators, with CLARO having a slight lead. This suggests a competitive market with no single dominant player. The balanced distribution also indicates that the dataset provides a good representation of the overall market.

  

### Age Distribution

  

Age distribution by plan type reveals different preferences across age groups:

  

| Plan Type | Age Bucket | Customer Count |

|-----------|------------|----------------|

| PREPAGO | >50 | 754 |

| POSPAGO | >50 | 706 |

| CONTROL | >50 | 734 |

| POSPAGO | 30-50 | 532 |

| CONTROL | 30-50 | 510 |

| PREPAGO | 30-50 | 499 |

  

```sql

SELECT * FROM gold.gold_age_distribution_by_plan ORDER BY cnt DESC;

```

  

**Analysis**: Older customers (>50 years) show a preference for prepaid plans, possibly because of budget considerations or simpler usage patterns. The 30-50 age group is more likely to choose postpaid plans, which may be linked to higher data consumption or business usage.

  

## Financial Analysis

  

### Revenue by Plan Type

  

Average Revenue Per User (ARPU) by plan type:

  

| Plan Type | Users | Total Revenue | ARPU |

|-----------|-------|---------------|--------|

| PREPAGO | 1,564 | $120,654.94 | $77.15 |

| POSPAGO | 1,562 | $118,953.14 | $76.15 |

| CONTROL | 1,591 | $120,350.26 | $75.64 |

  

```sql

SELECT * FROM gold.gold_arpu_by_plan_type;

```

  

**Analysis**: ARPU is remarkably consistent across all plan types, with prepaid plans generating the highest average revenue. This contradicts the common industry assumption that postpaid customers generate higher ARPU. It suggests that pricing strategies across plans are well-balanced, or that prepaid customers are purchasing higher value top-ups.

  

Revenue statistics by plan type and operator:

  

| Plan Type | Operator | Avg Revenue | Median Revenue |

|-----------|----------|-------------|----------------|

| POSPAGO | MOVISTAR | $80.73 | $82.57 |

| PREPAGO | WOM | $79.73 | $77.64 |

| PREPAGO | TIGO | $79.26 | $80.05 |

| CONTROL | CLARO | $78.68 | $77.80 |

| POSPAGO | TIGO | $78.55 | $79.79 |

  

```sql

SELECT * FROM gold.gold_revenue_stats_by_plan_and_operator ORDER BY avg_revenue DESC;

```

  

**Analysis**: MOVISTAR is extracting the highest average revenue from postpaid customers, suggesting effective upselling or premium plan offerings. WOM and TIGO are performing well with prepaid customers, potentially due to attractive prepaid packages or promotions.

  

### Credit Score Segments

  

Distribution of customers by credit score segment:

  

| Credit Segment | Count | Average Score |

|----------------|-------|---------------|

| Bajo (<500) | 1,694 | 393.80 |

| Alto (650-799) | 1,309 | 724.68 |

| Medio (500-649)| 1,236 | 578.72 |

| Premium (≥800) | 478 | 825.92 |

  

```sql

SELECT * FROM gold.gold_credit_score_segments;

```

  

**Analysis**: The largest segment is customers with low credit scores, representing approximately 34% of the customer base. This suggests a need for secure payment methods and potentially deposit-based services for this segment. The premium segment, while smallest, represents the most financially reliable customers who might be targeted for high-value services.

  

### Revenue Distribution by Geography

  

Top 5 cities by revenue:

  

| Country | City | Revenue | Unique Customers |

|----------|--------------|-----------|------------------|

| PERU | Lima | $21,845.14| 280 |

| COLOMBIA | Bogota | $20,642.10| 267 |

| COLOMBIA | Medellin | $19,903.26| 265 |

| COLOMBIA | Cali | $18,639.86| 238 |

| PERU | Arequipa | $18,348.73| 252 |

  

```sql

SELECT * FROM gold.gold_revenue_distribution_by_geo ORDER BY revenue DESC LIMIT 5;

```

  

**Analysis**: Lima generates the highest total revenue despite not having the highest customer count. This suggests higher spending per customer in this city. Colombian cities (Bogota, Medellin, and Cali) are significant revenue contributors, making Colombia the most valuable country in the dataset despite the relatively even distribution of customers across countries.

  

### Top Customer Segments

  

Customers segmented by spending levels:

  

| Segment Rank | Customers | Avg Spent | Min Spent | Max Spent |

|--------------|-----------|-----------|-----------|-----------|

| 1 | 944 | $136.15 | $122.73 | $149.94 |

| 2 | 944 | $107.19 | $92.55 | $122.61 |

| 3 | 943 | $78.69 | $64.99 | $92.49 |

| 4 | 943 | $51.07 | $36.70 | $64.96 |

| 5 | 943 | $20.04 | -$99.58 | $36.64 |

  

```sql

SELECT * FROM gold.gold_top_customer_segments;

```

  

**Analysis**: The customer base is evenly divided into five spending segments. The top segment (approximately 20% of customers) spends an average of $136.15 per month, which is nearly 7 times higher than the lowest segment. The negative minimum spend in the lowest segment suggests refunds or credits applied to some accounts. This clear segmentation provides an opportunity for targeted marketing strategies based on spending capacity.

  

## Product Analysis

  

### Device Brand Popularity

  

Device brand distribution:

  

| Device Brand | Customers |

|--------------|-----------|

| Huawei | 1,182 |

| Samsung | 1,182 |

| Xiaomi | 1,174 |

| Apple | 1,179 |

  

```sql

SELECT * FROM gold.gold_device_brand_popularity;

```

  

**Analysis**: Device brand distribution is remarkably even, with no clear leader in the market. This suggests a highly competitive device market in the region. The relatively equal share of Apple devices compared to more affordable brands like Xiaomi and Huawei indicates a significant premium segment in the customer base.

  

Device brand preferences by plan type:

  

| Plan Type | Device Brand | Customer Count |

|-----------|--------------|----------------|

| CONTROL | Huawei | 416 |

| POSPAGO | Apple | 408 |

| CONTROL | Samsung | 401 |

| PREPAGO | Samsung | 400 |

| CONTROL | Xiaomi | 398 |

  

```sql

SELECT * FROM gold.gold_device_brand_by_plan ORDER BY customer_count DESC LIMIT 5;

```

  

**Analysis**: Huawei is most popular among control plan users, while Apple has the strongest presence in the postpaid segment. This aligns with the premium positioning of Apple and the value positioning of Huawei. The strong presence of Samsung across all plan types reflects its broad product range spanning different price points.

  

### Service Popularity

  

Popularity of different services:

  

| Service Name | Customers |

|---------------|-----------|

| INTERNATIONAL | 2,353 |

| VOICE | 2,336 |

| DATA | 2,321 |

| ROAMING | 2,319 |

| SMS | 2,318 |

  

```sql

SELECT * FROM gold.gold_service_popularity;

```

  

**Analysis**: International calling is the most popular service, closely followed by voice and data. The high adoption of international and roaming services suggests a customer base with significant international connections or travel needs. The similar adoption rates across all services indicate that most customers opt for comprehensive service packages rather than selecting individual services.

  

### Service Combinations

  

Most common service combinations:

  

| Service Combination | Count |

|---------------------------------|-------|

| ROAMING | 256 |

| INTERNATIONAL | 248 |

| DATA+INTERNATIONAL+ROAMING+VOICE| 239 |

| DATA+INTERNATIONAL+SMS+VOICE | 236 |

| DATA+ROAMING+SMS+VOICE | 236 |

  

```sql

SELECT * FROM gold.gold_service_combinations ORDER BY cnt DESC LIMIT 5;

```

  

**Analysis**: While standalone roaming and international services are the most common individual choices, a significant number of customers opt for comprehensive service bundles. The prevalence of 4-service combinations indicates potential for creating attractive bundled offerings that combine these popular services.

  

## Customer Behavior

  

### Credit vs Payment Behavior

  

Payment behavior by credit score segment:

  

| Credit Score Segment | Payment Status | Count |

|----------------------|----------------|-------|

| Bajo (<500) | PAID | 2,772 |

| Bajo (<500) | LATE | 2,640 |

| Bajo (<500) | FAILED | 2,567 |

| Bajo (<500) | PENDING | 2,530 |

| Medio-bajo (500-649) | FAILED | 1,972 |

  

```sql

SELECT * FROM gold.gold_credit_vs_payment_behavior ORDER BY cnt DESC LIMIT 5;

```

  

**Analysis**: Despite having low credit scores, the "Bajo" segment has the highest number of paid invoices, which challenges conventional assumptions about payment behavior. However, this segment also has significant counts of late, failed, and pending payments. This suggests that while these customers do make payments, their payment reliability is inconsistent. Targeted payment reminder systems and flexible payment options might improve collection rates for this segment.

  

### Pending Payments

  

Sample of pending payments:

  

| Customer ID | Payment Date | Amount |

|-------------|--------------|--------|

| 1184 | 2025-03-13 | $46.50 |

| 1232 | 2025-01-18 | $96.62 |

| 1451 | 2024-07-02 | $77.29 |

| 1482 | 2024-08-12 | $50.49 |

| 1482 | 2024-08-19 | (null) |

  

```sql

SELECT * FROM gold.gold_pending_payments LIMIT 5;

```

  

**Analysis**: The pending payments data shows varying amounts, with some customers having multiple pending payments. The presence of a null amount suggests incomplete invoice data for some transactions. The dates indicate some long-standing unpaid invoices from 2024, which may require special collection efforts or consideration for write-offs.

  

## Acquisition Trends

  

### Customer Acquisition by Operator

  

New customer acquisition by operator:

  

| Operator | Total New Customers |

|----------|---------------------|

| TIGO | 412 |

| CLARO | 381 |

| WOM | 373 |

| MOVISTAR | 363 |

  

```sql

SELECT * FROM gold.gold_acquisition_trends_by_operator;

```

  

**Analysis**: TIGO leads in customer acquisition, outperforming CLARO despite the latter having a larger overall customer base. This suggests TIGO has effective acquisition strategies or attractive introductory offers. MOVISTAR lags in new customer acquisition, which may indicate a focus on retention rather than acquisition, or challenges in attracting new customers.

  

### New Customer Trends

  

Monthly new customer trends for first 3 months (sample):

  

| Month | Operator | New Customers |

|-----------|----------|---------------|

| 2022-06 | MOVISTAR | 23 |

| 2022-06 | CLARO | 18 |

| 2022-06 | WOM | 21 |

| 2022-06 | TIGO | 15 |

| 2022-07 | WOM | 37 |

| 2022-07 | CLARO | 34 |

  

```sql

SELECT * FROM gold.gold_new_customer_trends_by_operator LIMIT 6;

```

  

**Analysis**: The data shows month-to-month variations in acquisition performance by operator. WOM shows strong growth from June to July 2022, nearly doubling their new customer count. This suggests successful promotional campaigns or expanded coverage during that period. Tracking these trends over time can provide insights into the effectiveness of marketing campaigns and the impact of competitive actions.

  

## Conclusion

  

The telecom dataset reveals a balanced market with four main operators competing across five Latin American countries. Key findings include:

  

1. **Customer Base**: The customer statuses are evenly distributed, with only about a third being active. This represents a significant opportunity for reactivation campaigns.

  

2. **Revenue Patterns**: Contrary to industry norms, prepaid plans show the highest ARPU, suggesting effective monetization of this segment. MOVISTAR extracts the highest revenue from postpaid customers.

  

3. **Geographic Insights**: While customers are evenly distributed across countries, Cali (Colombia) shows a significant concentration of customers. Lima (Peru) generates the highest revenue despite not having the highest customer count.

  

4. **Device Preferences**: The market is evenly split between four major device brands. Apple devices are most popular among postpaid customers, while Huawei leads in the control plan segment.

  

5. **Service Usage**: International calling is the most popular service, with many customers opting for comprehensive service bundles. This suggests opportunities for targeted bundle offerings.

  

6. **Credit and Payment Behavior**: Despite conventional wisdom, customers with low credit scores represent a large portion of paid invoices, though they also show inconsistent payment patterns.

  

7. **Acquisition Trends**: TIGO leads in new customer acquisition, outperforming CLARO despite the latter's larger overall customer base.

  

These insights provide a foundation for targeted marketing strategies, product development, and customer management initiatives. Further analysis could explore seasonal patterns, churn predictors, and lifetime value optimization.

  

## Appendix: SQL Queries

  

Below are the SQL queries used to generate the analytics presented in this report:

  

### Customer Demographics Queries

  

```sql

-- Customer Status Distribution

SELECT * FROM gold.gold_customer_status_distribution;

  

-- Customer Distribution by Country

SELECT * FROM gold.gold_customer_distribution_by_country;

  

-- Customer Distribution by City

SELECT * FROM gold.gold_customer_distribution_by_city ORDER BY customer_count DESC;

  

-- Customer Distribution by Operator

SELECT * FROM gold.gold_customer_distribution_by_operator;

  

-- Age Distribution by Plan

SELECT * FROM gold.gold_age_distribution_by_plan ORDER BY cnt DESC;

  

-- Age Distribution by Country and Operator

SELECT * FROM gold.gold_age_distribution_by_country_operator;

```

  

### Financial Analysis Queries

  

```sql

-- ARPU by Plan Type

SELECT * FROM gold.gold_arpu_by_plan_type;

  

-- Revenue Stats by Plan and Operator

SELECT * FROM gold.gold_revenue_stats_by_plan_and_operator ORDER BY avg_revenue DESC;

  

-- Credit Score Segments

SELECT * FROM gold.gold_credit_score_segments;

  

-- Revenue Distribution by Geography

SELECT * FROM gold.gold_revenue_distribution_by_geo ORDER BY revenue DESC;

  

-- Top Customer Segments

SELECT * FROM gold.gold_top_customer_segments;

```

  

### Product Analysis Queries

  

```sql

-- Device Brand Popularity

SELECT * FROM gold.gold_device_brand_popularity;

  

-- Device Brand by Plan

SELECT * FROM gold.gold_device_brand_by_plan ORDER BY customer_count DESC;

  

-- Device Brand by Country and Operator

SELECT * FROM gold.gold_device_brand_by_country_operator;

  

-- Service Popularity

SELECT * FROM gold.gold_service_popularity;

  

-- Service Combinations

SELECT * FROM gold.gold_service_combinations ORDER BY cnt DESC;

```

  

### Customer Behavior Queries

  

```sql

-- Credit vs Payment Behavior

SELECT * FROM gold.gold_credit_vs_payment_behavior ORDER BY cnt DESC;

  

-- Pending Payments

SELECT * FROM gold.gold_pending_payments;

```

  

### Acquisition Trends Queries

  

```sql

-- Customer Acquisition by Operator

SELECT * FROM gold.gold_acquisition_trends_by_operator;

  

-- New Customer Trends by Operator

SELECT * FROM gold.gold_new_customer_trends_by_operator;

```