from mcp.server.fastmcp import FastMCP  # Import the modern FastMCP framework for building the server
import json  # Standard library for processing JSON data structures
from typing import List, Optional, Union, Dict, Any  # Import typing for clear API documentation and IDE support

mcp = FastMCP("ChartJS")  # Initialize the FastMCP instance with a descriptive name

# Define comprehensive color palettes for consistent and professional chart styling
COLOR_PALETTES = {
    "vibrant": [  # A bold palette for charts that need to pop
        "rgba(255, 99, 132, 0.8)", "rgba(54, 162, 235, 0.8)", "rgba(255, 206, 86, 0.8)",
        "rgba(75, 192, 192, 0.8)", "rgba(153, 102, 255, 0.8)", "rgba(255, 159, 64, 0.8)",
        "rgba(199, 199, 199, 0.8)", "rgba(83, 102, 255, 0.8)", "rgba(255, 99, 255, 0.8)"
    ],
    "pastel": [  # Soft, gentle colors for light-themed or subtle visualizations
        "rgba(255, 179, 186, 0.8)", "rgba(186, 225, 255, 0.8)", "rgba(255, 223, 186, 0.8)",
        "rgba(186, 255, 201, 0.8)", "rgba(220, 186, 255, 0.8)", "rgba(255, 218, 193, 0.8)"
    ],
    "professional": [  # Corporate-style colors for business and academic reports
        "rgba(41, 128, 185, 0.8)", "rgba(52, 152, 219, 0.8)", "rgba(155, 89, 182, 0.8)",
        "rgba(142, 68, 173, 0.8)", "rgba(22, 160, 133, 0.8)", "rgba(26, 188, 156, 0.8)"
    ],
    "earth": [  # Natural, grounded tones for organic data representation
        "rgba(139, 69, 19, 0.8)", "rgba(160, 82, 45, 0.8)", "rgba(205, 133, 63, 0.8)",
        "rgba(210, 180, 140, 0.8)", "rgba(188, 143, 143, 0.8)", "rgba(165, 42, 42, 0.8)"
    ]
}

@mcp.tool()  # Decorator to register this function as an MCP tool for client use
def create_chart_config(  # Generic tool for granular Chart.js configuration control
    chart_type: str,  # The type of chart structure to be initialized
    labels: List[str],  # The data labels corresponding to each data point
    datasets: List[Dict[str, Any]],  # A nested list of dataset objects with values and styling
    options: Optional[Dict[str, Any]] = None  # Advanced override options for the Chart.js api
) -> str:  # Returns a JSON string containing the final configuration
    """
    Generate a Chart.js configuration object as a JSON string.
    """
    config = {  # Construct the primary configuration tree
        "type": chart_type,  # Inject the specified chart type
        "data": {  # Nested data map containing labels and actual data items
            "labels": labels,  # Map the provided labels to the axis
            "datasets": datasets  # Assign the provided datasets list
        },
        "options": options or {}  # Use provided options or default to an empty dictionary
    }
    return json.dumps(config, indent=2)  # Return formatted JSON with 2-space indentation

