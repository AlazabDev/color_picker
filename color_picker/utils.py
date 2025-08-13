# ===== color_picker/utils.py =====
import frappe

def boot_session(bootinfo):
    """إضافة بيانات لجلسة المستخدم"""
    bootinfo.color_picker = {
        "version": "1.0.0",
        "features": {
            "pwa_enabled": True,
            "offline_mode": True,
            "camera_support": True
        }
    }
    
    # إضافة مجموعات الألوان المفضلة للمستخدم
    if frappe.session.user != "Guest":
        user_palettes = frappe.get_all(
            "Color Palette",
            filters={"created_by": frappe.session.user},
            fields=["name", "palette_name"],
            limit=5
        )
        bootinfo.color_picker["user_palettes"] = user_palettes
