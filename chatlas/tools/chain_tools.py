"""
Chainable tool utilities that combine data fetching with analysis
These tools demonstrate how to chain API calls with data processing
"""

from typing import List, Dict, Any, Optional
from . import data_utils

def extract_unique_categories(products_data: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique product categories from products data.
    This is a chainable tool that processes product data to get unique categories.

    Args:
        products_data: List of product dictionaries from API
    """
    try:
        if not products_data or (len(products_data) == 1 and "error" in products_data[0]):
            return ["No products data available"]

        # Extract unique categories using data utils
        categories = data_utils.get_unique_values(products_data, "category")
        return categories if categories else ["No categories found"]
    except Exception as e:
        return [f"Error extracting product categories: {str(e)}"]

def analyze_products_data(products_data: List[Dict[str, Any]], category_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze products data with statistical analysis.
    This is a general analysis tool that processes product data from any source.

    Args:
        products_data: List of product dictionaries from API
        category_filter: Optional category to filter by before analysis
    """
    try:
        if not products_data:
            return {"error": "No products data provided"}

        # Filter by category if specified
        if category_filter:
            products_data = data_utils.filter_data(products_data, {"category": category_filter})

        if not products_data:
            return {"error": f"No products found for category: {category_filter}"}

        # Analyze price statistics
        price_stats = data_utils.summarize_numeric_field(products_data, "price")

        # Count by category
        category_counts = data_utils.count_by_field(products_data, "category")

        # Count by brand
        brand_counts = data_utils.count_by_field(products_data, "brand", limit=10)

        return {
            "total_products": len(products_data),
            "price_analysis": price_stats,
            "category_breakdown": category_counts,
            "top_brands": brand_counts
        }
    except Exception as e:
        return {"error": f"Error analyzing products: {str(e)}"}

def analyze_customer_data(customers_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze customer distribution across different dimensions.
    This is a general analysis tool that processes customer data from any source.

    Args:
        customers_data: List of customer dictionaries from API
    """
    try:
        if not customers_data:
            return {"error": "No customers data provided"}

        # Analyze city distribution
        city_distribution = data_utils.count_by_field(customers_data, "city")

        # Analyze country distribution
        country_distribution = data_utils.count_by_field(customers_data, "country")

        return {
            "total_customers": len(customers_data),
            "city_distribution": city_distribution[:10],  # Top 10 cities
            "country_distribution": country_distribution,
            "unique_cities": len(data_utils.get_unique_values(customers_data, "city")),
            "unique_countries": len(data_utils.get_unique_values(customers_data, "country"))
        }
    except Exception as e:
        return {"error": f"Error analyzing customers: {str(e)}"}

def analyze_sales_data(sales_data: List[Dict[str, Any]], customer_filter: Optional[int] = None, product_filter: Optional[int] = None) -> Dict[str, Any]:
    """
    Analyze sales patterns from sales data.
    This is a general analysis tool that processes sales data from any source.

    Args:
        sales_data: List of sales dictionaries from API
        customer_filter: Filter by customer ID (optional)
        product_filter: Filter by product ID (optional)
    """
    try:
        if not sales_data:
            return {"error": "No sales data provided"}

        # Apply filters if specified
        filtered_sales = sales_data
        if customer_filter:
            filtered_sales = data_utils.filter_data(filtered_sales, {"customer_id": customer_filter})
        if product_filter:
            filtered_sales = data_utils.filter_data(filtered_sales, {"product_id": product_filter})

        if not filtered_sales:
            return {"error": "No sales data found matching the filters"}

        # Analyze transaction amounts
        amount_stats = data_utils.summarize_numeric_field(filtered_sales, "total_amount")

        # Analyze quantities
        quantity_stats = data_utils.summarize_numeric_field(filtered_sales, "quantity")

        # Group by customer if not filtered
        customer_analysis = None
        if not customer_filter:
            customer_analysis = data_utils.group_by_field(
                filtered_sales, "customer_id", "total_amount", "sum"
            )[:10]  # Top 10 customers

        # Group by product if not filtered
        product_analysis = None
        if not product_filter:
            product_analysis = data_utils.group_by_field(
                filtered_sales, "product_id", "total_amount", "sum"
            )[:10]  # Top 10 products

        return {
            "total_sales": len(filtered_sales),
            "amount_analysis": amount_stats,
            "quantity_analysis": quantity_stats,
            "top_customers_by_sales": customer_analysis,
            "top_products_by_sales": product_analysis
        }
    except Exception as e:
        return {"error": f"Error analyzing sales patterns: {str(e)}"}

def compare_categories(category_sales_data: Dict[str, Any], products_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare performance across different product categories.
    This combines category sales analytics with product details.

    Args:
        category_sales_data: Sales analytics data by category from API
        products_data: List of product dictionaries from API
    """
    try:
        if not category_sales_data or not products_data:
            return {"error": "Missing required data for category comparison"}

        # Analyze products per category
        products_per_category = data_utils.count_by_field(products_data, "category")

        # Analyze average price per category
        category_price_analysis = {}
        for category_info in products_per_category:
            category = category_info["value"]
            category_products = data_utils.filter_data(products_data, {"category": category})
            if category_products:
                price_stats = data_utils.summarize_numeric_field(category_products, "price")
                category_price_analysis[category] = {
                    "avg_price": price_stats.get("mean", 0),
                    "product_count": len(category_products),
                    "price_range": {
                        "min": price_stats.get("min", 0),
                        "max": price_stats.get("max", 0)
                    }
                }

        return {
            "sales_performance": category_sales_data,
            "product_distribution": products_per_category,
            "pricing_analysis": category_price_analysis
        }
    except Exception as e:
        return {"error": f"Error comparing category performance: {str(e)}"}

def generate_insights(summary_data: Dict[str, Any], top_customers_data: Dict[str, Any],
                     top_products_data: Dict[str, Any], category_data: Dict[str, Any],
                     weekend_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive business insights by combining multiple analytics data sources.
    This is a high-level tool that combines various analytics data.

    Args:
        summary_data: Sales summary data from API
        top_customers_data: Top customers data from API
        top_products_data: Top products data from API
        category_data: Category performance data from API
        weekend_data: Weekend vs weekday analysis from API
    """
    try:
        # Combine into comprehensive insights
        insights = {
            "business_summary": summary_data,
            "top_performers": {
                "customers": top_customers_data,
                "products": top_products_data
            },
            "category_insights": category_data,
            "temporal_patterns": weekend_data
        }

        # Add derived insights
        insights["derived_insights"] = []

        # Analyze summary data if available
        if isinstance(summary_data, dict) and "total_sales" in summary_data:
            if summary_data["total_sales"] > 100000:
                insights["derived_insights"].append("Strong overall sales performance")

            if summary_data.get("average_order_value", 0) > 50:
                insights["derived_insights"].append("High average order value indicates quality customers")

        return insights
    except Exception as e:
        return {"error": f"Error generating business insights: {str(e)}"}