@mcp.tool()  # Register pie chart creation tool
def create_pie_chart(  # Function dedicated to proportional pie visualizations
    labels: List[str],  # Labels for each slice of the pie
    data: List[Union[int, float]],  # Numerical values representing slice proportions
    title: str = "Pie Chart",  # The descriptive title displayed above the chart
    color_palette: str = "vibrant"  # Selected color scheme from COLOR_PALETTES
) -> str:  # Returns the JSON configuration for the pie chart
    """
    Create a pie chart configuration.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])  # Select palette or fallback to vibrant
    
    config = {  # Structure the pie chart configuration
        "type": "pie",  # Specifically set chart type to 'pie'
        "data": {  # Container for labels and data values
            "labels": labels,  # Map labels to their respective slices
            "datasets": [{  # Pie charts usually have a single primary dataset
                "data": data,  # Pass the raw numerical data
                "backgroundColor": colors[:len(data)],  # Slice the palette to match data length
                "borderWidth": 2,  # Set white stroke width for slice separation
                "borderColor": "#fff"  # Set white border color for clear contrast
            }]
        },
        "options": {  # Layout and plugin configurations
            "responsive": True,  # Enable fluid resizing based on container width
            "plugins": {  # Plugin block for additional features
                "title": {  # Configuration for the chart title
                    "display": True,  # Ensure title is visible
                    "text": title,  # Use the provided title text
                    "font": {"size": 18}  # Style the title font size
                },
                "legend": {  # Configuration for the color key
                    "position": "bottom"  # Place legend at the bottom for better visibility
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # Output the serialized configuration

@mcp.tool()  # Register doughnut chart tool
def create_doughnut_chart(  # Function for creating doughnut-style visualizations
    labels: List[str],  # labels for each ring segment
    data: List[Union[int, float]],  # numerical values for each segment
    title: str = "Doughnut Chart",  # title of the doughnut chart
    color_palette: str = "vibrant",  # selected color palette
    cutout_percentage: int = 50  # central cutout size (0-100)
) -> str:  # returns doughnut chart configuration
    """
    Create a doughnut chart configuration.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])  # fetch colors
    
    config = {  # starting configuration object
        "type": "doughnut",  # set type to doughnut
        "data": {  # data property
            "labels": labels,  # apply labels
            "datasets": [{  # primary dataset
                "data": data,  # apply values
                "backgroundColor": colors[:len(data)],  # apply background colors
                "borderWidth": 2,  # segment border width
                "borderColor": "#fff"  # segment border color
            }]
        },
        "options": {  # charting options
            "responsive": True,  # make chart responsive
            "cutout": f"{cutout_percentage}%",  # set the cutout radius
            "plugins": {  # plugin settings
                "title": {  # title plugin
                    "display": True,  # show title
                    "text": title,  # specific title text
                    "font": {"size": 18}  # title font size
                },
                "legend": {  # legend plugin
                    "position": "bottom"  # place legend at bottom
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return pretty-printed JSON

@mcp.tool()  # register bar chart tool
def create_bar_chart(  # function for bar and column charts
    labels: List[str],  # labels for the categories
    datasets: List[Dict[str, Any]],  # list of labeled datasets
    title: str = "Bar Chart",  # main chart title
    stacked: bool = False,  # whether to stack bars
    horizontal: bool = False  # orientation of bars
) -> str:  # returns bar chart JSON
    """
    Create a bar chart configuration.
    """
    chart_type = "bar" if not horizontal else "horizontalBar"  # determine chart orientation
    
    config = {  # init config
        "type": chart_type,  # set the type
        "data": {  # set data
            "labels": labels,  # assign labels
            "datasets": datasets  # assign datasets
        },
        "options": {  # set options
            "responsive": True,  # maintain responsiveness
            "plugins": {  # configure plugins
                "title": {  # configure title
                    "display": True,  # show title header
                    "text": title,  # header text
                    "font": {"size": 18}  # header font size
                },
                "legend": {  # configure legend
                    "display": True,  # show legend
                    "position": "top"  # top alignment for bar legends
                }
            },
            "scales": {  # configure axes
                "x": {"stacked": stacked},  # x-axis stacking
                "y": {"stacked": stacked, "beginAtZero": True}  # y-axis stacking & zero start
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized config

@mcp.tool()  # Register line chart tool
def create_line_chart(  # Function for time-series or trend visualization
    labels: List[str],  # X-axis category labels
    datasets: List[Dict[str, Any]],  # Data series with labels and points
    title: str = "Line Chart",  # Chart header title
    smooth: bool = True,  # Use bezier curves for smoothing
    fill: bool = False  # Fill space below the line
) -> str:  # Returns line chart JSON
    """
    Create a line chart configuration.
    """
    # Iterate through datasets to apply unified styling
    for dataset in datasets:  # Process each series
        if "tension" not in dataset:  # Check if tension exists
            dataset["tension"] = 0.4 if smooth else 0  # Apply smoothing factor
        if "fill" not in dataset:  # Check if fill exists
            dataset["fill"] = fill  # Apply fill status
    
    config = {  # Initialize configuration
        "type": "line",  # Explicitly set line type
        "data": {  # Data mapping
            "labels": labels,  # Map axis labels
            "datasets": datasets  # Map data series
        },
        "options": {  # Chart behavior
            "responsive": True,  # Auto-adjust size
            "plugins": {  # Core plugins
                "title": {  # Header plugin
                    "display": True,  # Show header
                    "text": title,  # Header text
                    "font": {"size": 18}  # Font styling
                },
                "legend": {  # Legend settings
                    "display": True,  # Show legend
                    "position": "top"  # Top orientation
                }
            },
            "scales": {  # Axis scaling
                "y": {"beginAtZero": True}  # Start Y from zero
            }
        }
    }
    return json.dumps(config, indent=2)  # Return JSON string

@mcp.tool()  # Register radar chart tool
def create_radar_chart(  # Function for spider/radar visualizations
    labels: List[str],  # Multi-axis dimension labels
    datasets: List[Dict[str, Any]],  # Data values for dimensions
    title: str = "Radar Chart"  # Chart header
) -> str:  # Returns radar JSON config
    """
    Create a radar chart configuration.
    """
    config = {  # Configuration structure
        "type": "radar",  # Set type to radar
        "data": {  # Data mappings
            "labels": labels,  # Map axis dimensions
            "datasets": datasets  # Map series data
        },
        "options": {  # Layout settings
            "responsive": True,  # Resize dynamically
            "plugins": {  # Plugin block
                "title": {  # Title settings
                    "display": True,  # Visible title
                    "text": title,  # Use title argument
                    "font": {"size": 18}  # Style font
                },
                "legend": {  # Legend orientation
                    "display": True,  # Show labels
                    "position": "top"  # Top placement
                }
            },
            "scales": {  # Radial scales
                "r": {  # Scale for radar axis
                    "beginAtZero": True  # Zero-based origin
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # Output JSON string

@mcp.tool()  # register polar area tool
def create_polar_area_chart(  # function for cyclical area charts
    labels: List[str],  # dimension labels
    data: List[Union[int, float]],  # data values
    title: str = "Polar Area Chart",  # chart title
    color_palette: str = "vibrant"  # styling palette
) -> str:  # returns polar JSON
    """
    Create a polar area chart configuration.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["vibrant"])  # select palette
    
    config = {  # init config
        "type": "polarArea",  # set specific type
        "data": {  # setup data
            "labels": labels,  # map labels
            "datasets": [{  # setup dataset
                "data": data,  # map values
                "backgroundColor": colors[:len(data)]  # map colors
            }]
        },
        "options": {  # layout options
            "responsive": True,  # auto-resize
            "plugins": {  # plugins block
                "title": {  # title plugin
                    "display": True,  # set visible
                    "text": title,  # apply title text
                    "font": {"size": 18}  # apply font size
                },
                "legend": {  # legend plugin
                    "position": "bottom"  # bottom alignment
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON

@mcp.tool()  # register scatter plot tool
def create_scatter_chart(  # function for X/Y correlation plots
    datasets: List[Dict[str, Any]],  # data points list
    title: str = "Scatter Chart"  # chart title
) -> str:  # returns scatter JSON
    """
    Create a scatter chart configuration.
    """
    config = {  # main config tree
        "type": "scatter",  # set chart type
        "data": {  # map data
            "datasets": datasets  # assign datasets
        },
        "options": {  # layout config
            "responsive": True,  # enable responsive resizing
            "plugins": {  # plugin settings
                "title": {  # header settings
                    "display": True,  # enable display
                    "text": title,  # apply title text
                    "font": {"size": 18}  # font size style
                },
                "legend": {  # legend settings
                    "display": True,  # visible legend
                    "position": "top"  # top alignment
                }
            },
            "scales": {  # axis scaling settings
                "x": {  # x-axis settings
                    "type": "linear",  # continuous linear scale
                    "position": "bottom"  # place at bottom
                },
                "y": {  # y-axis settings
                    "beginAtZero": True  # force zero origin
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON

@mcp.tool()  # register bubble chart tool
def create_bubble_chart(  # function for 3D data point visualizations (x, y, r)
    datasets: List[Dict[str, Any]],  # datasets containing x, y, and radius (r)
    title: str = "Bubble Chart"  # title of the bubble plot
) -> str:  # returns bubble JSON config
    """
    Create a bubble chart configuration.
    """
    config = {  # init configuration object
        "type": "bubble",  # set specific chart type to bubble
        "data": {  # setup data property
            "datasets": datasets  # assign provided datasets
        },
        "options": {  # layout settings
            "responsive": True,  # enable responsive resizing behaviour
            "plugins": {  # configure plugins
                "title": {  # title plugin configuration
                    "display": True,  # show title header on chart
                    "text": title,  # apply title text from argument
                    "font": {"size": 18}  # apply font size for title
                },
                "legend": {  # legend plugin configuration
                    "display": True,  # show legend key
                    "position": "top"  # position legend at top
                }
            },
            "scales": {  # axis scaling configuration
                "x": {  # horizontal axis settings
                    "type": "linear",  # use linear scale for X
                    "position": "bottom"  # place x-axis at bottom
                },
                "y": {  # vertical axis settings
                    "beginAtZero": True  # align y-axis start to zero
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON string

@mcp.tool()  # register mixed chart tool
def create_mixed_chart(  # function for combining multiple chart types in one view
    labels: List[str],  # shared axis labels
    datasets: List[Dict[str, Any]],  # series with specific 'type' (e.g., 'line', 'bar')
    title: str = "Mixed Chart"  # main chart header
) -> str:  # returns mixed chart JSON
    """
    Create a mixed chart with multiple chart types.
    """
    config = {  # init config structure
        "type": "bar",  # base type (can be overridden by individual datasets)
        "data": {  # map shared labels and varied datasets
            "labels": labels,  # apply axis labels
            "datasets": datasets  # assign custom datasets list
        },
        "options": {  # layout settings
            "responsive": True,  # maintain responsive scaling
            "plugins": {  # core plugins configuration
                "title": {  # main title component
                    "display": True,  # ensure title is visible
                    "text": title,  # apply the provided title
                    "font": {"size": 18}  # styling for title text
                },
                "legend": {  # key/legend component
                    "display": True,  # show the legend key
                    "position": "top"  # position on top of the chart
                }
            },
            "scales": {  # coordinate system settings
                "y": {"beginAtZero": True}  # ensure y-axis starts at zero
            }
        }
    }
    return json.dumps(config, indent=2)  # return pretty JSON string

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

@mcp.tool()  # register templates fetcher
def get_chart_templates() -> str:  # function to share boilerplate configurations
    """
    Return common Chart.js templates and examples for inspiration.
    """
    templates = {  # map of common chart structures
        "bar": {  # setup bar template
            "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],  # mock labels
            "datasets": [{  # mock dataset
                "label": "# of Votes",  # series label
                "data": [12, 19, 3, 5, 2, 3],  # mock values
                "backgroundColor": COLOR_PALETTES["vibrant"]  # apply default vibrant palette
            }]
        },
        "line": {  # setup line template
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],  # time-based labels
            "datasets": [{  # line series
                "label": "Monthly Sales",  # sales label
                "data": [65, 59, 80, 81, 56, 55],  # trend data
                "borderColor": "rgb(75, 192, 192)",  # cyan line color
                "tension": 0.4  # apply smooth curve
            }]
        },
        "pie": {  # setup pie template
            "labels": ["Chrome", "Firefox", "Safari", "Edge", "Other"],  # browser labels
            "datasets": [{  # pie series
                "data": [60, 20, 10, 5, 5],  # share data
                "backgroundColor": COLOR_PALETTES["professional"]  # blue palette
            }]
        },
        "radar": {  # setup radar template
            "labels": ["Speed", "Reliability", "Comfort", "Safety", "Efficiency"],  # feature labels
            "datasets": [{  # radar dataset
                "label": "Product A",  # product label
                "data": [80, 90, 70, 85, 75],  # scores
                "backgroundColor": "rgba(54, 162, 235, 0.2)",  # fill color
                "borderColor": "rgb(54, 162, 235)"  # line color
            }]
        }
    }
    return json.dumps(templates, indent=2)  # return serialized templates

@mcp.tool()  # register palette fetcher
def get_color_palettes() -> str:  # function to expose predefined color themes
    """
    Return available color palettes for charts.
    """
    return json.dumps(COLOR_PALETTES, indent=2)  # serialize and return COLOR_PALETTES map

@mcp.tool()  # register area chart tool
def create_area_chart(  # function for building filled line charts
    labels: List[str],  # axis category labels
    datasets: List[Dict[str, Any]],  # series data for the area
    title: str = "Area Chart",  # main chart header
    stacked: bool = False  # specify if areas should stack
) -> str:  # returns area chart JSON
    """
    Create an area chart (filled line chart).
    """
    # Iterate through datasets to apply required area styling
    for dataset in datasets:  # process each series in the list
        if "fill" not in dataset:  # check if fill property is missing
            dataset["fill"] = True  # force enable fill for area charts
        if "tension" not in dataset:  # check if tension is already set
            dataset["tension"] = 0.4  # apply default smooth curve
    
    config = {  # initialize configuration tree
        "type": "line",  # set technical type to line (area uses line + fill)
        "data": {  # map labels and data
            "labels": labels,  # map provided labels to x-axis
            "datasets": datasets  # assign styled datasets list
        },
        "options": {  # charting behavior settings
            "responsive": True,  # maintain responsive layout
            "plugins": {  # configure core plugins
                "title": {  # component for chart title
                    "display": True,  # make title visible
                    "text": title,  # set the title text
                    "font": {"size": 18}  # styling for title font
                },
                "legend": {  # component for data key
                    "display": True,  # make legend visible
                    "position": "top"  # align legend to the top
                },
                "filler": {  # component for area fill behavior
                    "propagate": False  # disable fill propagation
                }
            },
            "scales": {  # coordinate system mapping
                "x": {"stacked": stacked},  # handle horizontal stacking
                "y": {"stacked": stacked, "beginAtZero": True}  # handle vertical stacking & zero origin
            },
            "interaction": {  # interactions mapping
                "intersect": False  # allow interaction without direct intersection
            }
        }
    }
    return json.dumps(config, indent=2)  # return pretty JSON string

@mcp.tool()  # register time series tool
def create_time_series_chart(  # function for chronological data visualization
    data_points: List[Dict[str, Any]],  # data points list
    datasets: List[Dict[str, Any]],  # list of labeled datasets with 'data'
    title: str = "Time Series Chart",  # chart title header
    time_unit: str = "day"  # frequency unit for x-axis
) -> str:  # returns time series JSON
    """
    Create a time series chart with date/time on x-axis.
    """
    config = {  # structure chronological configuration
        "type": "line",  # base chart type is line
        "data": {  # map datasets to config
            "datasets": datasets  # assign datasets with time-based x values
        },
        "options": {  # behavioral settings
            "responsive": True,  # maintain resize-ability
            "plugins": {  # configure logic plugins
                "title": {  # main title settings
                    "display": True,  # enable title visibility
                    "text": title,  # apply title text
                    "font": {"size": 18}  # apply font size style
                },
                "legend": {  # chart legend settings
                    "display": True,  # show legend labels
                    "position": "top"  # position on top
                }
            },
            "scales": {  # coordinate system mapping
                "x": {  # horizontal time axis
                    "type": "time",  # set specific time scale type
                    "time": {  # time scale configuration
                        "unit": time_unit  # apply resolution (day, week, etc.)
                    },
                    "title": {  # axis label component
                        "display": True,  # show axis label
                        "text": "Date"  # set literal axis text
                    }
                },
                "y": {  # vertical value axis
                    "beginAtZero": True,  # start scale from zero
                    "title": {  # axis label component
                        "display": True,  # show vertical label
                        "text": "Value"  # set literal value text
                    }
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized configuration

@mcp.tool()  # register funnel chart tool
def create_funnel_chart(  # function for building waterfall/conversion funnels
    labels: List[str],  # labels for each conversion stage
    data: List[Union[int, float]],  # data values for each stage
    title: str = "Funnel Chart",  # main chart header
    color_palette: str = "professional"  # styling color palette
) -> str:  # returns funnel chart JSON
    """
    Create a funnel chart using horizontal bar chart.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["professional"])  # fetch colors
    
    config = {  # initialize configuration map
        "type": "bar",  # technical type set to bar
        "data": {  # setup data property
            "labels": labels,  # map stage labels
            "datasets": [{  # create primary dataset
                "data": data,  # assign stage values
                "backgroundColor": colors[:len(data)],  # apply styling colors
                "borderWidth": 2,  # set width of stage borders
                "borderColor": "#fff"  # set border color to white
            }]
        },
        "options": {  # layout behavior settings
            "indexAxis": "y",  # rotate axis to make bars horizontal
            "responsive": True,  # maintain resize flexibility
            "plugins": {  # configure core plugins
                "title": {  # component for chart header
                    "display": True,  # make header visible
                    "text": title,  # apply provided title text
                    "font": {"size": 18}  # styling for header font
                },
                "legend": {  # legend component
                    "display": False  # hide legend for single-series funnel
                }
            },
            "scales": {  # coordinate mapping
                "x": {  # horizontal value axis
                    "beginAtZero": True  # align scale origin to zero
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON string

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

@mcp.tool()  # register analysis tool
def analyze_data_for_chart(  # function to perform statistical screening
    data: List[Union[int, float]],  # input numeric series
    labels: Optional[List[str]] = None  # optional category markers
) -> str:  # returns analysis report
    """
    Analyze data and suggest the best chart type with statistics.
    """
    if not data:  # check for empty input
        return json.dumps({"error": "No data provided"})  # return error state
    
    # Logic to calculate core descriptive statistics
    total = sum(data)  # compute aggregate sum
    count = len(data)  # get sample size
    mean = total / count  # compute arithmetic average
    sorted_data = sorted(data)  # sort for positional stats
    median = sorted_data[count // 2] if count % 2 else (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2  # midpoint logic
    min_val = min(data)  # find floor value
    max_val = max(data)  # find ceiling value
    range_val = max_val - min_val  # compute spread
    
    # Logic for dispersion metrics
    variance = sum((x - mean) ** 2 for x in data) / count  # compute squared deviation
    std_dev = variance ** 0.5  # compute standard deviation root
    
    # Logic to generate visualization recommendations
    suggestions = []  # container for AI suggestions
    
    if count <= 10:  # rule for small samples
        suggestions.append({  # add pie suggestion
            "type": "pie",  # recommended type
            "reason": "Small dataset works well with pie chart for proportions"  # justification
        })
        suggestions.append({  # add bar suggestion
            "type": "bar",  # recommended type
            "reason": "Bar chart for easy comparison of values"  # justification
        })
    
    if count > 10:  # rule for large samples
        suggestions.append({  # add line suggestion
            "type": "line",  # recommended type
            "reason": "Line chart for trends over time or sequence"  # justification
        })
        suggestions.append({  # add area suggestion
            "type": "area",  # recommended type
            "reason": "Area chart to show cumulative trends"  # justification
        })
    
    if std_dev / mean > 0.5:  # High variability rule
        suggestions.append({  # add scatter suggestion
            "type": "scatter",  # recommended type
            "reason": "High variability suggests scatter plot for distribution"  # justification
        })
    
    analysis = {  # structure complete response
        "statistics": {  # numeric breakdown
            "count": count,  # population size
            "sum": total,    # aggregate total
            "mean": round(mean, 2),  # rounded average
            "median": median, # midpoint value
            "min": min_val,   # floor value
            "max": max_val,   # ceiling value
            "range": range_val, # spread value
            "std_dev": round(std_dev, 2), # rounded dispersion
            "variance": round(variance, 2) # rounded variance
        },
        "suggested_charts": suggestions,  # logic-based recommendations
        "data_summary": {  # contextual metadata
            "has_labels": labels is not None,  # label presence flag
            "label_count": len(labels) if labels else 0  # label count
        }
    }
    
    return json.dumps(analysis, indent=2)  # return serialized JSON report

@mcp.tool()  # register animation enhancement tool
def add_chart_animations(  # function to inject animation logic into existing configs
    chart_config: str,  # serialized chart configuration JSON
    animation_duration: int = 1000,  # animation speed in milliseconds
    animation_easing: str = "easeInOutQuart"  # mathematical easing function
) -> str:  # returns updated configuration JSON
    """
    Add animation configuration to an existing chart config.
    """
    config = json.loads(chart_config)  # parse input JSON string into dictionary
    
    if "options" not in config:  # check for options root
        config["options"] = {}  # create options dictionary if missing
    
    config["options"]["animation"] = {  # configure primary animation object
        "duration": animation_duration,  # set the animation timeline length
        "easing": animation_easing,  # apply selected interpolation curve
        "onComplete": None,  # callback hook for animation end
        "delay": 0  # initial start delay
    }
    
    # Add detailed property-specific animations
    config["options"]["animations"] = {  # detailed animations map
        "tension": {  # animate curve tension property
            "duration": animation_duration,  # match main duration
            "easing": animation_easing,  # match main easing
            "from": 1,  # starting tension value
            "to": 0,  # ending tension target
            "loop": False  # disable repeat looping
        }
    }
    
    return json.dumps(config, indent=2)  # return updated configuration

@mcp.tool()  # register comparison tool
def create_comparison_chart(  # function for side-by-side data comparison
    labels: List[str],  # common x-axis labels
    dataset1: Dict[str, Any],  # first dataset configuration
    dataset2: Dict[str, Any],  # second dataset configuration
    title: str = "Comparison Chart",  # chart title header
    chart_type: str = "bar"  # preferred visualization type
) -> str:  # returns comparison chart JSON
    """
    Create a chart comparing two datasets side by side.
    """
    # Auto-assign colors if not provided for visual consistency
    if "backgroundColor" not in dataset1:  # check for missing color in ds1
        dataset1["backgroundColor"] = COLOR_PALETTES["professional"][0]  # use first palette color
    if "backgroundColor" not in dataset2:  # check for missing color in ds2
        dataset2["backgroundColor"] = COLOR_PALETTES["professional"][1]  # use second palette color
    
    if chart_type == "line":  # additional logic for line chart comparisons
        if "borderColor" not in dataset1:  # check for line border color 1
            dataset1["borderColor"] = COLOR_PALETTES["professional"][0]  # map palette color
        if "borderColor" not in dataset2:  # check for line border color 2
            dataset2["borderColor"] = COLOR_PALETTES["professional"][1]  # map palette color
        dataset1["tension"] = 0.4  # apply smooth curve to ds1
        dataset2["tension"] = 0.4  # apply smooth curve to ds2
    
    config = {  # initialize configuration object
        "type": chart_type,  # set the specified chart type
        "data": {  # map labels and paired datasets
            "labels": labels,  # map provided labels
            "datasets": [dataset1, dataset2]  # group both datasets
        },
        "options": {  # layout behavior settings
            "responsive": True,  # maintain resize-ability
            "plugins": {  # configure logic plugins
                "title": {  # title component settings
                    "display": True,  # make header visible
                    "text": title,  # apply title text
                    "font": {"size": 18}  # styling for title text
                },
                "legend": {  # legend key settings
                    "display": True,  # show legend labels
                    "position": "top"  # position at top
                }
            },
            "scales": {  # coordinate system mapping
                "y": {"beginAtZero": True}  # linear scale for standard charts
            } if chart_type != "radar" else {  # specialized scale for radar
                "r": {"beginAtZero": True}  # radial scale for radar
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON string

@mcp.tool()  # register multi-axis tool
def create_multi_axis_chart(  # function for charts with dual y-scales
    labels: List[str],  # shared x-axis labels
    datasets: List[Dict[str, Any]],  # data series specifying yAxisID ('y' or 'y1')
    title: str = "Multi-Axis Chart"  # main chart header
) -> str:  # returns multi-axis JSON
    """
    Create a chart with multiple y-axes for different scales.
    """
    config = {  # structure base config
        "type": "line",  # default to line chart
        "data": {  # map data components
            "labels": labels,  # map provided labels
            "datasets": datasets  # assign datasets with separate yAxisIDs
        },
        "options": {  # behavioral settings
            "responsive": True,  # maintain resize flexibility
            "plugins": {  # configure core plugins
                "title": {  # title plugin settings
                    "display": True,  # make header visible
                    "text": title,  # set the title text
                    "font": {"size": 18}  # apply font size style
                },
                "legend": {  # legend key component
                    "display": True,  # show legend labels
                    "position": "top"  # align to top
                }
            },
            "scales": {  # coordinate mapping for multiple axes
                "y": {  # left-side y-axis
                    "type": "linear",  # continuous linear scale
                    "display": True,  # make visible
                    "position": "left",  # align to left
                    "beginAtZero": True  # start scale from zero
                },
                "y1": {  # right-side y-axis
                    "type": "linear",  # continuous linear scale
                    "display": True,  # make visible
                    "position": "right",  # align to right
                    "beginAtZero": True,  # start scale from zero
                    "grid": {  # gridline settings
                        "drawOnChartArea": False  # hide horizontal lines for clean look
                    }
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized configuration

@mcp.tool()  # register annotation tool
def create_chart_with_annotations(  # function to overlay static elements onto charts
    chart_config: str,  # input chart configuration JSON
    annotations: List[Dict[str, Any]]  # list of annotation objects (lines, boxes)
) -> str:  # returns configuration with annotations
    """
    Add annotations (lines, boxes, labels) to an existing chart.
    """
    config = json.loads(chart_config)  # parse the input JSON string
    
    if "options" not in config:  # check if options exist
        config["options"] = {}  # initialize if missing
    
    if "plugins" not in config["options"]:  # check for plugins block
        config["options"]["plugins"] = {}  # initialize if missing
    
    config["options"]["plugins"]["annotation"] = {  # setup chartjs-plugin-annotation block
        "annotations": {}  # dictionary to hold named annotation items
    }
    
    for i, ann in enumerate(annotations):  # loop through provided annotation specs
        ann_id = f"annotation{i}"  # generate a unique key
        config["options"]["plugins"]["annotation"]["annotations"][ann_id] = ann  # map object to key
    
    return json.dumps(config, indent=2)  # return updated configuration

@mcp.tool()  # register CSV export tool
def export_chart_data_csv(  # function to convert chart datasets to CSV string
    labels: List[str],  # list of labels for each data row
    datasets: List[Dict[str, Any]]  # list of datasets with 'label' and 'data'
) -> str:  # returns formatted CSV string
    """
    Export chart data as CSV format string.
    """
    # Create CSV structure by initializing line list
    csv_lines = []  # holding list for CSV rows
    header = ["Label"] + [ds.get("label", f"Dataset {i+1}") for i, ds in enumerate(datasets)]  # construct header row
    csv_lines.append(",".join(header))  # join and append header row
    
    # Process each label and corresponding data points across datasets
    for i, label in enumerate(labels):  # loop through each x-axis label
        row = [label]  # start row with the label
        for dataset in datasets:  # loop through each dataset to fetch value at current index
            data = dataset.get("data", [])  # fetch data list safely
            value = data[i] if i < len(data) else ""  # fetch specific value or empty string
            row.append(str(value))  # append string representation of value
        csv_lines.append(",".join(row))  # join and append data row
    
    return "\n".join(csv_lines)  # return full CSV as single string

@mcp.tool()  # register gradient dataset tool
def create_gradient_dataset(  # function to create datasets with color transitions
    data: List[Union[int, float]],  # numerical values for the dataset
    label: str,  # series label text
    start_color: str = "rgba(255, 99, 132, 0.8)",  # beginning color for the gradient
    end_color: str = "rgba(54, 162, 235, 0.8)"  # terminal color for the gradient
) -> str:  # returns dataset JSON fragment
    """
    Create a dataset configuration with gradient colors.
    """
    dataset = {  # structure dataset map
        "label": label,  # assign provided label
        "data": data,  # assign numerical data
        "backgroundColor": {  # custom gradient indicator for client-side processing
            "type": "gradient",  # specify gradient fill
            "colors": [start_color, end_color]  # provide start/end color tuple
        },
        "borderColor": start_color,  # set primary border color to match start
        "borderWidth": 2  # set stroke width
    }
    
    return json.dumps(dataset, indent=2)  # return pretty JSON string

@mcp.tool()  # register waterfall chart tool
def create_waterfall_chart(  # function for showing incremental value changes
    labels: List[str],  # labels for each sequential step
    data: List[Union[int, float]],  # values representing changes (positive/negative)
    title: str = "Waterfall Chart",  # main chart header
    color_palette: str = "professional"  # styling palette
) -> str:  # returns waterfall configuration JSON
    """
    Create a waterfall chart showing cumulative effect of sequential values.
    """
    colors = COLOR_PALETTES.get(color_palette, COLOR_PALETTES["professional"])  # fetch colors
    
    # Logic to calculate base cumulative offsets for waterfall effect
    cumulative = []  # list to hold the invisible 'base' bars
    running_total = 0  # track the cumulative floor
    background_colors = []  # list to hold positive/negative markers
    
    for i, value in enumerate(data):  # process each step values
        cumulative.append(running_total)  # set current base to current running total
        running_total += value  # update running total with current change
        # Color coding: Green for growth, red for reduction
        if value >= 0:  # check if change is positive
            background_colors.append("rgba(75, 192, 192, 0.8)")  # apply teal-green
        else:  # if value is negative
            background_colors.append("rgba(255, 99, 132, 0.8)")  # apply rose-red
    
    config = {  # structure the dual-dataset bar configuration
        "type": "bar",  # technical type is stacked bar
        "data": {  # setup data property
            "labels": labels,  # map step labels
            "datasets": [  # waterfall uses two datasets for stacking behavior
                {  # the invisible base dataset
                    "label": "Base",  # internal label
                    "data": cumulative,  # assign calculated bases
                    "backgroundColor": "rgba(0, 0, 0, 0)"  # fully transparent
                },
                {  # the visible change dataset
                    "label": "Change",  # internal label
                    "data": data,  # assign raw changes
                    "backgroundColor": background_colors  # apply directional colors
                }
            ]
        },
        "options": {  # chart behavior settings
            "responsive": True,  # maintain resize flexibility
            "plugins": {  # configure core plugins
                "title": {  # component for chart header
                    "display": True,  # make header visible
                    "text": title,  # apply provided title text
                    "font": {"size": 18}  # styling for header font
                },
                "legend": {  # legend visibility
                    "display": True  # show data key
                }
            },
            "scales": {  # coordinate mapping for stacking
                "x": {"stacked": True},  # enable horizontal stacking
                "y": {"stacked": True, "beginAtZero": True}  # enable vertical stacking & zero origin
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON string

@mcp.tool()  # register heatmap tool
def create_heatmap_chart(  # function for matrix-based temperature/density plots
    x_labels: List[str],  # labels for matrix columns
    y_labels: List[str],  # labels for matrix rows
    data_matrix: List[List[Union[int, float]]],  # 2D list of values
    title: str = "Heatmap"  # main chart header
) -> str:  # returns heatmap configuration
    """
    Create a heatmap chart using matrix data.
    """
    # Logic to flatten the 2D matrix for bubble chart representation
    bubble_data = []  # list to hold coordinates and radii
    max_val = max(max(row) for row in data_matrix)  # find highest value for scaling
    
    for y_idx, row in enumerate(data_matrix):  # loop through rows (Y-axis)
        for x_idx, value in enumerate(row):  # loop through columns (X-axis)
            bubble_data.append({  # append data point
                "x": x_idx,  # index position on X
                "y": y_idx,  # index position on Y
                "r": (value / max_val) * 20 + 5  # calculate radius based on value
            })
    
    config = {  # structure base config
        "type": "bubble",  # technical type is bubble (simulating heatmap)
        "data": {  # data components
            "datasets": [{  # heatmap dataset
                "label": "Heatmap",  # series label
                "data": bubble_data,  # assign flattened data
                "backgroundColor": "rgba(255, 99, 132, 0.6)"  # apply heatmap color
            }]
        },
        "options": {  # layout behavior settings
            "responsive": True,  # maintain resize flexibility
            "plugins": {  # configure core plugins
                "title": {  # component for chart header
                    "display": True,  # ensure title visibility
                    "text": title,  # apply title text
                    "font": {"size": 18}  # styling for font
                },
                "tooltip": {  # component for point interaction
                    "callbacks": {  # custom logic for hover tooltips
                        "label": "function(context) { return 'Value: ' + context.raw.r; }"  # display raw value
                    }
                }
            },
            "scales": {  # coordinate mapping settings
                "x": {  # horizontal axis settings
                    "type": "category",  # treat indices as categories
                    "labels": x_labels,  # map provided column labels
                    "offset": True  # center bubbles on labels
                },
                "y": {  # vertical axis settings
                    "type": "category",  # treat indices as categories
                    "labels": y_labels,  # map provided row labels
                    "offset": True  # center bubbles on labels
                }
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON configuration

@mcp.tool()  # register candlestick tool
def create_candlestick_chart(  # function for financial OHLC visualizations
    labels: List[str],  # time-based category labels
    data: List[Dict[str, float]],  # list of objects with open/high/low/close keys
    title: str = "Candlestick Chart"  # main chart header
) -> str:  # returns candlestick configuration
    """
    Create a candlestick/OHLC chart for financial data.
    """
    # Logic to simulate candlestick representation using bar chart structures
    config = {  # structure init
        "type": "bar",  # technical type set to bar
        "data": {  # define datasets
            "labels": labels,  # map provided time labels
            "datasets": [  # primary visual series
                {  # candlestick visual simulation
                    "label": "Low-High",  # series descriptor
                    "data": [d["high"] - d["low"] for d in data],  # calculate bar length (spread)
                    "backgroundColor": [  # dynamic color based on close direction
                        "rgba(75, 192, 192, 0.6)" if d["close"] >= d["open"]  # green for gains
                        else "rgba(255, 99, 132, 0.6)" for d in data  # red for losses
                    ]
                }
            ]
        },
        "options": {  # layout behavior settings
            "responsive": True,  # allow auto-resize
            "plugins": {  # logic plugins configuration
                "title": {  # header plugin components
                    "display": True,  # make header visible
                    "text": title,  # apply title text
                    "font": {"size": 18}  # apply styling to font
                },
                "tooltip": {  # interaction component
                    "enabled": True  # show data on hover
                }
            },
            "scales": {  # axis coordinate mapping
                "y": {"beginAtZero": False}  # disable zero origin for price context
            }
        }
    }
    return json.dumps(config, indent=2)  # return serialized JSON

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
@mcp.tool()  # register realtime tool
def create_realtime_chart_config(  # function for streaming data dashboards
    initial_labels: List[str],  # labels for starting state
    initial_data: List[Union[int, float]],  # values for starting state
    title: str = "Real-time Data Stream",  # main chart header
    max_data_points: int = 50  # buffer limit for rolling window
) -> str:  # returns realtime configuration
    """
    Create a chart configuration optimized for real-time data streaming.
    """
    config = {  # structure init
        "type": "line",  # base type is line chart
        "data": {  # define data components
            "labels": initial_labels,  # assign starting labels
            "datasets": [{  # primary data stream
                "label": "Live Sync",  # series label
                "data": initial_data,  # assign starting data
                "borderColor": "rgba(54, 162, 235, 1)",  # visual stroke color
                "tension": 0.4,  # apply line smoothing
                "fill": False  # disable area fill
            }]
        },
        "options": {  # interaction behavior settings
            "responsive": True,  # allow window resizing
            "plugins": {  # feature plugins
                "title": {  # header plugin
                    "display": True,  # show title
                    "text": title  # apply text
                }
            },
            "scales": {  # axis mapping
                "x": {  # horizontal mapping
                    "display": True,  # show X axis
                    "title": {  # label for X
                        "display": True,  # show label
                        "text": "Time"  # set text
                    }
                },
                "y": {  # vertical mapping
                    "display": True,  # show Y axis
                    "title": {  # label for Y
                        "display": True,  # show label
                        "text": "Value"  # set text
                    }
                }
            },
            "animation": {  # transition settings
                "duration": 300  # fast animations for updates
            }
        },
        "maxDataPoints": max_data_points  # metadata for streaming logic
    }
    return json.dumps(config, indent=2)  # return serialized JSON string

@mcp.tool()  # register responsive tool
def add_responsive_breakpoints(  # function for mobile-friendly behaviors
    chart_config: str,  # previous chart JSON
    breakpoints: Optional[Dict[str, Dict[str, Any]]] = None  # optional custom overrides
) -> str:  # returns updated configuration
    """
    Add responsive breakpoints to a chart configuration.
    """
    config = json.loads(chart_config)  # parse input JSON
    
    default_breakpoints = {  # standard screen-size rules
        "mobile": {  # phone settings
            "maxWidth": 480,  # trigger threshold
            "options": {  # layout overrides
                "plugins": {  # sub-plugin overrides
                    "legend": {"position": "bottom"},  # move legend down
                    "title": {"font": {"size": 14}}  # shrink header font
                }
            }
        },
        "tablet": {  # tablet settings
            "maxWidth": 768,  # trigger threshold
            "options": {  # layout overrides
                "plugins": {  # sub-plugin overrides
                    "legend": {"position": "top"},  # move legend up
                    "title": {"font": {"size": 16}}  # medium header font
                }
            }
        },
        "desktop": {  # computer settings
            "minWidth": 769,  # trigger threshold
            "options": {  # layout overrides
                "plugins": {  # sub-plugin overrides
                    "legend": {"position": "right"},  # move legend aside
                    "title": {"font": {"size": 18}}  # large header font
                }
            }
        }
    }
    
    config["responsive_breakpoints"] = breakpoints or default_breakpoints  # assign rules
    return json.dumps(config, indent=2)  # return updated JSON

@mcp.tool()  # register accessibility tool
def add_accessibility_features(  # function for inclusive data design
    chart_config: str,  # input chart JSON
    enable_keyboard_nav: bool = True,  # toggle arrow-key navigation
    enable_screen_reader: bool = True  # toggle voice descriptions
) -> str:  # returns accessible configuration
    """
    Add accessibility features to a chart configuration.
    """
    config = json.loads(chart_config)  # parse input JSON
    
    if "options" not in config:  # ensure options object exists
        config["options"] = {}  # initialize if missing
    
    if "plugins" not in config["options"]:  # ensure plugins object exists
        config["options"]["plugins"] = {}  # initialize if missing
    
    config["options"]["plugins"]["a11y"] = {  # configure a11y plugin
        "enabled": True,  # activate plugin
        "keyboardNavigation": enable_keyboard_nav,  # set keyboard state
        "screenReaderAnnouncements": enable_screen_reader  # set announcement state
    }
    
    # Logic to add standard ARIA metadata
    config["aria"] = {  # structure ARIA object
        "label": config.get("options", {}).get("plugins", {}).get("title", {}).get("text", "Chart"),  # use title if available
        "describedBy": "chart-description"  # link to visual description
    }
    
    return json.dumps(config, indent=2)  # return updated JSON

@mcp.tool()  # register cumulative transformation tool
def transform_data_cumulative(  # function to compute growth/totals
    data: List[Union[int, float]]  # input data series
) -> str:  # returns cumulative results
    """
    Transform data into cumulative sum.
    """
    cumulative = []  # results container
    running_sum = 0  # accumulator variable
    for value in data:  # iterate through items
        running_sum += value  # add current to total
        cumulative.append(running_sum)  # store snapshot
    
    return json.dumps({  # return paired results
        "original": data,  # include source
        "cumulative": cumulative  # include transformed
    }, indent=2)  # format JSON output

@mcp.tool()  # register moving average tool
def transform_data_moving_average(  # function for data smoothing
    data: List[Union[int, float]],  # input data series
    window_size: int = 3  # smoothing period length
) -> str:  # returns averaged results
    """
    Calculate moving average of data.
    """
    moving_avg = []  # container for results
    for i in range(len(data)):  # iterate through indices
        start = max(0, i - window_size + 1)  # determine period start
        window = data[start:i + 1]  # extract slice
        moving_avg.append(sum(window) / len(window))  # compute and store mean
    
    return json.dumps({  # return rich results
        "original": data,  # include source
        "moving_average": [round(v, 2) for v in moving_avg],  # round for UI
        "window_size": window_size  # include used setting
    }, indent=2)  # format output

@mcp.tool()  # register pct change tool
def transform_data_percentage_change(  # function for volatility/growth analysis
    data: List[Union[int, float]]  # input data series
) -> str:  # returns change results
    """
    Calculate percentage change between consecutive values.
    """
    pct_change = [0]  # First value has no relative entry
    for i in range(1, len(data)):  # loop from second item
        if data[i - 1] != 0:  # protect against div by zero
            change = ((data[i] - data[i - 1]) / data[i - 1]) * 100  # math formula
            pct_change.append(round(change, 2))  # store rounded result
        else:  # handle zero baseline
            pct_change.append(0)  # assign zero change
    
    return json.dumps({  # return paired output
        "original": data,  # include source
        "percentage_change": pct_change  # include delta sequence
    }, indent=2)  # format JSON output

@mcp.tool()  # register merge tool
def merge_chart_datasets(  # function to combine data sources
    chart_config1: str,  # first input JSON
    chart_config2: str,  # second input JSON
    title: str = "Merged Chart"  # header for result
) -> str:  # returns unified configuration
    """
    Merge datasets from two chart configurations.
    """
    config1 = json.loads(chart_config1)  # parse first input
    config2 = json.loads(chart_config2)  # parse second input
    
    merged_config = {  # structure unified config
        "type": config1.get("type", "bar"),  # inherit chart type
        "data": {  # unified data object
            "labels": config1.get("data", {}).get("labels", []),  # use first labels
            "datasets": (  # list concatenation of datasets
                config1.get("data", {}).get("datasets", []) +  # items from first
                config2.get("data", {}).get("datasets", [])    # items from second
            )
        },
        "options": config1.get("options", {})  # inherit layout behavior
    }
    
    if "plugins" not in merged_config["options"]:  # ensure plugin root exists
        merged_config["options"]["plugins"] = {}  # init if missing
    
    merged_config["options"]["plugins"]["title"] = {  # update title plugin
        "display": True,  # show header
        "text": title,  # apply new title
        "font": {"size": 18}  # apply visual styling
    }
    
    return json.dumps(merged_config, indent=2)  # return serialized JSON

@mcp.tool()  # register theme tool
def create_theme_preset(  # function for bulk visual styling
    theme_name: str = "dark"  # selection key for style
) -> str:  # returns theme values
    """
    Get a complete theme preset for charts.
    """
    themes = {  # style dictionary
        "dark": {  # carbon deep theme
            "backgroundColor": "#1a1a1a",  # canvas background
            "textColor": "#e0e0e0",  # label/legend text
            "gridColor": "rgba(255, 255, 255, 0.1)",  # axis lines
            "palette": COLOR_PALETTES["vibrant"]  # active dataset colors
        },
        "light": {  # clean white theme
            "backgroundColor": "#ffffff",  # canvas background
            "textColor": "#333333",  # label/legend text
            "gridColor": "rgba(0, 0, 0, 0.1)",  # axis lines
            "palette": COLOR_PALETTES["professional"]  # active dataset colors
        },
        "ocean": {  # navy maritime theme
            "backgroundColor": "#0a1929",  # canvas background
            "textColor": "#b2d8ff",  # text color
            "gridColor": "rgba(178, 216, 255, 0.1)",  # grid color
            "palette": [  # custom naval palette
                "rgba(54, 162, 235, 0.8)",  # blue
                "rgba(26, 188, 156, 0.8)",  # teal
                "rgba(52, 152, 219, 0.8)",  # light blue
                "rgba(22, 160, 133, 0.8)"   # moss
            ]
        },
        "sunset": {  # twilight orange theme
            "backgroundColor": "#2d1b2e",  # background
            "textColor": "#ffcccb",  # text color
            "gridColor": "rgba(255, 204, 203, 0.1)",  # grid color
            "palette": [  # warm color palette
                "rgba(255, 99, 132, 0.8)",  # pink
                "rgba(255, 159, 64, 0.8)",  # orange
                "rgba(255, 206, 86, 0.8)",  # yellow
                "rgba(255, 179, 186, 0.8)"  # coral
            ]
        },
        "forest": {  # nature green theme
            "backgroundColor": "#1a2f1a",  # background
            "textColor": "#c8e6c9",  # text color
            "gridColor": "rgba(200, 230, 201, 0.1)",  # grid color
            "palette": [  # organic palette
                "rgba(75, 192, 192, 0.8)",  # teal
                "rgba(22, 160, 133, 0.8)",  # jade
                "rgba(46, 125, 50, 0.8)",   # forest
                "rgba(76, 175, 80, 0.8)"    # grass
            ]
        },
        "neon": {  # synthwave black theme
            "backgroundColor": "#000000",  # background
            "textColor": "#00ff00",  # text color
            "gridColor": "rgba(0, 255, 0, 0.2)",  # grid color
            "palette": [  # hyper-saturated palette
                "rgba(0, 255, 0, 0.8)",    # lime
                "rgba(255, 0, 255, 0.8)",  # magenta
                "rgba(0, 255, 255, 0.8)",  # cyan
                "rgba(255, 255, 0, 0.8)"   # lemon
            ]
        }
    }
    
    return json.dumps(themes.get(theme_name, themes["light"]), indent=2)  # return selection or default

@mcp.tool()  # register tooltip tool
def add_interactive_tooltips(  # function for data hover interactions
    chart_config: str,  # input chart JSON
    tooltip_mode: str = "index",  # hover trigger mode
    show_percentages: bool = False  # toggle logic for relative values
) -> str:  # returns interactive configuration
    """
    Add advanced interactive tooltips to a chart.
    """
    config = json.loads(chart_config)  # parse input JSON
    
    if "options" not in config:  # ensure options object exists
        config["options"] = {}  # init if missing
    
    if "plugins" not in config["options"]:  # ensure plugins object exists
        config["options"]["plugins"] = {}  # init if missing
    
    config["options"]["plugins"]["tooltip"] = {  # configure tooltip sub-object
        "enabled": True,  # activate tooltips
        "mode": tooltip_mode,  # apply selected mode
        "intersect": False,  # trigger even when not directly over point
        "backgroundColor": "rgba(0, 0, 0, 0.8)",  # box background
        "titleColor": "#fff",  # title font color
        "bodyColor": "#fff",   # content font color
        "borderColor": "rgba(255, 255, 255, 0.3)",  # box stroke
        "borderWidth": 1,      # stroke thickness
        "padding": 12,         # internal spacing
        "displayColors": True, # show dataset swatch
        "callbacks": {  # custom logic for label text
            "label": "function(context) { return context.dataset.label + ': ' + context.parsed.y; }"  # dynamic label
        }
    }
    
    if show_percentages:  # check for extra logic
        config["options"]["plugins"]["tooltip"]["callbacks"]["afterLabel"] = \
            "function(context) { return '(' + Math.round(context.parsed.y / total * 100) + '%)'; }"  # add extra line
    
    return json.dumps(config, indent=2)  # return updated JSON

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
@mcp.tool()  # register zoom tool
def add_zoom_pan_controls(  # function for chart navigation
    chart_config: str,  # input chart JSON
    enable_zoom: bool = True,  # toggle zoom feature
    enable_pan: bool = True,   # toggle pan feature
    zoom_mode: str = "xy"      # navigation directions
) -> str:  # returns interactive configuration
    """
    Add zoom and pan controls to a chart.
    """
    config = json.loads(chart_config)  # parse input JSON
    
    if "options" not in config:  # check for options root
        config["options"] = {}  # init if missing
    
    if "plugins" not in config["options"]:  # check for plugins root
        config["options"]["plugins"] = {}  # init if missing
    
    config["options"]["plugins"]["zoom"] = {  # configure zoom/pan plugin
        "zoom": {  # magnification settings
            "enabled": enable_zoom,  # set toggle state
            "mode": zoom_mode,       # set direction
            "speed": 0.1             # sensitivity setting
        },
        "pan": {  # translation settings
            "enabled": enable_pan,   # set toggle state
            "mode": zoom_mode        # set direction
        },
        "limits": {  # movement boundaries
            "x": {"min": "original", "max": "original"},  # clamp to first bounds
            "y": {"min": "original", "max": "original"}   # clamp to first bounds
        }
    }
    
    return json.dumps(config, indent=2)  # return updated JSON configuration

@mcp.tool()  # register filter tool
def filter_chart_data(  # function to prune data by logic
    labels: List[str],  # input category labels
    datasets: List[Dict[str, Any]],  # input dataset objects
    filter_condition: str,  # selection logic key
    threshold: Union[int, float]  # comparison value
) -> str:  # returns pruned result
    """
    Filter chart data based on a condition.
    """
    filtered_labels = []  # container for passing labels
    filtered_datasets = []  # container for passing data
    
    # Logic to identify indices that pass the filter
    if datasets:  # check if source is valid
        first_dataset_data = datasets[0].get("data", [])  # use primary as baseline
        matching_indices = []  # indices of survivors
        
        for i, value in enumerate(first_dataset_data):  # loop through measurements
            match = False  # default mismatch
            if filter_condition == "greater_than" and value > threshold:  # test upper
                match = True  # mark success
            elif filter_condition == "less_than" and value < threshold:  # test lower
                match = True  # mark success
            elif filter_condition == "equals" and value == threshold:  # test identity
                match = True  # mark success
            elif filter_condition == "not_equals" and value != threshold:  # test difference
                match = True  # mark success
            
            if match:  # check for pass
                matching_indices.append(i)  # save index
                if i < len(labels):  # protect bounds
                    filtered_labels.append(labels[i])  # keep corresponding label
        
        # Logic to apply pruning across all datasets
        for dataset in datasets:  # loop through all series
            filtered_dataset = dataset.copy()  # clone structure
            original_data = dataset.get("data", [])  # extract source data
            filtered_dataset["data"] = [original_data[i] for i in matching_indices if i < len(original_data)]  # extract survivors
            filtered_datasets.append(filtered_dataset)  # store pruned series
    
    return json.dumps({  # return results object
        "labels": filtered_labels,  # include pruned categories
        "datasets": filtered_datasets,  # include pruned measurements
        "filter_applied": {  # metadata for confirmation
            "condition": filter_condition,  # report used logic
            "threshold": threshold,  # report used value
            "original_count": len(labels),  # report input size
            "filtered_count": len(filtered_labels)  # report output size
        }
    }, indent=2)  # format output JSON

@mcp.tool()  # register stats tool
def add_statistical_overlay(  # function to add baseline/trend lines
    chart_config: str,  # input chart JSON
    show_mean: bool = True,  # toggle average line
    show_median: bool = True, # toggle midpoint line
    show_std_dev: bool = False # toggle dispersion bands (placeholder)
) -> str:  # returns enriched configuration
    """
    Add statistical overlay lines to a chart.
    """
    config = json.loads(chart_config)  # parse input JSON
    
    # Logic to compute stats from the primary dataset
    if "data" in config and "datasets" in config["data"] and config["data"]["datasets"]:  # validation
        first_dataset = config["data"]["datasets"][0]  # isolate baseline series
        data = first_dataset.get("data", [])  # extract numeric values
        
        if data:  # ensure values exist
            mean = sum(data) / len(data)  # compute arithmetic average
            sorted_data = sorted(data)    # sort for median calculation
            median = sorted_data[len(data) // 2] if len(data) % 2 else \
                     (sorted_data[len(data) // 2 - 1] + sorted_data[len(data) // 2]) / 2  # midpoint logic
            
            labels = config["data"].get("labels", [])  # get categories for line sizing
            
            if show_mean:  # check toggle for mean
                config["data"]["datasets"].append({  # inject mean dataset
                    "label": "Mean",  # display name
                    "data": [mean] * len(labels),  # solid baseline value
                    "type": "line",  # render as line
                    "borderColor": "rgba(255, 206, 86, 1)",  # yellow color
                    "borderWidth": 2,  # stroke width
                    "borderDash": [5, 5],  # dashed style
                    "fill": False,  # disable filling
                    "pointRadius": 0  # hide individual points
                })
            
            if show_median:  # check toggle for median
                config["data"]["datasets"].append({  # inject median dataset
                    "label": "Median",  # display name
                    "data": [median] * len(labels),  # solid baseline value
                    "type": "line",  # render as line
                    "borderColor": "rgba(153, 102, 255, 1)", # purple color
                    "borderWidth": 2,  # stroke width
                    "borderDash": [10, 5], # long dash style
                    "fill": False,  # disable filling
                    "pointRadius": 0  # hide individual points
                })
    
    return json.dumps(config, indent=2)  # return updated JSON configuration

@mcp.tool()  # register export tool
def export_chart_as_image_html(  # function to generate download gateway
    chart_config: str,  # input chart JSON
    filename: str = "chart.png",  # target download name
    width: int = 800,   # visual width
    height: int = 600   # visual height
) -> str:  # returns complete HTML document
    """
    Generate HTML with JavaScript to export chart as image.
    """
    # Multi-line string generating a self-contained renderer/exporter page
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Chart Export</title>
    <!-- Include CDN for Chart.js rendering -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Canvas for rendering -->
    <canvas id="myChart" width="{width}" height="{height}"></canvas>
    <!-- Interactive trigger for download -->
    <button onclick="downloadChart()">Download Chart</button>
    
    <script>
        // Logic to render the Chart.js instance using the provided config
        const ctx = document.getElementById('myChart').getContext('2d');
        const config = {chart_config};
        const myChart = new Chart(ctx, config);
        
        // Logic to convert canvas to image and trigger system download
        function downloadChart() {{
            const url = myChart.toBase64Image(); // capture frame
            const link = document.createElement('a'); // create dummy anchor
            link.download = '{filename}'; // set target filename
            link.href = url; // set data URI as source
            link.click(); // programmatically trigger click
        }}
    </script>
</body>
</html>"""
    
    return html  # return the generated HTML markup

if __name__ == "__main__":  # check if script is being run directly
    mcp.run()  # launch the FastMCP server instance and start listening

