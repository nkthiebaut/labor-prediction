# Labor prediction

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/nkthiebaut/labor-prediction/main)

Messing with [Streamlit](https://streamlit.io) and the [Birth Dataset from the CDC](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm).

## Development

1. Download the 2019 US birth data from the [website of the CDC](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/DVS/natality/Nat2019us.zip) and unzip it (the corresponding documentation is available [here](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/UserGuide2019-508.pdf)).
2. Run the preprocessing script: `bash preprocessing.sh`
3. Install requirements: `pip install -r requirements.txt`
4. Run the app: `streamlit run streamlit_app.py`
