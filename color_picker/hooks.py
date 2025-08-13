from . import __version__ as app_version

app_name = "color_picker"
app_title = "Color Picker"
app_publisher = "Azab Tools"
app_description = "Advanced Color Picker Tool for extracting colors from images"
app_icon = "fa fa-paint-brush"
app_color = "#667eea"
app_email = "info@azabtools.com"
app_license = "MIT"
app_version = "1.0.0"

# Website routing
website_route_rules = [
    {"from_route": "/color-picker", "to_route": "color-picker.html"},
    {"from_route": "/tools/colors", "to_route": "color-picker.html"},
]

# Web pages that are disabled
website_generators = ["Color Palette"]

# Add to desk
app_include_css = ["/assets/color_picker/css/color_picker.css"]
app_include_js = ["/assets/color_picker/js/color_picker.js"]

# PWA Settings
website_context = {
    "favicon": "/assets/color_picker/img/favicon.ico",
    "splash_image": "/assets/color_picker/img/icon-512.png"
}

# Permissions
has_permission = {
    "Color Palette": "color_picker.color_picker.doctype.color_palette.color_palette.has_permission"
}

# Scheduled tasks
scheduler_events = {
    "daily": [
        "color_picker.tasks.cleanup_old_color_data"
    ],
    "weekly": [
        "color_picker.tasks.generate_analytics_report"
    ]
}

# Boot session
boot_session = "color_picker.utils.boot_session"

# Standard includes
standard_portal_menu_items = [
    {
        "title": "Color Picker",
        "route": "/color-picker",
        "reference_doctype": "Color Palette",
        "role": "Customer"
    }
]

# Fixtures
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["name", "in", [
            "User-favorite_colors",
            "User-color_history"
        ]]]
    }
]

# Background jobs
background_jobs = {
    "color_analysis": {
        "method": "color_picker.api.analyze_image_colors",
        "timeout": 300
    }
}
