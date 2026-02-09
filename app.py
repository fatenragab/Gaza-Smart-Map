import streamlit as st
import leafmap.geemap7 as leafmap
import ee

st.set_page_config(layout="wide")

st.title("crop monitoring")
st.markdown("""
هذا التطبيق يستخدم بيانات الأقمار الصناعية (Sentinel-2) لتحليل صحة المحاصيل 
في المناطق الشرقية لخان يونس لدعم المزارعين في اتخاذ قرارات الري.
""")

# 1. الاتصال بـ Google Earth Engine
try:
    ee.Initialize()
except Exception as e:
    st.error("يرجى التأكد من تفعيل حساب Google Earth Engine")

# 2. إعداد الخريطة التفاعلية
m = leafmap.Map(center=[31.34, 34.34], zoom=14) # إحداثيات شرق خان يونس

# 3. وظيفة جلب بيانات NDVI
def get_ndvi(roi):
    dataset = (ee.ImageCollection('COPERNICUS/S2_SR')
               .filterBounds(roi)
               .filterDate('2024-01-01', '2024-12-31')
               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
               .median())
    
    ndvi = dataset.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi

# 4. تحديد المنطقة الجغرافية (شرق خان يونس)
region = ee.Geometry.BBox(34.30, 31.30, 34.38, 31.40)

# 5. إضافة الطبقات للخريطة
ndvi_image = get_ndvi(region)
ndvi_vis = {
    'min': 0,
    'max': 0.8,
    'palette': ['red', 'yellow', 'green']
}

m.add_layer(ndvi_image, ndvi_vis, 'NDVI (صحة النبات)')
m.add_colorbar(ndvi_vis, label="مؤشر صحة النبات")

# عرض الخريطة في Streamlit
m.to_streamlit(height=600)

st.info("اللون الأخضر يمثل نباتات صحية، الأحمر يمثل تربة جافة أو مناطق عمرانية.")
