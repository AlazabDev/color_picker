from frappe import _

def get_data():
    return {
        "Color Picker": {
            "color": "#667eea",
            "icon": "fa fa-paint-brush", 
            "type": "module",
            "label": _("Color Picker"),
            "description": _("Advanced Color Picker and Analysis Tools"),
            "category": "Tools",
            "items": [
                {
                    "type": "page",
                    "name": "color-picker",
                    "label": _("Color Picker Tool"),
                    "description": _("Extract colors from images with advanced tools")
                },
                {
                    "type": "doctype",
                    "name": "Color Palette",
                    "label": _("Color Palettes"),
                    "description": _("Manage and organize color collections")
                },
                {
                    "type": "report", 
                    "name": "Color Usage Analytics",
                    "label": _("Color Analytics"),
                    "description": _("Analysis and statistics of color usage")
                }
            ]
        }
    }
