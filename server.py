from mcp.server.fastmcp import FastMCP
import json
from typing import List, Optional, Union, Dict, Any

mcp = FastMCP("ChartJS")

# Color palettes for easy chart styling
COLOR_PALETTES = {
    "vibrant": [
        "rgba(255, 99, 132, 0.8)", "rgba(54, 162, 235, 0.8)", "rgba(255, 206, 86, 0.8)",
        "rgba(75, 192, 192, 0.8)", "rgba(153, 102, 255, 0.8)", "rgba(255, 159, 64, 0.8)",
        "rgba(199, 199, 199, 0.8)", "rgba(83, 102, 255, 0.8)", "rgba(255, 99, 255, 0.8)"
    ],
    "pastel": [
        "rgba(255, 179, 186, 0.8)", "rgba(186, 225, 255, 0.8)", "rgba(255, 223, 186, 0.8)",
        "rgba(186, 255, 201, 0.8)", "rgba(220, 186, 255, 0.8)", "rgba(255, 218, 193, 0.8)"
    ],
    "professional": [
        "rgba(41, 128, 185, 0.8)", "rgba(52, 152, 219, 0.8)", "rgba(155, 89, 182, 0.8)",
        "rgba(142, 68, 173, 0.8)", "rgba(22, 160, 133, 0.8)", "rgba(26, 188, 156, 0.8)"
    ],
    "earth": [
        "rgba(139, 69, 19, 0.8)", "rgba(160, 82, 45, 0.8)", "rgba(205, 133, 63, 0.8)",
        "rgba(210, 180, 140, 0.8)", "rgba(188, 143, 143, 0.8)", "rgba(165, 42, 42, 0.8)"
    ]
}

