"""
Data analysis utilities for processing and summarizing data
These tools can be chained together for complex analysis workflows
"""

from typing import List, Dict, Any, Set, Union, Optional
from collections import Counter
import statistics

def get_unique_values(data: List[Dict[str, Any]], field: str) -> List[Any]:
    """
    Extract unique values from a specific field in a list of dictionaries.

    Args:
        data: List of dictionaries containing the data
        field: Field name to extract unique values from
    """
    try:
        if not data or not isinstance(data, list):
            return []

        values = []
        for item in data:
            if isinstance(item, dict) and field in item:
                value = item[field]
                if value is not None and value not in values:
                    values.append(value)

        return sorted(values) if values else []
    except Exception as e:
        return [f"Error extracting unique values: {str(e)}"]

def summarize_numeric_field(data: List[Dict[str, Any]], field: str) -> Dict[str, Any]:
    """
    Generate summary statistics for a numeric field.

    Args:
        data: List of dictionaries containing the data
        field: Numeric field name to analyze
    """
    try:
        if not data or not isinstance(data, list):
            return {"error": "Invalid data format"}

        values = []
        for item in data:
            if isinstance(item, dict) and field in item:
                value = item[field]
                if isinstance(value, (int, float)) and value is not None:
                    values.append(value)

        if not values:
            return {"error": f"No numeric values found for field '{field}'"}

        return {
            "field": field,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "sum": sum(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0
        }
    except Exception as e:
        return {"error": f"Error summarizing numeric field: {str(e)}"}

def count_by_field(data: List[Dict[str, Any]], field: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Count occurrences of values in a specific field.

    Args:
        data: List of dictionaries containing the data
        field: Field name to count values for
        limit: Maximum number of results to return (optional)
    """
    try:
        if not data or not isinstance(data, list):
            return [{"error": "Invalid data format"}]

        values = []
        for item in data:
            if isinstance(item, dict) and field in item:
                value = item[field]
                if value is not None:
                    values.append(str(value))

        if not values:
            return [{"error": f"No values found for field '{field}'"}]

        # Count occurrences
        counter = Counter(values)
        results = [
            {"value": value, "count": count}
            for value, count in counter.most_common(limit)
        ]

        return results
    except Exception as e:
        return [{"error": f"Error counting field values: {str(e)}"}]

def filter_data(data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter data based on field conditions.

    Args:
        data: List of dictionaries containing the data
        filters: Dictionary of field_name: value pairs to filter by
    """
    try:
        if not data or not isinstance(data, list):
            return [{"error": "Invalid data format"}]

        if not filters:
            return data

        filtered_data = []
        for item in data:
            if not isinstance(item, dict):
                continue

            matches = True
            for field, expected_value in filters.items():
                item_value = item.get(field)

                # Handle different comparison types
                if isinstance(expected_value, dict):
                    # Range or comparison filters like {"min": 10, "max": 100}
                    if "min" in expected_value and item_value < expected_value["min"]:
                        matches = False
                        break
                    if "max" in expected_value and item_value > expected_value["max"]:
                        matches = False
                        break
                else:
                    # Exact match or contains
                    if isinstance(item_value, str) and isinstance(expected_value, str):
                        if expected_value.lower() not in item_value.lower():
                            matches = False
                            break
                    elif item_value != expected_value:
                        matches = False
                        break

            if matches:
                filtered_data.append(item)

        return filtered_data
    except Exception as e:
        return [{"error": f"Error filtering data: {str(e)}"}]

def group_by_field(data: List[Dict[str, Any]], group_field: str,
                  agg_field: Optional[str] = None, agg_func: str = "count") -> List[Dict[str, Any]]:
    """
    Group data by a field and optionally aggregate another field.

    Args:
        data: List of dictionaries containing the data
        group_field: Field to group by
        agg_field: Field to aggregate (optional, required for sum/avg/min/max)
        agg_func: Aggregation function (count, sum, avg, min, max)
    """
    try:
        if not data or not isinstance(data, list):
            return [{"error": "Invalid data format"}]

        groups = {}

        for item in data:
            if not isinstance(item, dict) or group_field not in item:
                continue

            group_key = str(item[group_field])

            if group_key not in groups:
                groups[group_key] = []

            groups[group_key].append(item)

        results = []
        for group_value, group_items in groups.items():
            result = {"group": group_value, "count": len(group_items)}

            if agg_func != "count" and agg_field:
                numeric_values = []
                for item in group_items:
                    if agg_field in item and isinstance(item[agg_field], (int, float)):
                        numeric_values.append(item[agg_field])

                if numeric_values:
                    if agg_func == "sum":
                        result["sum"] = sum(numeric_values)
                    elif agg_func == "avg":
                        result["avg"] = statistics.mean(numeric_values)
                    elif agg_func == "min":
                        result["min"] = min(numeric_values)
                    elif agg_func == "max":
                        result["max"] = max(numeric_values)

            results.append(result)

        # Sort by count descending
        return sorted(results, key=lambda x: x["count"], reverse=True)
    except Exception as e:
        return [{"error": f"Error grouping data: {str(e)}"}]

def sort_data(data: List[Dict[str, Any]], sort_field: str, descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sort data by a specific field.

    Args:
        data: List of dictionaries containing the data
        sort_field: Field to sort by
        descending: Sort in descending order (default: True)
    """
    try:
        if not data or not isinstance(data, list):
            return [{"error": "Invalid data format"}]

        # Filter out items that don't have the sort field
        valid_items = [item for item in data if isinstance(item, dict) and sort_field in item]

        if not valid_items:
            return [{"error": f"No items found with field '{sort_field}'"}]

        return sorted(valid_items, key=lambda x: x[sort_field] or 0, reverse=descending)
    except Exception as e:
        return [{"error": f"Error sorting data: {str(e)}"}]