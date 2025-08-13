# ===== color_picker/color_picker/doctype/color_palette/color_palette.js =====
frappe.ui.form.on('Color Palette', {
    refresh: function(frm) {
        // إضافة أزرار مخصصة
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('تصدير CSS'), function() {
                frm.call('export_css').then(r => {
                    if (r.message) {
                        frappe.show_alert({
                            message: __('تم نسخ CSS إلى الحافظة'),
                            indicator: 'green'
                        });
                        copy_to_clipboard(r.message);
                    }
                });
            });
            
            frm.add_custom_button(__('تصدير JSON'), function() {
                frm.call('export_json').then(r => {
                    if (r.message) {
                        download_file(r.message, `${frm.doc.palette_name}.json`);
                    }
                });
            });
            
            frm.add_custom_button(__('فتح منتقي الألوان'), function() {
                window.open('/color-picker', '_blank');
            });
        }
        
        // إضافة زر في الأعلى
        frm.add_custom_button(__('منتقي الألوان'), function() {
            window.open('/color-picker', '_blank');
        }, __('Tools'));
    },
    
    palette_name: function(frm) {
        // تنظيف اسم المجموعة
        if (frm.doc.palette_name) {
            frm.set_value('palette_name', frm.doc.palette_name.trim());
        }
    }
});

frappe.ui.form.on('Color Palette Item', {
    hex_value: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.hex_value) {
            // تحويل تلقائي لـ RGB و HSL
            let rgb = hex_to_rgb(row.hex_value);
            let hsl = rgb_to_hsl(rgb.r, rgb.g, rgb.b);
            
            frappe.model.set_value(cdt, cdn, 'rgb_value', `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`);
            frappe.model.set_value(cdt, cdn, 'hsl_value', `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`);
        }
    }
});

// دوال مساعدة
function hex_to_rgb(hex) {
    let result = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16), 
        b: parseInt(result[3], 16)
    } : null;
}

function rgb_to_hsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
        h = s = 0;
    } else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    
    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}

function copy_to_clipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('تم النسخ بنجاح');
    });
}

function download_file(content, filename) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
