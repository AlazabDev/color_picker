# ===== color_picker/tasks.py =====
import frappe
from frappe.utils import add_days, nowdate

def cleanup_old_color_data():
    """تنظيف البيانات القديمة يومياً"""
    # حذف الصور المؤقتة الأكبر من 7 أيام
    old_date = add_days(nowdate(), -7)
    
    # يمكن إضافة منطق التنظيف هنا
    frappe.db.sql("""
        DELETE FROM `tabFile` 
        WHERE file_url LIKE '%color_picker_temp%' 
        AND creation < %s
    """, old_date)
    
    frappe.db.commit()
    print(f"تم تنظيف الملفات المؤقتة الأقدم من {old_date}")

def generate_analytics_report():
    """إنشاء تقرير تحليلي أسبوعي"""
    # إحصائيات الاستخدام
    total_palettes = frappe.db.count("Color Palette")
    public_palettes = frappe.db.count("Color Palette", {"is_public": 1})
    
    # الألوان الأكثر استخداماً
    popular_colors = frappe.db.sql("""
        SELECT hex_value, COUNT(*) as count
        FROM `tabColor Palette Item`
        GROUP BY hex_value
        ORDER BY count DESC
        LIMIT 10
    """, as_dict=True)
    
    print(f"📊 تقرير أسبوعي:")
    print(f"   • إجمالي المجموعات: {total_palettes}")
    print(f"   • المجموعات العامة: {public_palettes}")
    print(f"   • الألوان الشائعة: {len(popular_colors)}")
