import streamlit as st
import leafmap.geemap7 as leafmap
import ee

st.set_page_config(layout="wide")

st.title("crop monitoring")
st.markdown("""
crop monitoring to support farm
""")

# 1. الاتصال بـ Google Earth Engine
try:
    ee.Initialize()
except Exception as e:
    st.error("authonticate Google Earth Engine")

# 2. setup map
m = leafmap.Map(center=[31.34, 34.34], zoom=14) 

# 3.  NDVI
def get_ndvi(roi):
    dataset = (ee.ImageCollection('COPERNICUS/S2_SR')
               .filterBounds(roi)
               .filterDate('2024-01-01', '2024-12-31')
               .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
               .median())
    
    ndvi = dataset.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi

# 4. 
region = ee.Geometry.BBox(34.30, 31.30, 34.38, 31.40)

# 5
ndvi_image = get_ndvi(region)
ndvi_vis = {
    'min': 0,
    'max': 0.8,
    'palette': ['red', 'yellow', 'green']
}

m.add_layer(ndvi_image, ndvi_vis, 'NDVI (crop health)')
m.add_colorbar(ndvi_vis, label="crop health index")

#  Streamlit
m.to_streamlit(height=600)

st.info("green vegetation")
