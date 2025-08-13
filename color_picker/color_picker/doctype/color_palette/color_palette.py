# ===== color_picker/color_picker/doctype/color_palette/color_palette.py =====
import frappe
from frappe.model.document import Document
import json

class ColorPalette(Document):
    def before_save(self):
        """تنفيذ قبل الحفظ"""
        # تعيين المنشئ تلقائياً
        if not self.created_by:
            self.created_by = frappe.session.user
            
        # تحديث عداد الاستخدام
        if not self.usage_count:
            self.usage_count = 0
            
        # التحقق من صحة الألوان
        self.validate_colors()
        
    def validate_colors(self):
        """التحقق من صحة بيانات الألوان"""
        if not self.colors:
            frappe.throw("يجب إضافة لون واحد على الأقل")
            
        for color in self.colors:
            # التحقق من صيغة HEX
            if color.hex_value and not self.is_valid_hex(color.hex_value):
                frappe.throw(f"صيغة HEX غير صحيحة: {color.hex_value}")
                
    def is_valid_hex(self, hex_value):
        """التحقق من صحة كود HEX"""
        import re
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(pattern, hex_value))
        
    def increment_usage(self):
        """زيادة عداد الاستخدام"""
        self.usage_count = (self.usage_count or 0) + 1
        self.save()
        
    def get_dominant_color(self):
        """الحصول على اللون الأكثر استخداماً"""
        if self.colors:
            return self.colors[0].hex_value
        return "#667eea"
        
    @frappe.whitelist()
    def export_css(self):
        """تصدير كـ CSS Variables"""
        css_vars = []
        for i, color in enumerate(self.colors):
            var_name = f"--{self.palette_name.lower().replace(' ', '-')}-{i+1}"
            css_vars.append(f"{var_name}: {color.hex_value};")
        return "\\n".join(css_vars)
        
    @frappe.whitelist()
    def export_json(self):
        """تصدير كـ JSON"""
        colors_data = []
        for color in self.colors:
            colors_data.append({
                "name": color.color_name,
                "hex": color.hex_value,
                "rgb": color.rgb_value,
                "hsl": color.hsl_value
            })
        return json.dumps(colors_data, ensure_ascii=False, indent=2)

@frappe.whitelist()
def get_public_palettes(limit=20):
    """الحصول على المجموعات العامة"""
    return frappe.get_all(
        "Color Palette",
        filters={"is_public": 1},
        fields=["name", "palette_name", "description", "usage_count"],
        order_by="usage_count desc",
        limit=limit
    )

@frappe.whitelist()
def search_palettes(query, limit=10):
    """البحث في مجموعات الألوان"""
    return frappe.get_all(
        "Color Palette", 
        filters={
            "palette_name": ["like", f"%{query}%"],
            "is_public": 1
        },
        fields=["name", "palette_name", "description"],
        limit=limit
    )

def has_permission(doc, user=None, permission_type=None):
    """فحص الصلاحيات"""
    if not user:
        user = frappe.session.user
        
    # المدير العام له كل الصلاحيات
    if user == "Administrator":
        return True
        
    # منشئ المجموعة له كل الصلاحيات
    if doc.created_by == user:
        return True
        
    # المجموعات العامة يمكن قراءتها
    if doc.is_public and permission_type == "read":
        return True
        
    return False
