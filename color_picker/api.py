# ===== color_picker/api.py =====
import frappe
import base64
import io
from PIL import Image
import colorsys

@frappe.whitelist()
def analyze_image_colors(image_data, max_colors=5):
    """تحليل ألوان الصورة باستخدام الذكاء الاصطناعي"""
    try:
        # فك تشفير البيانات
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]
        
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
        
        # تصغير الصورة لتسريع المعالجة
        img.thumbnail((150, 150))
        
        # استخراج الألوان المهيمنة
        colors = extract_dominant_colors(img, max_colors)
        
        return {
            "success": True,
            "colors": colors,
            "total_colors": len(colors)
        }
        
    except Exception as e:
        frappe.log_error(f"خطأ في تحليل الصورة: {str(e)}")
        return {
            "success": False,
            "error": "فشل في تحليل الصورة"
        }

def extract_dominant_colors(img, max_colors):
    """استخراج الألوان المهيمنة من الصورة"""
    # تحويل لـ RGB
    img = img.convert('RGB')
    
    # الحصول على البيكسلات
    pixels = list(img.getdata())
    
    # حساب تكرار كل لون
    color_count = {}
    for pixel in pixels:
        if pixel in color_count:
            color_count[pixel] += 1
        else:
            color_count[pixel] = 1
    
    # ترتيب الألوان حسب التكرار
    sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
    
    # إرجاع أهم الألوان
    dominant_colors = []
    for i, (color, count) in enumerate(sorted_colors[:max_colors]):
        r, g, b = color
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        
        # تحويل لـ HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        hsl = {
            "h": int(h * 360),
            "s": int(s * 100), 
            "l": int(l * 100)
        }
        
        dominant_colors.append({
            "rank": i + 1,
            "hex": hex_color,
            "rgb": f"rgb({r}, {g}, {b})",
            "hsl": f"hsl({hsl['h']}, {hsl['s']}%, {hsl['l']}%)",
            "percentage": round((count / len(pixels)) * 100, 2)
        })
    
    return dominant_colors

@frappe.whitelist()
def save_color_palette(palette_data):
    """حفظ مجموعة ألوان جديدة"""
    try:
        # إنشاء مستند جديد
        doc = frappe.new_doc("Color Palette")
        doc.palette_name = palette_data.get("name", "مجموعة ألوان جديدة")
        doc.description = palette_data.get("description", "")
        doc.is_public = palette_data.get("is_public", 0)
        
        # إضافة الألوان
        for color_data in palette_data.get("colors", []):
            doc.append("colors", {
                "color_name": color_data.get("name", "لون"),
                "hex_value": color_data.get("hex"),
                "rgb_value": color_data.get("rgb"),
                "hsl_value": color_data.get("hsl")
            })
        
        doc.insert()
        
        return {
            "success": True,
            "name": doc.name,
            "message": "تم حفظ مجموعة الألوان بنجاح"
        }
        
    except Exception as e:
        frappe.log_error(f"خطأ في حفظ مجموعة الألوان: {str(e)}")
        return {
            "success": False,
            "error": "فشل في حفظ مجموعة الألوان"