@mcp.tool()
def create_chart_config(
    chart_type: str,
    labels: List[str],
    datasets: List[Dict[str, Any]],
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a Chart.js configuration object as a JSON string.
    
    Args:
        chart_type: The type of chart (bar, line, pie, doughnut, radar, polarArea, bubble, scatter).
        labels: List of labels for the x-axis (or equivalent).
        datasets: List of dataset objects. Each dataset should have 'label' and 'data'.
        options: Optional configuration options for the chart.
    """
    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": options or {}
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_pie_chart(
    labels: List[str],
    data: List[Union[int, float]],
    title: str = "Pie Chart",
    color_palette: str = "vibrant"
) -> str:
    """
    Create a pie chart configuration.
    
    Args:
        labels: List of labels for each slice.
        data: List of values for each slice.
        title: Chart title.
        color_palette: Color palette (vibrant, pastel, professional, earth).
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    config = {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)],
                "borderWidth": 2,
                "borderColor": "#fff"
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "position": "bottom"
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_doughnut_chart(
    labels: List[str],
    data: List[Union[int, float]],
    title: str = "Doughnut Chart",
    color_palette: str = "vibrant",
    cutout_percentage: int = 50
) -> str:
    """
    Create a doughnut chart configuration.
    
    Args:
        labels: List of labels for each slice.
        data: List of values for each slice.
        title: Chart title.
        color_palette: Color palette (vibrant, pastel, professional, earth).
        cutout_percentage: Percentage of the chart cut out (0-100).
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    config = {
        "type": "doughnut",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)],
                "borderWidth": 2,
                "borderColor": "#fff"
            }]
        },
        "options": {
            "responsive": True,
            "cutout": f"{cutout_percentage}%",
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "position": "bottom"
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_bar_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Bar Chart",
    stacked: bool = False,
    horizontal: bool = False
) -> str:
    """
    Create a bar chart configuration.
    
    Args:
        labels: List of labels for the x-axis.
        datasets: List of datasets, each with 'label' and 'data'.
        title: Chart title.
        stacked: Whether to stack the bars.
        horizontal: Whether to make horizontal bars.
    """
    chart_type = "bar" if not horizontal else "horizontalBar"
    
    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "x": {"stacked": stacked},
                "y": {"stacked": stacked, "beginAtZero": True}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_line_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Line Chart",
    smooth: bool = True,
    fill: bool = False
) -> str:
    """
    Create a line chart configuration.
    
    Args:
        labels: List of labels for the x-axis.
        datasets: List of datasets, each with 'label' and 'data'.
        title: Chart title.
        smooth: Whether to smooth the lines (tension).
        fill: Whether to fill the area under the line.
    """
    # Apply tension and fill to all datasets
    for dataset in datasets:
        if "tension" not in dataset:
            dataset["tension"] = 0.4 if smooth else 0
        if "fill" not in dataset:
            dataset["fill"] = fill
    
    config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "y": {"beginAtZero": True}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_radar_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Radar Chart"
) -> str:
    """
    Create a radar chart configuration.
    
    Args:
        labels: List of labels for each axis.
        datasets: List of datasets, each with 'label' and 'data'.
        title: Chart title.
    """
    config = {
        "type": "radar",
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "r": {
                    "beginAtZero": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_polar_area_chart(
    labels: List[str],
    data: List[Union[int, float]],
    title: str = "Polar Area Chart",
    color_palette: str = "vibrant"
) -> str:
    """
    Create a polar area chart configuration.
    
    Args:
        labels: List of labels for each segment.
        data: List of values for each segment.
        title: Chart title.
        color_palette: Color palette (vibrant, pastel, professional, earth).
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])
    
    config = {
        "type": "polarArea",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)]
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "position": "bottom"
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_scatter_chart(
    datasets: List[Dict[str, Any]],
    title: str = "Scatter Chart"
) -> str:
    """
    Create a scatter chart configuration.
    
    Args:
        datasets: List of datasets with 'label' and 'data' (array of {x, y} objects).
        title: Chart title.
    """
    config = {
        "type": "scatter",
        "data": {
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "x": {
                    "type": "linear",
                    "position": "bottom"
                },
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_bubble_chart(
    datasets: List[Dict[str, Any]],
    title: str = "Bubble Chart"
) -> str:
    """
    Create a bubble chart configuration.
    
    Args:
        datasets: List of datasets with 'label' and 'data' (array of {x, y, r} objects).
        title: Chart title.
    """
    config = {
        "type": "bubble",
        "data": {
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "x": {
                    "type": "linear",
                    "position": "bottom"
                },
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_mixed_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Mixed Chart"
) -> str:
    """
    Create a mixed chart with multiple chart types.
    
    Args:
        labels: List of labels for the x-axis.
        datasets: List of datasets, each with 'type', 'label', and 'data'.
        title: Chart title.
    """
    config = {
        "type": "bar",  # Default type
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "y": {"beginAtZero": True}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_chart_html(
    chart_type: str,
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "My Chart",
    options: Optional[Dict[str, Any]] = None,
    width: str = "800px",
    height: str = "500px",
    theme: str = "light"
) -> str:
    """
    Generate a full HTML page with Chart.js included to render the specified chart.
    
    Args:
        chart_type: The type of chart.
        labels: List of labels for the data points.
        datasets: List of dataset objects.
        title: The title displayed in the HTML page.
        options: Chart.js options.
        width: CSS width of the chart container.
        height: CSS height of the chart container.
        theme: Theme (light or dark).
    """
    bg_color = "#ffffff" if theme == "light" else "#1a1a1a"
    text_color = "#333333" if theme == "light" else "#e0e0e0"
    
    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": options or {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "color": text_color,
                    "font": {"size": 20}
                },
                "legend": {
                    "labels": {
                        "color": text_color
                    }
                }
            }
        }
    }
    
    config_json = json.dumps(config, indent=2)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: {bg_color};
            color: {text_color};
            padding: 20px;
            margin: 0;
        }}
        .chart-container {{
            position: relative;
            margin: auto;
            height: {height};
            width: {width};
            background: {bg_color};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {config_json});
    </script>
</body>
</html>"""
    return html

@mcp.tool()
def get_chart_templates() -> str:
    """
    Return common Chart.js templates and examples for inspiration.
    """
    templates = {
        "bar": {
            "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            "datasets": [{
                "label": "# of Votes",
                "data": [12, 19, 3, 5, 2, 3],
                "backgroundColor": COLOR_PALETTES["vibrant"]
            }]
        },
        "line": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "datasets": [{
                "label": "Monthly Sales",
                "data": [65, 59, 80, 81, 56, 55],
                "borderColor": "rgb(75, 192, 192)",
                "tension": 0.4
            }]
        },
        "pie": {
            "labels": ["Chrome", "Firefox", "Safari", "Edge", "Other"],
            "datasets": [{
                "data": [60, 20, 10, 5, 5],
                "backgroundColor": COLOR_PALETTES["professional"]
            }]
        },
        "radar": {
            "labels": ["Speed", "Reliability", "Comfort", "Safety", "Efficiency"],
            "datasets": [{
                "label": "Product A",
                "data": [80, 90, 70, 85, 75],
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgb(54, 162, 235)"
            }]
        }
    }
    return json.dumps(templates, indent=2)

@mcp.tool()
def get_color_palettes() -> str:
    """
    Return available color palettes for charts.
    """
    return json.dumps(COLOR_PALETTES, indent=2)

@mcp.tool()
def create_area_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Area Chart",
    stacked: bool = False
) -> str:
    """
    Create an area chart (filled line chart).
    
    Args:
        labels: List of labels for the x-axis.
        datasets: List of datasets, each with 'label' and 'data'.
        title: Chart title.
        stacked: Whether to stack the areas.
    """
    # Apply fill to all datasets
    for dataset in datasets:
        if "fill" not in dataset:
            dataset["fill"] = True
        if "tension" not in dataset:
            dataset["tension"] = 0.4
    
    config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                },
                "filler": {
                    "propagate": False
                }
            },
            "scales": {
                "x": {"stacked": stacked},
                "y": {"stacked": stacked, "beginAtZero": True}
            },
            "interaction": {
                "intersect": False
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_time_series_chart(
    data_points: List[Dict[str, Any]],
    datasets: List[Dict[str, Any]],
    title: str = "Time Series Chart",
    time_unit: str = "day"
) -> str:
    """
    Create a time series chart with date/time on x-axis.
    
    Args:
        data_points: List of {x: timestamp, y: value} objects for each dataset.
        datasets: List of datasets with 'label' and 'data'.
        title: Chart title.
        time_unit: Time unit (millisecond, second, minute, hour, day, week, month, quarter, year).
    """
    config = {
        "type": "line",
        "data": {
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "x": {
                    "type": "time",
                    "time": {
                        "unit": time_unit
                    },
                    "title": {
                        "display": True,
                        "text": "Date"
                    }
                },
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "Value"
                    }
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_funnel_chart(
    labels: List[str],
    data: List[Union[int, float]],
    title: str = "Funnel Chart",
    color_palette: str = "professional"
) -> str:
    """
    Create a funnel chart using horizontal bar chart.
    
    Args:
        labels: List of stage labels.
        data: List of values for each stage (should be descending).
        title: Chart title.
        color_palette: Color palette to use.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["professional"])
    
    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)],
                "borderWidth": 2,
                "borderColor": "#fff"
            }]
        },
        "options": {
            "indexAxis": "y",
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": False
                }
            },
            "scales": {
                "x": {
                    "beginAtZero": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_gauge_chart(
    value: Union[int, float],
    max_value: Union[int, float],
    title: str = "Gauge Chart",
    thresholds: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Create a gauge chart using doughnut chart.
    
    Args:
        value: Current value.
        max_value: Maximum value.
        title: Chart title.
        thresholds: Optional list of threshold objects with 'value' and 'color'.
    """
    remaining = max_value - value
    
    # Default thresholds
    if not thresholds:
        if value / max_value < 0.5:
            color = "rgba(255, 99, 132, 0.8)"  # Red
        elif value / max_value < 0.8:
            color = "rgba(255, 206, 86, 0.8)"  # Yellow
        else:
            color = "rgba(75, 192, 192, 0.8)"  # Green
    else:
        color = "rgba(54, 162, 235, 0.8)"  # Default blue
    
    config = {
        "type": "doughnut",
        "data": {
            "labels": ["Value", "Remaining"],
            "datasets": [{
                "data": [value, remaining],
                "backgroundColor": [color, "rgba(200, 200, 200, 0.2)"],
                "borderWidth": 0,
                "circumference": 180,
                "rotation": 270
            }]
        },
        "options": {
            "responsive": True,
            "cutout": "75%",
            "plugins": {
                "title": {
                    "display": True,
                    "text": f"{title}: {value}/{max_value}",
                    "font": {"size": 18}
                },
                "legend": {
                    "display": False
                },
                "tooltip": {
                    "enabled": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def analyze_data_for_chart(
    data: List[Union[int, float]],
    labels: Optional[List[str]] = None
) -> str:
    """
    Analyze data and suggest the best chart type with statistics.
    
    Args:
        data: List of numerical values.
        labels: Optional labels for the data.
    """
    if not data:
        return json.dumps({"error": "No data provided"})
    
    # Calculate statistics
    total = sum(data)
    count = len(data)
    mean = total / count
    sorted_data = sorted(data)
    median = sorted_data[count // 2] if count % 2 else (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val
    
    # Variance and standard deviation
    variance = sum((x - mean) ** 2 for x in data) / count
    std_dev = variance ** 0.5
    
    # Suggest chart type
    suggestions = []
    
    if count <= 10:
        suggestions.append({
            "type": "pie",
            "reason": "Small dataset works well with pie chart for proportions"
        })
        suggestions.append({
            "type": "bar",
            "reason": "Bar chart for easy comparison of values"
        })
    
    if count > 10:
        suggestions.append({
            "type": "line",
            "reason": "Line chart for trends over time or sequence"
        })
        suggestions.append({
            "type": "area",
            "reason": "Area chart to show cumulative trends"
        })
    
    if std_dev / mean > 0.5:  # High variability
        suggestions.append({
            "type": "scatter",
            "reason": "High variability suggests scatter plot for distribution"
        })
    
    analysis = {
        "statistics": {
            "count": count,
            "sum": total,
            "mean": round(mean, 2),
            "median": median,
            "min": min_val,
            "max": max_val,
            "range": range_val,
            "std_dev": round(std_dev, 2),
            "variance": round(variance, 2)
        },
        "suggested_charts": suggestions,
        "data_summary": {
            "has_labels": labels is not None,
            "label_count": len(labels) if labels else 0
        }
    }
    
    return json.dumps(analysis, indent=2)

@mcp.tool()
def add_chart_animations(
    chart_config: str,
    animation_duration: int = 1000,
    animation_easing: str = "easeInOutQuart"
) -> str:
    """
    Add animation configuration to an existing chart config.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        animation_duration: Animation duration in milliseconds.
        animation_easing: Easing function (linear, easeInQuad, easeOutQuart, easeInOutQuart, etc).
    """
    config = json.loads(chart_config)
    
    if "options" not in config:
        config["options"] = {}
    
    config["options"]["animation"] = {
        "duration": animation_duration,
        "easing": animation_easing,
        "onComplete": None,
        "delay": 0
    }
    
    # Add dataset-specific animations
    config["options"]["animations"] = {
        "tension": {
            "duration": animation_duration,
            "easing": animation_easing,
            "from": 1,
            "to": 0,
            "loop": False
        }
    }
    
    return json.dumps(config, indent=2)

@mcp.tool()
def create_comparison_chart(
    labels: List[str],
    dataset1: Dict[str, Any],
    dataset2: Dict[str, Any],
    title: str = "Comparison Chart",
    chart_type: str = "bar"
) -> str:
    """
    Create a chart comparing two datasets side by side.
    
    Args:
        labels: List of labels for comparison points.
        dataset1: First dataset with 'label' and 'data'.
        dataset2: Second dataset with 'label' and 'data'.
        title: Chart title.
        chart_type: Type of chart (bar, line, radar).
    """
    # Ensure datasets have colors
    if "backgroundColor" not in dataset1:
        dataset1["backgroundColor"] = COLOR_PALETTES["professional"][0]
    if "backgroundColor" not in dataset2:
        dataset2["backgroundColor"] = COLOR_PALETTES["professional"][1]
    
    if chart_type == "line":
        if "borderColor" not in dataset1:
            dataset1["borderColor"] = COLOR_PALETTES["professional"][0]
        if "borderColor" not in dataset2:
            dataset2["borderColor"] = COLOR_PALETTES["professional"][1]
        dataset1["tension"] = 0.4
        dataset2["tension"] = 0.4
    
    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": [dataset1, dataset2]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "y": {"beginAtZero": True}
            } if chart_type != "radar" else {
                "r": {"beginAtZero": True}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_multi_axis_chart(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    title: str = "Multi-Axis Chart"
) -> str:
    """
    Create a chart with multiple y-axes for different scales.
    
    Args:
        labels: List of labels for x-axis.
        datasets: List of datasets, each should have 'yAxisID' specified.
        title: Chart title.
    """
    config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True,
                    "position": "top"
                }
            },
            "scales": {
                "y": {
                    "type": "linear",
                    "display": True,
                    "position": "left",
                    "beginAtZero": True
                },
                "y1": {
                    "type": "linear",
                    "display": True,
                    "position": "right",
                    "beginAtZero": True,
                    "grid": {
                        "drawOnChartArea": False
                    }
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_chart_with_annotations(
    chart_config: str,
    annotations: List[Dict[str, Any]]
) -> str:
    """
    Add annotations (lines, boxes, labels) to an existing chart.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        annotations: List of annotation objects with type, value, label, etc.
    """
    config = json.loads(chart_config)
    
    if "options" not in config:
        config["options"] = {}
    
    if "plugins" not in config["options"]:
        config["options"]["plugins"] = {}
    
    config["options"]["plugins"]["annotation"] = {
        "annotations": {}
    }
    
    for i, ann in enumerate(annotations):
        ann_id = f"annotation{i}"
        config["options"]["plugins"]["annotation"]["annotations"][ann_id] = ann
    
    return json.dumps(config, indent=2)

@mcp.tool()
def export_chart_data_csv(
    labels: List[str],
    datasets: List[Dict[str, Any]]
) -> str:
    """
    Export chart data as CSV format string.
    
    Args:
        labels: List of labels.
        datasets: List of datasets with 'label' and 'data'.
    """
    # Create CSV header
    csv_lines = []
    header = ["Label"] + [ds.get("label", f"Dataset {i+1}") for i, ds in enumerate(datasets)]
    csv_lines.append(",".join(header))
    
    # Create data rows
    for i, label in enumerate(labels):
        row = [label]
        for dataset in datasets:
            data = dataset.get("data", [])
            value = data[i] if i < len(data) else ""
            row.append(str(value))
        csv_lines.append(",".join(row))
    
    return "\n".join(csv_lines)

@mcp.tool()
def create_gradient_dataset(
    data: List[Union[int, float]],
    label: str,
    start_color: str = "rgba(255, 99, 132, 0.8)",
    end_color: str = "rgba(54, 162, 235, 0.8)"
) -> str:
    """
    Create a dataset configuration with gradient colors.
    
    Args:
        data: List of data values.
        label: Dataset label.
        start_color: Starting gradient color.
        end_color: Ending gradient color.
    """
    dataset = {
        "label": label,
        "data": data,
        "backgroundColor": {
            "type": "gradient",
            "colors": [start_color, end_color]
        },
        "borderColor": start_color,
        "borderWidth": 2
    }
    
    return json.dumps(dataset, indent=2)

@mcp.tool()
def create_waterfall_chart(
    labels: List[str],
    data: List[Union[int, float]],
    title: str = "Waterfall Chart",
    color_palette: str = "professional"
) -> str:
    """
    Create a waterfall chart showing cumulative effect of sequential values.
    
    Args:
        labels: List of labels for each step.
        data: List of values (positive or negative changes).
        title: Chart title.
        color_palette: Color palette to use.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["professional"])
    
    # Calculate cumulative values
    cumulative = []
    running_total = 0
    background_colors = []
    
    for i, value in enumerate(data):
        cumulative.append(running_total)
        running_total += value
        # Green for positive, red for negative
        if value >= 0:
            background_colors.append("rgba(75, 192, 192, 0.8)")
        else:
            background_colors.append("rgba(255, 99, 132, 0.8)")
    
    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Base",
                    "data": cumulative,
                    "backgroundColor": "rgba(0, 0, 0, 0)"
                },
                {
                    "label": "Change",
                    "data": data,
                    "backgroundColor": background_colors
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True
                }
            },
            "scales": {
                "x": {"stacked": True},
                "y": {"stacked": True, "beginAtZero": True}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_heatmap_chart(
    x_labels: List[str],
    y_labels: List[str],
    data_matrix: List[List[Union[int, float]]],
    title: str = "Heatmap"
) -> str:
    """
    Create a heatmap chart using matrix data.
    
    Args:
        x_labels: Labels for x-axis.
        y_labels: Labels for y-axis.
        data_matrix: 2D array of values.
        title: Chart title.
    """
    # Flatten data for bubble chart representation
    bubble_data = []
    max_val = max(max(row) for row in data_matrix)
    
    for y_idx, row in enumerate(data_matrix):
        for x_idx, value in enumerate(row):
            bubble_data.append({
                "x": x_idx,
                "y": y_idx,
                "r": (value / max_val) * 20 + 5  # Scale radius
            })
    
    config = {
        "type": "bubble",
        "data": {
            "datasets": [{
                "label": "Heatmap",
                "data": bubble_data,
                "backgroundColor": "rgba(255, 99, 132, 0.6)"
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "tooltip": {
                    "callbacks": {
                        "label": "function(context) { return 'Value: ' + context.raw.r; }"
                    }
                }
            },
            "scales": {
                "x": {
                    "type": "category",
                    "labels": x_labels,
                    "offset": True
                },
                "y": {
                    "type": "category",
                    "labels": y_labels,
                    "offset": True
                }
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_candlestick_chart(
    labels: List[str],
    data: List[Dict[str, float]],
    title: str = "Candlestick Chart"
) -> str:
    """
    Create a candlestick/OHLC chart for financial data.
    
    Args:
        labels: List of time labels.
        data: List of dicts with 'open', 'high', 'low', 'close' values.
        title: Chart title.
    """
    # Use bar chart to simulate candlestick
    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Low-High",
                    "data": [d["high"] - d["low"] for d in data],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.6)" if d["close"] >= d["open"] 
                        else "rgba(255, 99, 132, 0.6)" for d in data
                    ]
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "tooltip": {
                    "enabled": True
                }
            },
            "scales": {
                "y": {"beginAtZero": False}
            }
        }
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def create_realtime_chart_config(
    initial_labels: List[str],
    initial_data: List[Union[int, float]],
    title: str = "Real-time Chart",
    max_data_points: int = 20
) -> str:
    """
    Create a chart configuration optimized for real-time data streaming.
    
    Args:
        initial_labels: Initial labels.
        initial_data: Initial data points.
        title: Chart title.
        max_data_points: Maximum number of points to display.
    """
    config = {
        "type": "line",
        "data": {
            "labels": initial_labels,
            "datasets": [{
                "label": "Real-time Data",
                "data": initial_data,
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "tension": 0.4,
                "fill": True
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": title,
                    "font": {"size": 18}
                },
                "legend": {
                    "display": True
                }
            },
            "scales": {
                "x": {
                    "display": True,
                    "title": {
                        "display": True,
                        "text": "Time"
                    }
                },
                "y": {
                    "display": True,
                    "title": {
                        "display": True,
                        "text": "Value"
                    }
                }
            },
            "animation": {
                "duration": 300
            }
        },
        "maxDataPoints": max_data_points
    }
    return json.dumps(config, indent=2)

@mcp.tool()
def add_responsive_breakpoints(
    chart_config: str,
    breakpoints: Optional[Dict[str, Dict[str, Any]]] = None
) -> str:
    """
    Add responsive breakpoints to a chart configuration.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        breakpoints: Dict of breakpoint configs (mobile, tablet, desktop).
    """
    config = json.loads(chart_config)
    
    default_breakpoints = {
        "mobile": {
            "maxWidth": 480,
            "options": {
                "plugins": {
                    "legend": {"position": "bottom"},
                    "title": {"font": {"size": 14}}
                }
            }
        },
        "tablet": {
            "maxWidth": 768,
            "options": {
                "plugins": {
                    "legend": {"position": "top"},
                    "title": {"font": {"size": 16}}
                }
            }
        },
        "desktop": {
            "minWidth": 769,
            "options": {
                "plugins": {
                    "legend": {"position": "right"},
                    "title": {"font": {"size": 18}}
                }
            }
        }
    }
    
    config["responsive_breakpoints"] = breakpoints or default_breakpoints
    return json.dumps(config, indent=2)

@mcp.tool()
def add_accessibility_features(
    chart_config: str,
    enable_keyboard_nav: bool = True,
    enable_screen_reader: bool = True
) -> str:
    """
    Add accessibility features to a chart configuration.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        enable_keyboard_nav: Enable keyboard navigation.
        enable_screen_reader: Enable screen reader support.
    """
    config = json.loads(chart_config)
    
    if "options" not in config:
        config["options"] = {}
    
    if "plugins" not in config["options"]:
        config["options"]["plugins"] = {}
    
    config["options"]["plugins"]["a11y"] = {
        "enabled": True,
        "keyboardNavigation": enable_keyboard_nav,
        "screenReaderAnnouncements": enable_screen_reader
    }
    
    # Add ARIA labels
    config["aria"] = {
        "label": config.get("options", {}).get("plugins", {}).get("title", {}).get("text", "Chart"),
        "describedBy": "chart-description"
    }
    
    return json.dumps(config, indent=2)

@mcp.tool()
def transform_data_cumulative(
    data: List[Union[int, float]]
) -> str:
    """
    Transform data into cumulative sum.
    
    Args:
        data: List of values.
    """
    cumulative = []
    running_sum = 0
    for value in data:
        running_sum += value
        cumulative.append(running_sum)
    
    return json.dumps({
        "original": data,
        "cumulative": cumulative
    }, indent=2)

@mcp.tool()
def transform_data_moving_average(
    data: List[Union[int, float]],
    window_size: int = 3
) -> str:
    """
    Calculate moving average of data.
    
    Args:
        data: List of values.
        window_size: Size of the moving window.
    """
    moving_avg = []
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        window = data[start:i + 1]
        moving_avg.append(sum(window) / len(window))
    
    return json.dumps({
        "original": data,
        "moving_average": [round(v, 2) for v in moving_avg],
        "window_size": window_size
    }, indent=2)

@mcp.tool()
def transform_data_percentage_change(
    data: List[Union[int, float]]
) -> str:
    """
    Calculate percentage change between consecutive values.
    
    Args:
        data: List of values.
    """
    pct_change = [0]  # First value has no change
    for i in range(1, len(data)):
        if data[i - 1] != 0:
            change = ((data[i] - data[i - 1]) / data[i - 1]) * 100
            pct_change.append(round(change, 2))
        else:
            pct_change.append(0)
    
    return json.dumps({
        "original": data,
        "percentage_change": pct_change
    }, indent=2)

@mcp.tool()
def merge_chart_datasets(
    chart_config1: str,
    chart_config2: str,
    title: str = "Merged Chart"
) -> str:
    """
    Merge datasets from two chart configurations.
    
    Args:
        chart_config1: First chart configuration JSON string.
        chart_config2: Second chart configuration JSON string.
        title: Title for the merged chart.
    """
    config1 = json.loads(chart_config1)
    config2 = json.loads(chart_config2)
    
    merged_config = {
        "type": config1.get("type", "bar"),
        "data": {
            "labels": config1.get("data", {}).get("labels", []),
            "datasets": (
                config1.get("data", {}).get("datasets", []) +
                config2.get("data", {}).get("datasets", [])
            )
        },
        "options": config1.get("options", {})
    }
    
    if "plugins" not in merged_config["options"]:
        merged_config["options"]["plugins"] = {}
    
    merged_config["options"]["plugins"]["title"] = {
        "display": True,
        "text": title,
        "font": {"size": 18}
    }
    
    return json.dumps(merged_config, indent=2)

@mcp.tool()
def create_theme_preset(
    theme_name: str = "dark"
) -> str:
    """
    Get a complete theme preset for charts.
    
    Args:
        theme_name: Theme name (dark, light, ocean, sunset, forest, neon).
    """
    themes = {
        "dark": {
            "backgroundColor": "#1a1a1a",
            "textColor": "#e0e0e0",
            "gridColor": "rgba(255, 255, 255, 0.1)",
            "palette": COLOR_PALETTES["vibrant"]
        },
        "light": {
            "backgroundColor": "#ffffff",
            "textColor": "#333333",
            "gridColor": "rgba(0, 0, 0, 0.1)",
            "palette": COLOR_PALETTES["professional"]
        },
        "ocean": {
            "backgroundColor": "#0a1929",
            "textColor": "#b2d8ff",
            "gridColor": "rgba(178, 216, 255, 0.1)",
            "palette": [
                "rgba(54, 162, 235, 0.8)",
                "rgba(26, 188, 156, 0.8)",
                "rgba(52, 152, 219, 0.8)",
                "rgba(22, 160, 133, 0.8)"
            ]
        },
        "sunset": {
            "backgroundColor": "#2d1b2e",
            "textColor": "#ffcccb",
            "gridColor": "rgba(255, 204, 203, 0.1)",
            "palette": [
                "rgba(255, 99, 132, 0.8)",
                "rgba(255, 159, 64, 0.8)",
                "rgba(255, 206, 86, 0.8)",
                "rgba(255, 179, 186, 0.8)"
            ]
        },
        "forest": {
            "backgroundColor": "#1a2f1a",
            "textColor": "#c8e6c9",
            "gridColor": "rgba(200, 230, 201, 0.1)",
            "palette": [
                "rgba(75, 192, 192, 0.8)",
                "rgba(22, 160, 133, 0.8)",
                "rgba(46, 125, 50, 0.8)",
                "rgba(76, 175, 80, 0.8)"
            ]
        },
        "neon": {
            "backgroundColor": "#000000",
            "textColor": "#00ff00",
            "gridColor": "rgba(0, 255, 0, 0.2)",
            "palette": [
                "rgba(0, 255, 0, 0.8)",
                "rgba(255, 0, 255, 0.8)",
                "rgba(0, 255, 255, 0.8)",
                "rgba(255, 255, 0, 0.8)"
            ]
        }
    }
    
    return json.dumps(themes.get(theme_name, themes["light"]), indent=2)

@mcp.tool()
def add_interactive_tooltips(
    chart_config: str,
    tooltip_mode: str = "index",
    show_percentages: bool = False
) -> str:
    """
    Add advanced interactive tooltips to a chart.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        tooltip_mode: Tooltip mode (index, dataset, point, nearest, x, y).
        show_percentages: Show percentages in tooltips.
    """
    config = json.loads(chart_config)
    
    if "options" not in config:
        config["options"] = {}
    
    if "plugins" not in config["options"]:
        config["options"]["plugins"] = {}
    
    config["options"]["plugins"]["tooltip"] = {
        "enabled": True,
        "mode": tooltip_mode,
        "intersect": False,
        "backgroundColor": "rgba(0, 0, 0, 0.8)",
        "titleColor": "#fff",
        "bodyColor": "#fff",
        "borderColor": "rgba(255, 255, 255, 0.3)",
        "borderWidth": 1,
        "padding": 12,
        "displayColors": True,
        "callbacks": {
            "label": "function(context) { return context.dataset.label + ': ' + context.parsed.y; }"
        }
    }
    
    if show_percentages:
        config["options"]["plugins"]["tooltip"]["callbacks"]["afterLabel"] = \
            "function(context) { return '(' + Math.round(context.parsed.y / total * 100) + '%)'; }"
    
    return json.dumps(config, indent=2)

@mcp.tool()
def add_zoom_pan_controls(
    chart_config: str,
    enable_zoom: bool = True,
    enable_pan: bool = True,
    zoom_mode: str = "xy"
) -> str:
    """
    Add zoom and pan controls to a chart.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        enable_zoom: Enable zoom functionality.
        enable_pan: Enable pan functionality.
        zoom_mode: Zoom mode (x, y, xy).
    """
    config = json.loads(chart_config)
    
    if "options" not in config:
        config["options"] = {}
    
    if "plugins" not in config["options"]:
        config["options"]["plugins"] = {}
    
    config["options"]["plugins"]["zoom"] = {
        "zoom": {
            "enabled": enable_zoom,
            "mode": zoom_mode,
            "speed": 0.1
        },
        "pan": {
            "enabled": enable_pan,
            "mode": zoom_mode
        },
        "limits": {
            "x": {"min": "original", "max": "original"},
            "y": {"min": "original", "max": "original"}
        }
    }
    
    return json.dumps(config, indent=2)

@mcp.tool()
def filter_chart_data(
    labels: List[str],
    datasets: List[Dict[str, Any]],
    filter_condition: str,
    threshold: Union[int, float]
) -> str:
    """
    Filter chart data based on a condition.
    
    Args:
        labels: List of labels.
        datasets: List of datasets.
        filter_condition: Condition (greater_than, less_than, equals, not_equals).
        threshold: Threshold value for filtering.
    """
    filtered_labels = []
    filtered_datasets = []
    
    # Get indices that match the condition
    if datasets:
        first_dataset_data = datasets[0].get("data", [])
        matching_indices = []
        
        for i, value in enumerate(first_dataset_data):
            match = False
            if filter_condition == "greater_than" and value > threshold:
                match = True
            elif filter_condition == "less_than" and value < threshold:
                match = True
            elif filter_condition == "equals" and value == threshold:
                match = True
            elif filter_condition == "not_equals" and value != threshold:
                match = True
            
            if match:
                matching_indices.append(i)
                if i < len(labels):
                    filtered_labels.append(labels[i])
        
        # Filter all datasets
        for dataset in datasets:
            filtered_dataset = dataset.copy()
            original_data = dataset.get("data", [])
            filtered_dataset["data"] = [original_data[i] for i in matching_indices if i < len(original_data)]
            filtered_datasets.append(filtered_dataset)
    
    return json.dumps({
        "labels": filtered_labels,
        "datasets": filtered_datasets,
        "filter_applied": {
            "condition": filter_condition,
            "threshold": threshold,
            "original_count": len(labels),
            "filtered_count": len(filtered_labels)
        }
    }, indent=2)

@mcp.tool()
def add_statistical_overlay(
    chart_config: str,
    show_mean: bool = True,
    show_median: bool = True,
    show_std_dev: bool = False
) -> str:
    """
    Add statistical overlay lines to a chart.
    
    Args:
        chart_config: Existing chart configuration JSON string.
        show_mean: Show mean line.
        show_median: Show median line.
        show_std_dev: Show standard deviation bands.
    """
    config = json.loads(chart_config)
    
    # Calculate statistics from first dataset
    if "data" in config and "datasets" in config["data"] and config["data"]["datasets"]:
        first_dataset = config["data"]["datasets"][0]
        data = first_dataset.get("data", [])
        
        if data:
            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            median = sorted_data[len(data) // 2] if len(data) % 2 else \
                     (sorted_data[len(data) // 2 - 1] + sorted_data[len(data) // 2]) / 2
            
            labels = config["data"].get("labels", [])
            
            if show_mean:
                config["data"]["datasets"].append({
                    "label": "Mean",
                    "data": [mean] * len(labels),
                    "type": "line",
                    "borderColor": "rgba(255, 206, 86, 1)",
                    "borderWidth": 2,
                    "borderDash": [5, 5],
                    "fill": False,
                    "pointRadius": 0
                })
            
            if show_median:
                config["data"]["datasets"].append({
                    "label": "Median",
                    "data": [median] * len(labels),
                    "type": "line",
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "borderWidth": 2,
                    "borderDash": [10, 5],
                    "fill": False,
                    "pointRadius": 0
                })
    
    return json.dumps(config, indent=2)

@mcp.tool()
def export_chart_as_image_html(
    chart_config: str,
    filename: str = "chart.png",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Generate HTML with JavaScript to export chart as image.
    
    Args:
        chart_config: Chart configuration JSON string.
        filename: Filename for the exported image.
        width: Image width.
        height: Image height.
    """
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart Export</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <canvas id="myChart" width="{width}" height="{height}"></canvas>
    <button onclick="downloadChart()">Download Chart</button>
    
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const config = {chart_config};
        const myChart = new Chart(ctx, config);
        
        function downloadChart() {{
            const url = myChart.toBase64Image();
            const link = document.createElement('a');
            link.download = '{filename}';
            link.href = url;
            link.click();
        }}
    </script>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    mcp.run()

