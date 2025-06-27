import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import requests
import random
import base64
from PIL import Image
from io import BytesIO
import os
import json
import time # For simulating loading

# --- Streamlit 頁面設定 ---
st.set_page_config(
    page_title="健康日記 Health Diary", # 頁籤標題
    page_icon="💖", # 頁籤圖示
    layout="centered", # 頁面佈局為居中
    initial_sidebar_state="collapsed" # 初始側邊欄狀態為收起
)

# --- 自訂 CSS 樣式 ---
# This CSS is carefully crafted to give the Streamlit app a friendly, cute, and responsive look.
# It uses soft pink and deeper pink tones, rounded corners, and subtle shadows for a modern feel.
st.markdown("""
    <style>
        /* Define a global anchor at the very top of the app, before any content */
        html {
            scroll-behavior: smooth; /* Smooth scrolling for anchors */
        }
        #app_top_anchor {
            position: absolute;
            top: 0;
            left: 0;
            visibility: hidden;
        }

        /* 將背景色應用到 Streamlit 應用程式的主容器 */
        .stApp {
            background-color: #fce4ec; /* 淺粉色作為主背景 */
            color: #333333; /* 預設文字顏色 */
        }
        .main {
            padding: 20px;
            border-radius: 10px;
        }

        /* 調整標題和文字顏色 */
        h1, h2, h3, h4, h5, h6 {
            color: #d81b60; /* 深粉色標題 */
            font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif; /* 嘗試卡通字體 */
        }
        p, li, div {
            color: #4a4a4a; /* 深灰色文字 */
            font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif; /* 應用卡通字體到普通文字 */
        }

        /* 按鈕樣式 */
        .stButton>button {
            background-color: #ffb6c1; /* 粉色按鈕 */
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            border: none;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff8b9b; /* 滑鼠懸停時更深的粉色 */
            box-shadow: 0 6px 12px 0 rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }

        /* 輸入框和選擇框樣式 */
        .stTextInput>div>div>input, .stSelectbox>div>div>select, .stDateInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #ffccd5; /* 粉色邊框 */
            padding: 8px;
            box-shadow: 0 2px 4px 0 rgba(0,0,0,0.05);
            font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif; /* 應用卡通字體 */
        }
        /* Markdown 文字樣式 */
        .stMarkdown {
            font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif;
            color: #5d4037; /* 棕色系文字，更溫暖 */
        }
        /* 數據框樣式 */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        }
        /* 訊息框樣式 (success, warning, error) */
        .stAlert {
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stAlert.success {
            background-color: #e8f5e9; /* 淺綠色成功提示 */
            color: #2e7d32;
        }
        .stAlert.warning {
            background-color: #fffde7; /* 淺黃色警告提示 */
            color: #fbc02d;
        }
        .stAlert.error {
            background-color: #ffebee; /* 淺紅色錯誤提示 */
            color: #c62828;
        }
        /* Plotly 圖表容器的背景和圓角 */
        .stPlotlyChart {
            background-color: #ffffff; /* 圖表背景 */
            border-radius: 15px; /* 更大的圓角 */
            padding: 15px; /* 內部間距 */
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.15); /* 更明顯的陰影 */
            margin-bottom: 20px;
        }
        /* LOGO 圖片樣式，用於讓圖片更融入標題 */
        .logo-img {
            vertical-align: middle; /* 垂直居中對齊文字 */
            margin-right: 15px; /* 與文字的間距 */
            border-radius: 50%; /* 如果是正方形圖片，可以變成圓形 */
        }
        /* 頁尾圖片樣式 */
        .footer-image-container {
            text-align: center; /* 讓頁尾圖片居中 */
            margin-top: 30px; /* 與上方內容的間距 */
            padding-top: 20px;
            border-top: 1px solid #ffccd5;
        }

        /* 導覽 Radio 樣式 */
        div.stRadio { /* Targeting the radio group container */
            display: flex; /* Use flexbox */
            justify-content: center; /* Center the buttons horizontally */
            flex-wrap: wrap; /* Allow buttons to wrap to the next line on smaller screens */
            margin-bottom: 20px; /* Space below the navigation */
            gap: 10px; /* Space between the radio buttons */
        }

        div.stRadio > label { /* Targeting each radio button label */
            display: flex; /* Use flexbox for icon and text alignment */
            align-items: center; /* Vertically align items */
            background-color: #ffccd2; /* Lighter pink background */
            padding: 8px 15px;
            border-radius: 20px; /* More rounded corners for a cute, pill-like look */
            border: 1px solid #ff80ab; /* Thin border */
            cursor: pointer;
            transition: all 0.3s ease; /* Smooth transition effects */
            font-weight: bold;
            color: #d81b60; /* Text color */
            white-space: nowrap; /* Prevent text wrapping inside the button */
        }

        div.stRadio > label:hover {
            background-color: #ffafbd; /* Darker pink on hover */
            border-color: #e91e63;
            color: #e91e63;
            transform: translateY(-2px); /* Slight lift effect on hover */
        }

        div.stRadio > label.css-1ccx87l.e16fv1bt2:has(input:checked) { /* Targets the checked state */
            background-color: #e91e63; /* Background color when selected */
            color: white; /* Text color when selected */
            border-color: #e91e63;
            box-shadow: 0 4px 8px rgba(233, 30, 99, 0.3); /* Add shadow when selected */
        }

        div.stRadio > label > div[data-testid="stRadio-0-input"] {
            display: none; /* Hide the actual radio circle */
        }

        div.stRadio > label > div > p {
            margin: 0; /* Remove default paragraph margin */
            padding-left: 5px; /* Space between icon and text */
            color: inherit; /* Ensure text color inherits from parent label */
        }
        /* Hide the "導覽" label for the radio buttons */
        div.stRadio > label[data-testid="stMarkdownContainer"]:first-child {
           
        }


        /* AI Food Recognition result card style */
        .food-recognition-card {
            background-color: #fff0f5; /* 淺粉色背景 */
            border-left: 5px solid #ff69b4; /* 粉色左邊框 */
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .food-recognition-card h5 {
            color: #d81b60;
            margin-top: 0;
            margin-bottom: 5px;
        }
        .food-recognition-card p {
            margin: 0;
            color: #5d4037;
        }
        /* Style for scroll to top button (cute pill shape) */
        .scroll-to-top-btn {
            display: inline-flex; /* Use flex for icon and text alignment */
            align-items: center; /* Vertically align items */
            justify-content: center; /* Center content horizontally */
            background-color: #ffb6c1; /* Light pink background */
            color: white; /* White text/emoji */
            padding: 10px 20px; /* Padding for button feel */
            border-radius: 30px; /* More rounded, pill-like */
            text-decoration: none; /* Removed underline */
            font-weight: bold;
            font-size: 1.1em; /* Slightly larger font for prominence */
            margin-top: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15); /* More prominent shadow */
            transition: all 0.3s ease; /* Smooth transitions */
            cursor: pointer;
        }
        .scroll-to-top-btn:hover {
            background-color: #ff8b9b; /* Darker pink on hover */
            box-shadow: 0 6px 12px rgba(0,0,0,0.25); /* More prominent shadow on hover */
            transform: translateY(-3px); /* Lift effect on hover */
            color: white; /* Ensure text remains white on hover */
        }
        /* AI Recognition Loading Animation (Spinner) */
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .ai-loading-spinner {
            border: 4px solid #f3f3f3; /* Light grey */
            border-top: 4px solid #ff69b4; /* Pink */
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: rotate 1s linear infinite;
            margin: 10px auto; /* Center the spinner */
        }
        /* AI Suggestion Box */
        .ai-suggestion-box {
            background-color: #ffe0f0; /* Very light pink */
            border: 2px dashed #ff8b9b; /* Dashed pink border */
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            text-align: center;
            font-weight: bold;
            color: #d81b60;
            font-size: 1.1em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .ai-suggestion-box .emoji-large {
            font-size: 1.8em;
            vertical-align: middle;
            margin-right: 10px;
        }
        /* New styles for AI recognition section for cute design */
        .stFileUploader {
            border: 2px dashed #ffccd5; /* Lighter pink dashed border */
            border-radius: 12px; /* Rounded corners for uploader */
            padding: 20px;
            background-color: #fffafa; /* Slightly off-white background */
            margin-bottom: 20px;
        }
        .ai-button {
            background-image: linear-gradient(to right, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%); /* Gradient button */
            border: none;
            color: white;
            padding: 12px 25px;
            border-radius: 25px; /* Pill shape */
            font-weight: bold;
            font-size: 1.1em;
            letter-spacing: 1px;
            box-shadow: 0 6px 12px rgba(255,154,158,0.4);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-top: 15px;
            display: block; /* Make button full width */
            width: fit-content; /* Adjust width to content */
            margin-left: auto; /* Center the button */
            margin-right: auto; /* Center the button */
        }
        .ai-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(255,154,158,0.6);
            color: white; /* Ensure text color remains white on hover */
        }
        .ai-button:active {
            transform: translateY(0);
            box-shadow: 0 4px 8px rgba(255,154,158,0.3);
        }
        /* Style for the "確認並新增到我的食物資料庫" button */
        /* Note: Streamlit's internal styling might override specific custom classes for form buttons,
           so targeting kind="primary" is generally more effective for form submit buttons. */
        .stForm button[kind="primary"] { 
            background-image: linear-gradient(to right, #84fab0 0%, #8fd3f4 100%); /* Green-blue gradient for success */
            border: none;
            color: white;
            padding: 12px 25px;
            border-radius: 25px; /* Pill shape */
            font-weight: bold;
            font-size: 1.1em;
            letter-spacing: 1px;
            box-shadow: 0 6px 12px rgba(132,250,176,0.4);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-top: 15px;
        }
        .stForm button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(132,250,176,0.6);
            color: white;
        }
        .stForm button[kind="primary"]:active {
            transform: translateY(0);
            box_shadow: 0 4px 8px rgba(132,250,176,0.3);
        }

        /* New styles for food item chips */
        .food-chips-container {
            display: flex;
            flex-wrap: wrap; /* Allow chips to wrap to the next line */
            gap: 8px; /* Space between chips */
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px dashed #ffccd5; /* Light pink dashed border */
            border-radius: 10px;
            background-color: #fffafa; /* Light background for the container */
            min-height: 40px; /* Ensure some height even if empty */
            align-items: center; /* Center items vertically */
        }
        .food-chip {
            background-color: #ffeadb; /* Lighter peach for chips */
            color: #d81b60; /* Deep pink text */
            padding: 6px 12px;
            border-radius: 20px; /* Pill shape for chips */
            font-size: 0.9em;
            font-weight: bold;
            white-space: nowrap; /* Prevent text wrapping inside chip */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        .food-chip:hover {
            transform: translateY(-1px); /* Slight lift on hover */
        }
        /* Styles for the "clear meal" buttons in add record page */
        .clear-meal-button {
            background-color: #f48fb1; /* Medium pink */
            color: white;
            border-radius: 8px;
            padding: 5px 10px;
            font-size: 0.9em;
            margin-top: 10px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            width: fit-content; /* Make button fit content */
            display: block; /* Ensure it's a block element */
            margin-left: auto; /* Push to right */
            margin-right: auto; /* Push to left, effectively centering for small buttons */
        }
        .clear-meal-button:hover {
            background-color: #e91e63; /* Darker pink on hover */
        }
        /* Adjust st.info for compact meal display */
        .stInfo > div {
            padding: 10px;
        }
        /* Styles for the Assistant Page */
        .assistant-plan-card {
            background-color: #fcf8f2; /* Creamy background */
            border: 1px solid #ffe0b2; /* Light orange border */
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }
        .assistant-plan-card h5 {
            color: #ff9800; /* Orange title */
            margin-top: 0;
            margin-bottom: 10px;
        }
        .assistant-plan-card ul {
            list-style-type: none; /* Remove bullet points */
            padding-left: 0;
        }
        .assistant-plan-card ul li {
            margin-bottom: 5px;
            color: #4e342e; /* Dark brown text */
        }
        .assistant-plan-card strong {
            color: #d81b60; /* Deep pink for emphasis */
        }
        .plan-header {
            font-size: 1.3em;
            color: #d81b60;
            margin-top: 10px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .day-header {
            font-size: 1.1em;
            color: #ff8a65; /* Salmon pink for day headers */
            margin-top: 8px;
            margin-bottom: 5px;
            font-weight: bold;
            border-bottom: 1px dashed #ffccbc;
            padding-bottom: 3px;
        }
        /* Styles for Diet Plan Cards within the Assistant Page */
        .diet-plan-card {
            background-color: #fffafa; /* Light background for the card */
            border: 1px solid #ffccd2; /* Light pink border */
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }
        .diet-plan-card h4 {
            color: #d81b60; /* Deep pink for card titles */
            margin-top: 0;
            margin-bottom: 10px;
        }
        .diet-plan-card .stExpander { /* Styling for expanders inside the diet plan card */
            border: none; /* Remove default expander border */
            box-shadow: none; /* Remove default expander shadow */
            margin-bottom: 5px;
        }
        .diet-plan-card .streamlit-expanderHeader {
            background-color: #ffeadb; /* Lighter peach for expander header */
            color: #d81b60;
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: bold;
            border: 1px solid #ffccd2;
            transition: background-color 0.3s ease;
        }
        .diet-plan-card .streamlit-expanderHeader:hover {
            background-color: #ffc2b4; /* Slightly darker peach on hover */
        }
        .diet-plan-card .streamlit-expanderContent {
            background-color: #fff0f5; /* Light pink for expander content */
            border-left: 3px solid #ff80ab; /* Pink left border for content */
            padding: 10px;
            border-radius: 0 0 8px 8px;
            margin-top: -5px;
        }
        .diet-plan-card p, .diet-plan-card li {
            color: #5d4037; /* Darker text for content */
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Define a global anchor at the very top of the application for "scroll to top" functionality
st.markdown("<a name='app_top'></a>", unsafe_allow_html=True)

# --- 定義卡通風格顏色調色盤 ---
# 可愛粉色系和馬卡龍色
CUTE_COLORS = [
    '#ffb6c1', # Light Pink
    '#ffdbcd', # Peach Puff
    '#ffe4e1', # Misty Rose
    '#add8e6', # Light Blue
    '#b0e0e6', # Powder Blue
    '#e6e6fa', # Lavender
    '#f0e68c', # Khaki (light yellow)
    '#98fb98', # Pale Green
    '#dda0dd', # Plum (light)
    '#ffacd9'  # Hot Pink (lighter)
]

# --- 圖片處理 ---
@st.cache_data
def get_base64_image(image_path):
    """
    將圖片檔案轉換為 Base64 編碼字串，用於在 Streamlit 中嵌入圖片。
    參數:
        image_path (str): 圖片檔案的路徑。
    回傳:
        str: Base64 編碼的圖片字串，如果檔案未找到或發生錯誤則回傳 None。
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        # 將錯誤訊息輸出到控制台，而不是直接顯示在應用程式介面上
        print(f"錯誤：圖片檔案未找到: {image_path}，請確認檔案是否存在於相同目錄下。")
        return None
    except Exception as e:
        print(f"錯誤：載入圖片 {image_path} 時發生錯誤: {e}")
        return None

# 載入 LOGO 和頁尾插圖
logo_base64 = get_base64_image("vivi.png")
footer_image_base64 = get_base64_image("S__13418505.jpg")

# --- 資料載入與儲存 ---
DATA_FILE = 'health_data.csv' # 統一使用 health_data.csv

def load_data():
    """
    從 CSV 文件載入健康紀錄數據。
    處理文件不存在或為空的情況，並確保日期列被正確解析。
    回傳:
        pd.DataFrame: 載入的健康紀錄 DataFrame。
    """
    # 定義所有預期的列名，確保順序和一致性
    columns = [
        '日期', '體重(kg)', '目標體重(kg)', '身高(公分)', '性別',
        'BMI', '體脂肪率', '總攝取熱量', '運動類型', '運動時間(分鐘)',
        '運動消耗熱量', '天氣城市', '天氣說明', '氣溫', '健康建議', '總淨熱量',
        '餐點內容'
    ]
    
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            # 嘗試讀取 CSV，直接解析日期為 datetime.date 物件
            df = pd.read_csv(DATA_FILE, parse_dates=['日期'], date_format='%Y-%m-%d')
            df['日期'] = df['日期'].dt.date # 確保是 date 物件
            
            # 確保讀取的 DataFrame 包含所有預期的欄位，如果缺少則補齊
            for col in columns:
                if col not in df.columns:
                    df[col] = None 
            
            # 確保關鍵數值列為數字類型，將非數字值轉換為 NaN，然後填充為 0
            numeric_cols = [
                '體重(kg)', '目標體重(kg)', '身高(公分)', 'BMI', '體脂肪率',
                '總攝取熱量', '運動時間(分鐘)', '運動消耗熱量', '氣溫', '總淨熱量'
            ]
            for col in numeric_cols:
                if col in df.columns:
                    # 使用 errors='coerce' 將無效解析的數據轉為 NaN，然後填充 0
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) 

            # 重新排序列，確保新紀錄和舊紀錄的列順序一致，避免 pd.concat 報錯
            df = df[columns]
            return df
        except pd.errors.EmptyDataError:
            st.warning("歷史紀錄檔案存在但內容為空，將創建新的紀錄表。")
            return pd.DataFrame(columns=columns)
        except Exception as e:
            st.error(f"讀取歷史紀錄時發生錯誤: {e}。請檢查 '{DATA_FILE}' 檔案的日期格式或內容。將創建新的紀錄表。")
            return pd.DataFrame(columns=columns)
    else:
        st.info("歷史紀錄檔案未找到或為空，將創建新的紀錄表。")
        return pd.DataFrame(columns=columns)

# 載入數據到 Session State
if 'df_history' not in st.session_state:
    st.session_state.df_history = load_data()

def save_data(df):
    """
    將 DataFrame 儲存到 CSV 文件。
    參數:
        df (pd.DataFrame): 要儲存的 DataFrame。
    """
    try:
        # 在儲存前，確保日期列是字串格式，以便 CSV 正常儲存
        df_to_save = df.copy() # 避免修改原始 DataFrame
        df_to_save['日期'] = df_to_save['日期'].apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, (datetime.date, datetime.datetime)) else x)
        df_to_save.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"儲存歷史紀錄時發生錯誤: {e}")

# --- 食物資料庫 (會話狀態管理) ---
if 'food_database' not in st.session_state:
    st.session_state.food_database = {
        # 中式
        "白飯(一碗)": {"calories": 280, "category": "中式"},
        "炒麵(一碗)": {"calories": 400, "category": "中式"},
        "滷肉飯(一碗)": {"calories": 350, "category": "中式"},
        "水餃(10顆)": {"calories": 500, "category": "中式"},
        "小籠包(5顆)": {"calories": 350, "category": "中式"},
        "粥(一碗)": {"calories": 150, "category": "中式"},
        "豆漿(250ml)": {"calories": 70, "category": "中式"},
        "油條(一根)": {"calories": 200, "category": "中式"},
        "蚵仔煎(一份)": {"calories": 500, "category": "中式"},
        "大腸麵線(一碗)": {"calories": 400, "category": "中式"},
        "臭豆腐(一份)": {"calories": 350, "category": "中式"},
        "肉圓(一個)": {"calories": 250, "category": "中式"},
        "潤餅(一份)": {"calories": 200, "category": "中式"},
        "涼麵(一份)": {"calories": 350, "category": "中式"},
        "鍋貼(5個)": {"calories": 300, "category": "中式"},
        "水煎包(一個)": {"calories": 180, "category": "中式"},
        "鹹酥雞(100g)": {"calories": 350, "category": "中式"},
        "滷味(100g)": {"calories": 150, "category": "中式"},
        "關東煮(100g)": {"calories": 100, "category": "中式"},
        "牛肉麵(一碗)": {"calories": 600, "category": "中式"},
        "陽春麵(一碗)": {"calories": 350, "category": "中式"},
        "榨菜肉絲麵(一碗)": {"calories": 400, "category": "中式"},
        "排骨酥麵(一碗)": {"calories": 500, "category": "中式"},
        "羹麵(一碗)": {"calories": 450, "category": "中式"},
        "滷味拼盤(一份)": {"calories": 300, "category": "中式"},
        "鹹粥(一碗)": {"calories": 200, "category": "中式"},
        "清粥小菜(一份)": {"calories": 150, "category": "中式"},
        "飯糰(一個)": {"calories": 250, "category": "中式"},
        "海苔飯捲(一個)": {"calories": 300, "category": "中式"},
        "烤地瓜(一個)": {"calories": 200, "category": "中式"},
        "烤玉米(一根)": {"calories": 180, "category": "中式"},
        "紅燒肉(100g)": {"calories": 300, "category": "中式"},
        "麻婆豆腐(一份)": {"calories": 250, "category": "中式"},
        "宮保雞丁(一份)": {"calories": 350, "category": "中式"},
        "糖醋排骨(一份)": {"calories": 400, "category": "中式"},
        "炒青菜(一份)": {"calories": 100, "category": "中式"},
        "番茄炒蛋(一份)": {"calories": 200, "category": "中式"},
        "蒜泥白肉(一份)": {"calories": 300, "category": "中式"},
        "客家小炒(一份)": {"calories": 350, "category": "中式"},
        "三杯雞(一份)": {"calories": 400, "category": "中式"},
        "蛤蜊絲瓜(一份)": {"calories": 150, "category": "中式"},
        "薑絲大腸(一份)": {"calories": 250, "category": "中式"},
        "蒼蠅頭(一份)": {"calories": 280, "category": "中式"},
        "鹹豬肉(100g)": {"calories": 350, "category": "中式"},
        "香腸(一條)": {"calories": 200, "category": "中式"},
        "米腸(一條)": {"calories": 150, "category": "中式"},
        "黑白切(一份)": {"calories": 250, "category": "中式"},
        "滷蛋(一顆)": {"calories": 80, "category": "中式"},
        "海帶(一份)": {"calories": 50, "category": "中式"},
        "豆乾(一份)": {"calories": 60, "category": "中式"},
        "豬血糕(一份)": {"calories": 180, "category": "中式"},
        "粉腸(一份)": {"calories": 100, "category": "中式"},
        "肝連(一份)": {"calories": 120, "category": "中式"},
        "嘴邊肉(一份)": {"calories": 150, "category": "中式"},
        "鯊魚煙(一份)": {"calories": 100, "category": "中式"},
        "透抽(100g)": {"calories": 90, "category": "中式"},
        "小卷(100g)": {"calories": 80, "category": "中式"},
        "中卷(100g)": {"calories": 85, "category": "中式"},
        "花枝(100g)": {"calories": 95, "category": "中式"},
        "墨魚(100g)": {"calories": 80, "category": "中式"},
        "鱈魚(100g)": {"calories": 105, "category": "中式"},
        "鯛魚(100g)": {"calories": 120, "category": "中式"},
        "鯖魚(100g)": {"calories": 200, "category": "中式"},
        "秋刀魚(一條)": {"calories": 250, "category": "中式"},
        "柳葉魚(1條)": {"calories": 50, "category": "中式"},
        "虱目魚(100g)": {"calories": 180, "category": "中式"},
        "吳郭魚(100g)": {"calories": 120, "category": "中式"},
        "草魚(100g)": {"calories": 110, "category": "中式"},
        "鰱魚(100g)": {"calories": 120, "category": "中式"},
        "石斑魚(100g)": {"calories": 95, "category": "中式"},
        "土魠魚羹(一碗)": {"calories": 400, "category": "中式"},
        "肉羹湯(一碗)": {"calories": 180, "category": "中式"},
        "排骨湯(一碗)": {"calories": 250, "category": "中式"},
        "雞湯(一碗)": {"calories": 200, "category": "中式"},
        "鴨肉羹(一碗)": {"calories": 350, "category": "中式"},
        "羊肉爐(一份)": {"calories": 500, "category": "中式"},
        "薑母鴨(一份)": {"calories": 600, "category": "中式"},
        "酸菜白肉鍋(一份)": {"calories": 550, "category": "中式"},
        "麻辣鍋(一份)": {"calories": 700, "category": "中式"},
        "臭臭鍋(一份)": {"calories": 450, "category": "中式"},
        "海鮮鍋(一份)": {"calories": 400, "category": "中式"},
        "牛奶鍋(一份)": {"calories": 450, "category": "中式"},
        "番茄鍋(一份)": {"calories": 350, "category": "中式"},
        "起司鍋(一份)": {"calories": 500, "category": "中式"},
        "壽喜燒(一份)": {"calories": 400, "category": "中式"},
        "石鍋拌飯(一份)": {"calories": 600, "category": "中式"},
        "部隊鍋(一份)": {"calories": 650, "category": "中式"},
        "韓式烤肉(一份)": {"calories": 700, "category": "中式"},
        "泡菜鍋(一份)": {"calories": 450, "category": "中式"},
        "人參雞湯(一碗)": {"calories": 300, "category": "中式"},
        "炸醬麵(一碗)": {"calories": 500, "category": "中式"},
        "海鮮麵(一碗)": {"calories": 450, "category": "中式"},
        "冷麵(一碗)": {"calories": 350, "category": "中式"},
        "豆腐鍋(一份)": {"calories": 300, "category": "中式"},
        "炒年糕(一份)": {"calories": 400, "category": "中式"},
        "辣炒雞排(一份)": {"calories": 550, "category": "中式"},
        "烤肉串(韓式)": {"calories": 180, "category": "中式"},
        "韓式炸雞(一份)": {"calories": 700, "category": "中式"},
        "豬腳飯(一份)": {"calories": 700, "category": "中式"},
        "控肉飯(一份)": {"calories": 650, "category": "中式"},
        "焢肉飯(一份)": {"calories": 650, "category": "中式"},
        "筒仔米糕(一個)": {"calories": 250, "category": "中式"},
        "碗粿(一個)": {"calories": 200, "category": "中式"},
        "鼎邊趖(一碗)": {"calories": 300, "category": "中式"},
        "阿給(一份)": {"calories": 200, "category": "中式"},
        "魚丸(一顆)": {"calories": 30, "category": "中式"},
        "肉羹(一塊)": {"calories": 40, "category": "中式"},
        "排骨酥(一塊)": {"calories": 60, "category": "中式"},
        "油豆腐(一塊)": {"calories": 50, "category": "中式"},
        "板豆腐(100g)": {"calories": 76, "category": "中式"},
        "嫩豆腐(100g)": {"calories": 50, "category": "中式"},
        "雞蛋豆腐(100g)": {"calories": 80, "category": "中式"},
        "臭豆腐(炸)": {"calories": 350, "category": "中式"},
        "臭豆腐(煮)": {"calories": 250, "category": "中式"},
        "麻辣鴨血(一份)": {"calories": 150, "category": "中式"},
        "滷大腸(一份)": {"calories": 200, "category": "中式"},
        "滷豬頭皮(一份)": {"calories": 150, "category": "中式"},
        "滷花生(一份)": {"calories": 200, "category": "中式"},
        "滷蛋(一顆)": {"calories": 80, "category": "中式"},
        "滷豆干(一份)": {"calories": 60, "category": "中式"},
        "滷海帶(一份)": {"calories": 50, "category": "中式"},
        "滷米血(一份)": {"calories": 180, "category": "中式"},
        "鴨血湯(一碗)": {"calories": 100, "category": "中式"},
        "綜合滷味(一份)": {"calories": 300, "category": "中式"},
        "豬血湯(一碗)": {"calories": 120, "category": "中式"},
        "豬肝湯(一碗)": {"calories": 150, "category": "中式"},
        "蚵仔湯(一碗)": {"calories": 100, "category": "中式"},
        "蛤蜊湯(一碗)": {"calories": 80, "category": "中式"},
        "鱸魚湯(一碗)": {"calories": 200, "category": "中式"},
        "味噌魚湯(一碗)": {"calories": 150, "category": "中式"},
        "酸辣湯餃(一份)": {"calories": 400, "category": "中式"},
        "餛飩麵(一碗)": {"calories": 450, "category": "中式"},
        "福州魚丸湯(一碗)": {"calories": 150, "category": "中式"},
        "赤肉羹湯(一碗)": {"calories": 180, "category": "中式"},
        "排骨麵(一碗)": {"calories": 450, "category": "中式"},
        "牛肉燴飯(一份)": {"calories": 600, "category": "中式"},
        "滑蛋蝦仁燴飯(一份)": {"calories": 500, "category": "中式"},
        "廣東炒飯(一份)": {"calories": 700, "category": "中式"},
        "揚州炒飯(一份)": {"calories": 650, "category": "中式"},
        "蛋炒飯(一份)": {"calories": 500, "category": "中式"},
        "蝦仁炒飯(一份)": {"calories": 550, "category": "中式"},
        "牛肉炒飯(一份)": {"calories": 600, "category": "中式"},
        "雞肉炒飯(一份)": {"calories": 550, "category": "中式"},
        "排骨炒飯(一份)": {"calories": 650, "category": "中式"},
        "咖哩炒飯(一份)": {"calories": 600, "category": "中式"},
        "素炒飯(一份)": {"calories": 400, "category": "中式"},
        "火腿蛋炒飯(一份)": {"calories": 550, "category": "中式"},
        "臘味炒飯(一份)": {"calories": 650, "category": "中式"},
        "海鮮炒飯(一份)": {"calories": 600, "category": "中式"},
        "鳳梨炒飯(一份)": {"calories": 550, "category": "中式"},
        "鹹魚雞粒炒飯(一份)": {"calories": 600, "category": "中式"},
        "肉絲炒飯(一份)": {"calories": 550, "category": "中式"},
        "什錦炒飯(一份)": {"calories": 600, "category": "中式"},
        "培根炒飯(一份)": {"calories": 600, "category": "中式"},
        "泡菜炒飯(一份)": {"calories": 550, "category": "中式"},
        "鮭魚炒飯(一份)": {"calories": 600, "category": "中式"},
        "牛肉湯(一碗)": {"calories": 200, "category": "中式"},
        "羊肉湯(一碗)": {"calories": 250, "category": "中式"},
        "豬肝湯(一碗)": {"calories": 150, "category": "中式"},
        "赤肉羹(一份)": {"calories": 180, "category": "中式"},
        "蝦仁羹(一份)": {"calories": 150, "category": "中式"},
        "花枝羹(一份)": {"calories": 180, "category": "中式"},
        "魷魚羹(一份)": {"calories": 160, "category": "中式"},
        "土魠魚羹(一份)": {"calories": 200, "category": "中式"},
        "肉羹(一份)": {"calories": 180, "category": "中式"},
        "小卷米粉(一碗)": {"calories": 300, "category": "中式"},
        "肉燥飯(一碗)": {"calories": 280, "category": "中式"},
        "雞肉飯(一碗)": {"calories": 300, "category": "中式"},
        "火雞肉飯(一碗)": {"calories": 320, "category": "中式"},
        "蝦仁羹麵(一碗)": {"calories": 400, "category": "中式"},
        "肉羹麵(一碗)": {"calories": 420, "category": "中式"},
        "魷魚羹麵(一碗)": {"calories": 400, "category": "中式"},
        "花枝羹麵(一碗)": {"calories": 450, "category": "中式"},
        "土魠魚羹麵(一碗)": {"calories": 480, "category": "中式"},
        "排骨酥麵(一碗)": {"calories": 500, "category": "中式"},
        "赤肉羹麵(一碗)": {"calories": 450, "category": "中式"},
        "乾麵(一碗)": {"calories": 380, "category": "中式"},
        "麻醬麵(一碗)": {"calories": 450, "category": "中式"},
        "酸辣麵(一碗)": {"calories": 420, "category": "中式"},
        "湯麵(一般)": {"calories": 300, "category": "中式"},
        "滷味麵(一份)": {"calories": 400, "category": "中式"},
        "米苔目(一碗)": {"calories": 300, "category": "中式"},
        "粿仔條(一碗)": {"calories": 320, "category": "中式"},
        "意麵(一碗)": {"calories": 350, "category": "中式"},
        "鍋燒意麵(一碗)": {"calories": 400, "category": "中式"},
        "燒餅油條(一份)": {"calories": 450, "category": "中式"},
        "蘿蔔糕(一份)": {"calories": 200, "category": "中式"},
        "包子(一個)": {"calories": 150, "category": "中式"},
        "饅頭(一個)": {"calories": 120, "category": "中式"},
        "稀飯(一碗)": {"calories": 100, "category": "中式"},
        "水煮蛋(一顆)": {"calories": 78, "category": "中式"},
        "蒸蛋(一份)": {"calories": 120, "category": "中式"},
        "皮蛋瘦肉粥(一碗)": {"calories": 280, "category": "中式"},
        # 西式
        "麵包(一片)": {"calories": 150, "category": "西式"},
        "雞胸肉(100g)": {"calories": 165, "category": "西式"},
        "牛肉(100g)": {"calories": 250, "category": "西式"},
        "鮭魚(100g)": {"calories": 208, "category": "西式"},
        "花椰菜(100g)": {"calories": 25, "category": "西式"},
        "蘋果(一個)": {"calories": 95, "category": "西式"},
        "香蕉(一根)": {"calories": 105, "category": "西式"},
        "牛奶(250ml)": {"calories": 150, "category": "西式"},
        "優格(100g)": {"calories": 60, "category": "西式"},
        "雞蛋(一顆)": {"calories": 78, "category": "西式"},
        "豬肉(100g)": {"calories": 242, "category": "西式"},
        "蝦仁(100g)": {"calories": 85, "category": "西式"},
        "糙米飯(一碗)": {"calories": 250, "category": "西式"},
        "全麥麵包(一片)": {"calories": 120, "category": "西式"},
        "地瓜(100g)": {"calories": 86, "category": "西式"},
        "馬鈴薯(100g)": {"calories": 77, "category": "西式"},
        "青菜(100g)": {"calories": 20, "category": "西式"},
        "柳橙(一個)": {"calories": 62, "category": "西式"},
        "葡萄(100g)": {"calories": 69, "category": "西式"},
        "燕麥片(50g)": {"calories": 190, "category": "西式"},
        "鮪魚罐頭(100g)": {"calories": 180, "category": "西式"},
        "起司(一片)": {"calories": 113, "category": "西式"},
        "薯條(100g)": {"calories": 312, "category": "西式"},
        "披薩(一片)": {"calories": 285, "category": "西式"},
        "漢堡(一個)": {"calories": 300, "category": "西式"},
        "三明治(一個)": {"calories": 250, "category": "西式"},
        "咖啡(黑咖啡)": {"calories": 5, "category": "西式"},
        "義大利麵(一份)": {"calories": 400, "category": "西式"},
        "牛排(一份)": {"calories": 600, "category": "西式"},
        "烤雞(一份)": {"calories": 450, "category": "西式"},
        "沙拉(一份)": {"calories": 150, "category": "西式"},
        "濃湯(一碗)": {"calories": 120, "category": "西式"},
        "法式吐司(一片)": {"calories": 200, "category": "西式"},
        "美式鬆餅(一片)": {"calories": 250, "category": "西式"},
        "可頌麵包(一個)": {"calories": 200, "category": "西式"},
        "法式麵包(100g)": {"calories": 260, "category": "西式"},
        "吐司(一片)": {"calories": 80, "category": "西式"},
        "全麥吐司(一片)": {"calories": 70, "category": "西式"},
        "火腿蛋三明治(一份)": {"calories": 280, "category": "西式"},
        "總匯三明治(一份)": {"calories": 400, "category": "西式"},
        "鮪魚三明治(一份)": {"calories": 350, "category": "西式"},
        "雞排三明治(一份)": {"calories": 400, "category": "西式"},
        "卡拉雞腿堡(一個)": {"calories": 500, "category": "西式"},
        "勁辣雞腿堡(一個)": {"calories": 550, "category": "西式"},
        "大麥克(一個)": {"calories": 550, "category": "西式"},
        "麥香雞(一個)": {"calories": 380, "category": "西式"},
        "麥香魚(一個)": {"calories": 350, "category": "西式"},
        "雙層牛肉吉事堡(一個)": {"calories": 450, "category": "西式"},
        "薯餅(一份)": {"calories": 150, "category": "西式"},
        "雞塊(6塊)": {"calories": 280, "category": "西式"},
        "玉米湯(一份)": {"calories": 100, "category": "西式"},
        "可樂(中杯)": {"calories": 180, "category": "西式"},
        "雪碧(中杯)": {"calories": 160, "category": "西式"},
        "紅茶(無糖)": {"calories": 0, "category": "西式"},
        "綠茶(無糖)": {"calories": 0, "category": "西式"},
        "奶茶(中杯)": {"calories": 250, "category": "西式"},
        "咖啡拿鐵(中杯)": {"calories": 180, "category": "西式"},
        "卡布奇諾(中杯)": {"calories": 150, "category": "西式"},
        "摩卡(中杯)": {"calories": 300, "category": "西式"},
        "美式咖啡(中杯)": {"calories": 5, "category": "西式"},
        "冰拿鐵(一份)": {"calories": 200, "category": "西式"},
        # 甜點
        "巧克力(100g)": {"calories": 530, "category": "甜點"},
        "甜甜圈(一個)": {"calories": 250, "category": "甜點"},
        "冰淇淋(一球)": {"calories": 150, "category": "甜點"},
        "布丁(一個)": {"calories": 100, "category": "甜點"},
        "蛋糕(一片)": {"calories": 300, "category": "甜點"},
        "馬卡龍(一個)": {"calories": 100, "category": "甜點"},
        "提拉米蘇(一份)": {"calories": 350, "category": "甜點"},
        "泡芙(一個)": {"calories": 200, "category": "甜點"},
        "鬆餅(一份)": {"calories": 400, "category": "甜點"},
        "雞蛋糕(3個)": {"calories": 150, "category": "甜點"},
        "紅豆餅(一個)": {"calories": 200, "category": "甜點"},
        "車輪餅(一個)": {"calories": 200, "category": "甜點"},
        "仙草(一份)": {"calories": 80, "category": "甜點"},
        "愛玉(一份)": {"calories": 50, "category": "甜點"},
        "粉圓(一份)": {"calories": 150, "category": "甜點"},
        "豆花(一份)": {"calories": 120, "category": "甜點"},
        "湯圓(5顆)": {"calories": 250, "category": "甜點"},
        "紅豆湯(一碗)": {"calories": 200, "category": "甜點"},
        "綠豆湯(一碗)": {"calories": 180, "category": "甜點"},
        "起司蛋糕(一片)": {"calories": 400, "category": "甜點"},
        "千層蛋糕(一片)": {"calories": 450, "category": "甜點"},
        "銅鑼燒(一個)": {"calories": 250, "category": "甜點"},
        "蛋捲(一根)": {"calories": 80, "category": "甜點"},
        "鳳梨酥(一個)": {"calories": 200, "category": "甜點"},
        "太陽餅(一個)": {"calories": 250, "category": "甜點"},
        "老婆餅(一個)": {"calories": 220, "category": "甜點"},
        "綠豆椪(一個)": {"calories": 300, "category": "甜點"},
        "月餅(一個)": {"calories": 400, "category": "甜點"},
        "麻糬(一個)": {"calories": 100, "category": "甜點"},
        "紅龜粿(一個)": {"calories": 180, "category": "甜點"},
        "草仔粿(一個)": {"calories": 150, "category": "甜點"},
        "巧克力餅乾(一片)": {"calories": 60, "category": "甜點"},
        "洋芋片(一包)": {"calories": 200, "category": "甜點"},
        "爆米花(一份)": {"calories": 150, "category": "甜點"},
        "牛奶糖(一顆)": {"calories": 25, "category": "甜點"},
        "軟糖(一份)": {"calories": 100, "category": "甜點"},
        "棒棒糖(一根)": {"calories": 50, "category": "甜點"},
        "黑巧克力(100g)": {"calories": 580, "category": "甜點"},
        "珍珠奶茶(大杯)": {"calories": 400, "category": "甜點"},
        "刨冰(一份)": {"calories": 300, "category": "甜點"},
        "雪花冰(一份)": {"calories": 400, "category": "甜點"},
        "芒果冰(一份)": {"calories": 500, "category": "甜點"},
        # 水果
        "西瓜(100g)": {"calories": 30, "category": "水果"}, "鳳梨(100g)": {"calories": 50, "category": "水果"},
        "香瓜(100g)": {"calories": 35, "category": "水果"}, "木瓜(100g)": {"calories": 43, "category": "水果"},
        "芭樂(100g)": {"calories": 68, "category": "水果"}, "蓮霧(100g)": {"calories": 35, "category": "水果"},
        "釋迦(100g)": {"calories": 100, "category": "水果"}, "芒果(100g)": {"calories": 60, "category": "水果"},
        "龍眼(100g)": {"calories": 60, "category": "水果"}, "荔枝(100g)": {"calories": 66, "category": "水果"},
        "櫻桃(100g)": {"calories": 50, "category": "水果"}, "草莓(100g)": {"calories": 32, "category": "水果"},
        "藍莓(100g)": {"calories": 57, "category": "水果"}, "奇異果(一個)": {"calories": 60, "category": "水果"},
        "火龍果(100g)": {"calories": 50, "category": "水果"}, "酪梨(100g)": {"calories": 160, "category": "水果"},
        "榴槤(100g)": {"calories": 147, "category": "水果"}, "山竹(100g)": {"calories": 73, "category": "水果"},
        "葡萄柚(一個)": {"calories": 52, "category": "水果"}, "檸檬(一個)": {"calories": 29, "category": "水果"},
        "番茄(100g)": {"calories": 18, "category": "水果"}, "小番茄(100g)": {"calories": 18, "category": "水果"},
        # 蔬菜
        "小黃瓜(100g)": {"calories": 15, "category": "蔬菜"}, "高麗菜(100g)": {"calories": 25, "category": "蔬菜"},
        "大白菜(100g)": {"calories": 13, "category": "蔬菜"}, "空心菜(100g)": {"calories": 20, "category": "蔬菜"},
        "菠菜(100g)": {"calories": 23, "category": "蔬菜"}, "地瓜葉(100g)": {"calories": 29, "category": "蔬菜"},
        "金針菇(100g)": {"calories": 25, "category": "蔬菜"}, "香菇(100g)": {"calories": 26, "category": "蔬菜"},
        "杏鮑菇(100g)": {"calories": 34, "category": "蔬菜"}, "豆腐乳(10g)": {"calories": 20, "category": "蔬菜"},
        "泡菜(100g)": {"calories": 30, "category": "蔬菜"}, "海帶芽(100g)": {"calories": 44, "category": "蔬菜"},
        "黑木耳(100g)": {"calories": 25, "category": "蔬菜"}, "白木耳(100g)": {"calories": 20, "category": "蔬菜"},
        "金針花(100g)": {"calories": 30, "category": "蔬菜"}, "玉米筍(100g)": {"calories": 26, "category": "蔬菜"},
        "筊白筍(100g)": {"calories": 22, "category": "蔬菜"}, "青椒(100g)": {"calories": 20, "category": "蔬菜"},
        "紅椒(100g)": {"calories": 26, "category": "蔬菜"}, "黃椒(100g)": {"calories": 27, "category": "蔬菜"},
        "苦瓜(100g)": {"calories": 19, "category": "蔬菜"}, "絲瓜(100g)": {"calories": 17, "category": "蔬菜"},
        "冬瓜(100g)": {"calories": 13, "category": "蔬菜"}, "南瓜(100g)": {"calories": 26, "category": "蔬菜"},
        "大蒜(10g)": {"calories": 15, "category": "蔬菜"}, "薑(10g)": {"calories": 8, "category": "蔬菜"},
        "蔥(10g)": {"calories": 5, "category": "蔬菜"}, "洋蔥(100g)": {"calories": 40, "category": "蔬菜"},
        # 穀物與澱粉
        "玉米(100g)": {"calories": 86, "category": "穀物與澱粉"}, "綠豆(100g)": {"calories": 340, "category": "穀物與澱粉"},
        "紅豆(100g)": {"calories": 330, "category": "穀物與澱粉"}, "芋頭(100g)": {"calories": 115, "category": "穀物與澱粉"},
        "山藥(100g)": {"calories": 108, "category": "穀物與澱粉"}, "蓮藕(100g)": {"calories": 74, "category": "穀物與澱粉"},
        "荸薺(100g)": {"calories": 67, "category": "穀物與澱粉"}, "菱角(100g)": {"calories": 116, "category": "穀物與澱粉"},
        # 堅果與種子
        "花生(100g)": {"calories": 567, "category": "堅果與種子"}, "腰果(100g)": {"calories": 553, "category": "堅果與種子"},
        "核桃(100g)": {"calories": 654, "category": "堅果與種子"}, "杏仁(100g)": {"calories": 579, "category": "堅果與種子"},
        "開心果(100g)": {"calories": 562, "category": "堅果與種子"}, "瓜子(100g)": {"calories": 572, "category": "堅果與種子"},
        "黑芝麻(100g)": {"calories": 573, "category": "堅果與種子"}, "白芝麻(100g)": {"calories": 597, "category": "堅果與種子"},
        "奇亞籽(10g)": {"calories": 48, "category": "堅果與種子"}, "亞麻籽(10g)": {"calories": 53, "category": "堅果與種子"},
        "蕎麥(100g)": {"calories": 343, "category": "穀物與澱粉"}, "藜麥(100g)": {"calories": 368, "category": "穀物與澱粉"},
        "小米(100g)": {"calories": 378, "category": "穀物與澱粉"},
        # 肉類與海鮮
        "雞胸肉(100g)": {"calories": 165, "category": "肉類與海鮮"}, "牛肉(100g)": {"calories": 250, "category": "肉類與海鮮"},
        "鮭魚(100g)": {"calories": 208, "category": "肉類與海鮮"}, "豬肉(100g)": {"calories": 242, "category": "肉類與海鮮"},
        "蝦仁(100g)": {"calories": 85, "category": "肉類與海鮮"}, "鮪魚罐頭(100g)": {"calories": 180, "category": "肉類與海鮮"},
        # 乳製品與蛋
        "牛奶(250ml)": {"calories": 150, "category": "乳製品與蛋"}, "優格(100g)": {"calories": 60, "category": "乳製品與蛋"},
        "雞蛋(一顆)": {"calories": 78, "category": "乳製品與蛋"}, "起司(一片)": {"calories": 113, "category": "乳製品與蛋"},
        # 其他零食
        "餅乾(一片)": {"calories": 50, "category": "其他零食"}, "花生醬(10g)": {"calories": 60, "category": "其他零食"},
        "果醬(10g)": {"calories": 30, "category": "其他零食"},
    }

# --- 運動類型及每分鐘消耗卡路里 (參考值) ---
if 'exercise_calories_per_min' not in st.session_state:
    st.session_state.exercise_calories_per_min = {
        "慢跑": 10, "游泳": 8, "騎自行車": 7, "快走": 5, "瑜伽": 3,
        "重訓": 6, "跳繩": 12, "球類運動": 9, "有氧舞蹈": 7,
        "跑步機": 9, "橢圓機": 7, "划船機": 8, "階梯機": 10,
        "飛輪": 11, "高強度間歇訓練(HIIT)": 15, "拳擊/踢拳": 13, "壁球": 12,
        "籃球": 10, "足球": 11, "排球": 6, "網球": 8,
        "羽毛球": 7, "桌球": 5, "高爾夫球(步行)": 5, "滑雪(下坡)": 7,
        "滑雪(越野)": 10, "溜冰": 6, "直排輪": 7, "舞蹈": 6,
        "尊巴(Zumba)": 8, "普拉提(Pilates)": 4, "太極拳": 3, "柔道": 10,
        "跆拳道": 11, "空手道": 9, "攀岩": 9, "抱石": 10,
        "划獨木舟/皮划艇": 4, "立槳衝浪": 5, "衝浪": 6, "滑板": 5,
        "徒步旅行(平坦)": 6, "徒步旅行(山地)": 9, "背包旅行": 10, "園藝": 4,
        "割草": 5, "打掃房屋": 3, "洗車": 4, "洗碗": 2,
        "遛狗": 3, "購物(步行)": 2, "做飯": 3, "睡覺": 1,
        "閱讀": 1, "看電視": 1, "辦公室工作": 2, "駕駛": 2,
        "釣魚(站立)": 2, "打獵": 5, "射箭": 3, "保齡球": 3,
        "撞球": 3, "飛鏢": 2, "開合跳": 10, "波比跳": 15,
        "仰臥起坐": 6, "伏地挺身": 7, "深蹲": 8, "弓箭步": 7,
        "平板支撐": 5, "引體向上": 12, "單槓懸垂": 4, "雙槓屈臂伸": 10,
        "戰繩": 14, "壺鈴擺盪": 12, "農夫走路": 8, "輪椅籃球": 8,
        "輪椅網球": 7, "手搖自行車": 6, "水中有氧": 5, "沙灘排球": 10,
        "攀岩訓練": 11, "越野跑": 12, "馬拉松訓練": 13, "鐵人三項訓練": 14,
        "街舞": 8, "芭蕾舞": 7, "國標舞": 6, "肚皮舞": 5,
        "體操": 9, "舉重": 10, "競技體操": 11, "跳水": 4,
        "韻律操": 6, "體育舞蹈": 7, "擊劍": 8, "摔跤": 9,
        "划船": 8, "帆船": 4, "風帆": 5, "水上摩托車": 6,
        "水上滑板": 7, "潛水(浮潛)": 3, "潛水(深潛)": 6, "馬術": 5,
        "射擊": 2, "高空跳傘": 7, "滑翔翼": 5, "滑翔傘": 5,
        "滑翔機": 4, "熱氣球": 2, "高空彈跳": 8, "滑索": 6,
        "跳傘": 7, "越野車": 8, "卡丁車": 7, "極限單車": 9,
        "山地自行車": 8, "公路自行車": 7, "特技自行車": 9, "城市騎行": 6,
        "遛狗(快走)": 4, "跑步機(快走)": 6, "跑步機(坡度)": 11, "橢圓機(高強度)": 9,
        "划船機(高強度)": 10, "動感單車": 12, "攀登(室內)": 9, "攀登(室外)": 10,
        "抱石(室內)": 10, "抱石(室外)": 11, "瑜伽(熱瑜伽)": 5, "皮拉提斯(器械)": 6,
        "體能訓練": 10, "核心訓練": 8, "平衡訓練": 4, "柔韌訓練": 3,
        "復健運動": 3, "伸展運動": 2, "冥想": 1, "深呼吸練習": 1,
        "散步(慢)": 2, "散步(中速)": 3, "散步(快)": 4, "爬樓梯": 8,
        "上下樓梯": 7, "站立工作": 2, "唱歌": 2, "彈奏樂器": 3,
        "繪畫": 2, "寫作": 2, "打字": 1, "園藝(重度)": 6,
        "搬家": 8, "修車": 5, "洗澡": 1, "穿衣服": 1,
        "吃飯": 1, "喝水": 0, "看書": 1, "玩遊戲(坐著)": 1,
        "玩遊戲(站著)": 2, "說話": 1, "大笑": 1, "哭泣": 1,
    }

# 計算 BMI 函數
def calculate_bmi(weight, height):
    """計算身體質量指數 (BMI)。"""
    if height > 0:
        return weight / ((height / 100) ** 2)
    return 0

# 計算基礎代謝率 (BMR) 和每日總能量消耗 (TDEE) 函數
def calculate_bmr_tdee(gender, weight, height, age, activity_level):
    """計算基礎代謝率 (BMR) 和每日總能量消耗 (TDEE)。"""
    # 根據性別計算 BMR (Harris-Benedict Equation)
    if gender == "男性":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else: # 女性
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 定義活動程度的乘數 (TDEE 使用，BMR 不變)
    activity_multipliers = {
        "久坐 (很少運動)": 1.2,
        "輕度運動 (每週1-3天)": 1.375,
        "中度運動 (每週3-5天)": 1.55,
        "高度運動 (每週6-7天)": 1.725,
        "非常高度運動 (每天訓練)": 1.9
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2) # 獲取活動係數，如果未定義則默認為久坐
    return bmr, tdee

# 計算每餐熱量的函數
def calculate_meal_calories(selected_foods_list_names, food_db):
    """根據選擇的食物計算總熱量。"""
    total_meal_cal = 0
    meal_details = {} # 用於儲存食物名稱和其對應熱量
    for item_name in selected_foods_list_names:
        if item_name in food_db:
            calories = food_db[item_name]["calories"]
            total_meal_cal += calories
            meal_details[item_name] = calories
    return total_meal_cal, meal_details

# 天氣運動建議函數
def get_weather_exercise_suggestion(weather_desc, temperature):
    """根據天氣情況給出運動建議。"""
    suggestion = "根據天氣，建議您"

    weather_desc_lower = weather_desc.lower()

    if "雨" in weather_desc_lower or "下雨" in weather_desc_lower or "雷" in weather_desc_lower:
        suggestion += "在室內運動，例如：瑜伽、跑步機、重訓、室內游泳。"
    elif temperature < 10:
        suggestion += "注意保暖，進行溫和的室內運動，如瑜伽或輕量重訓，避免感冒。"
    elif temperature > 30 and ("晴" in weather_desc_lower or "熱" in weather_desc_lower):
        suggestion += "避免高強度戶外運動，或選擇清晨/傍晚時段，並多補充水分，預防中暑。"
    elif "晴" in weather_desc_lower or "多雲" in weather_desc_lower or "陰" in weather_desc_lower:
        suggestion += "適合戶外活動！可以考慮慢跑、騎自行車、健走、球類運動，享受好天氣。"
    else:
        suggestion += "選擇您喜歡的運動，保持活力！"

    return suggestion

# --- Plotly 圖表樣式設定 (自定義卡通/手繪風格) ---
def get_cute_plotly_template():
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Arial Rounded MT Bold, sans-serif", size=12, color="#5d4037"), # 卡通字體，棕色
            title_font_size=18,
            title_font_color="#d81b60", # 深粉色標題
            paper_bgcolor='rgba(0,0,0,0)', # 背景透明，讓CSS背景生效
            plot_bgcolor='rgba(0,0,0,0)', # 圖表區背景透明
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial Rounded MT Bold"),
            xaxis=dict(
                showgrid=False, # 不顯示網格線
                showline=True, linecolor="#ffb6c1", linewidth=2, # 粉色軸線
                tickfont=dict(color="#5d4037"),
                title_font_color="#d81b60",
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False, # 不顯示網格線
                showline=True, linecolor="#ffb6c1", linewidth=2, # 粉色軸線
                tickfont=dict(color="#5d4037"),
                title_font_color="#d81b60",
                zeroline=False,
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0.7)", # 輕微透明白色背景
                bordercolor="#ffb6c1",
                borderwidth=1,
                font=dict(color="#5d4037"),
                orientation="h", # 水平圖例
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=80, b=40), # 調整邊距
        )
    )

px.defaults.template = get_cute_plotly_template() # 將自定義模板設為 Plotly Express 的預設

# --- 頁面定義 ---
def get_greeting():
    """
    根據當前時間生成不同的問候語。
    這個函數已經進行了測試和優化，使其更準確地判斷時間段。
    如果因環境因素導致仍有誤差，可考慮簡化問候語為更通用內容。
    """
    current_hour = datetime.datetime.now().hour

    # 更精確的時間段劃分
    if 5 <= current_hour <= 10: # 早上 5 點到上午 10 點
        return "早安！新的一天，能量滿滿！☀️"
    elif 11 <= current_hour <= 13: # 上午 11 點到下午 1 點
        return "午安！享用美味午餐了嗎？🥗"
    else: # 下午 2 點到凌晨 4 點
        return "晚安！辛苦一天了，是時候回顧今日的健康成果！🌙"


def home_page(df_history):
    """
    生成應用程式的首頁內容，包含歡迎語和健康概覽。
    參數:
        df_history (pd.DataFrame): 包含用戶健康歷史紀錄的 DataFrame。
    """
    # Removed specific anchor here, using global 'app_top'

    greeting = get_greeting()

    # 健康小語列表
    health_quotes = [
        "每一次的選擇，都在塑造更好的你。",
        "保持健康，就是對自己最好的投資！",
        "運動讓身體發光，健康讓生活精彩！",
        "均衡飲食是健康之路的基石。",
        "聆聽身體的聲音，它會告訴你答案。",
        "每天一點點進步，累積成健康大成功！",
        "微笑是最好的良藥，保持好心情喔！",
        "多喝水，多運動，保持好心情！💖",
        "健康是財富，而記錄是累積財富的過程。",
        "讓健康成為一種習慣，而不是一時的努力。"
    ]
    random_quote = random.choice(health_quotes)

    st.write(f"### {greeting}")
    st.markdown(f"<p style='font-family: \"Comic Sans MS\", \"Arial Rounded MT Bold\", sans-serif; color: #8b0000; font-size: 1.0em; text-align: left; margin-top: 0; font-weight: bold;'>{random_quote}</p>", unsafe_allow_html=True)
    st.write("---")

    st.subheader("📊 您的健康概覽")
    st.write("在這裡，您可以快速掌握最新的健康數據，輕鬆了解自己的身體變化！")

    if not df_history.empty:
        # 確保日期是 datetime.date 對象，以便排序和顯示
        df_history['日期'] = pd.to_datetime(df_history['日期']).dt.date
        df_history_sorted = df_history.sort_values(by='日期', ascending=True)

        # 獲取最新一筆紀錄
        latest_record = df_history_sorted.iloc[-1]

        # 顯示最近的健康概覽數據
        st.markdown(f"<p style='font-size: 1.1em;'>**🗓️ 最近紀錄日期:** <span style='color: #8b0000; font-weight: bold;'>{latest_record['日期']}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1.1em;'>**⚖️ 最新體重:** <span style='color: #8b0000; font-weight: bold;'>{latest_record['體重(kg)']:.1f} kg</span></p>", unsafe_allow_html=True)

        if 'BMI' in latest_record and pd.notna(latest_record['BMI']):
            st.markdown(f"<p style='font-size: 1.1em;'>**📏 最新 BMI:** <span style='color: #8b0000; font-weight: bold;'>{latest_record['BMI']:.2f}</span></p>", unsafe_allow_html=True)
        if '體脂肪率' in latest_record and pd.notna(latest_record['體脂肪率']):
            st.markdown(f"<p style='font-size: 1.1em;'>**💪 最新體脂率:** <span style='color: #8b0000; font-weight: bold;'>{latest_record['體脂肪率']:.1f} %</span></p>", unsafe_allow_html=True)
        
        # 新增基礎代謝 (BMR)
        # 從 session state 獲取年齡和性別，用於 BMR 計算
        user_age = st.session_state.get('age', 25) # 預設年齡
        user_gender = st.session_state.get('gender', '男性') # 預設性別
        
        # 確保有有效的體重和身高來計算 BMR
        if pd.notna(latest_record['體重(kg)']) and pd.notna(latest_record['身高(公分)']) and latest_record['體重(kg)'] > 0 and latest_record['身高(公分)'] > 0:
            bmr_value, _ = calculate_bmr_tdee(user_gender, latest_record['體重(kg)'], latest_record['身高(公分)'], user_age, "久坐 (很少運動)")
            st.markdown(f"<p style='font-size: 1.1em;'>**⚡ 基礎代謝率 (BMR):** <span style='color: #8b0000; font-weight: bold;'>{bmr_value:.0f} kcal</span></p>", unsafe_allow_html=True)


        # 體重變化趨勢圖 (改為卡通風格平滑折線圖)
        if len(df_history_sorted) > 1: # 至少有兩筆資料才適合繪製趨勢圖
            st.subheader("📈 體重變化趨勢")
            st.write("透過圖表，您可以清楚看到體重的變化軌跡，以及與目標體重的差距。")
            # 確保日期是唯一的，若有多筆同日數據，取最後一筆
            df_weight = df_history_sorted.drop_duplicates(subset=['日期'], keep='last').copy()
            df_weight['日期_dt'] = pd.to_datetime(df_weight['日期']) # 轉換為 datetime 類型
            
            # 確保 '目標體重(kg)' 欄位存在且為數值，如果不存在則填充為 0.0
            if '目標體重(kg)' not in df_weight.columns:
                 df_weight['目標體重(kg)'] = 0.0 # 預設值
            df_weight['目標體重(kg)'] = pd.to_numeric(df_weight['目標體重(kg)'], errors='coerce').fillna(0)


            fig_weight = px.line(df_weight, x='日期_dt', y=['體重(kg)', '目標體重(kg)'],
                                  color_discrete_sequence=[CUTE_COLORS[1], CUTE_COLORS[4]], # 蜜桃粉和淺藍
                                  labels={'value': '體重(kg)', 'variable': '類型'},
                                  title='體重變化趨勢',
                                  markers=True) # 顯示標記點

            fig_weight.update_traces(mode='lines+markers', line=dict(width=3), # 粗線條
                                     marker=dict(size=10, symbol='circle', # 可愛圓點
                                                 line=dict(width=2, color='white')), # 白色邊框
                                     hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial Rounded MT Bold"))
            fig_weight.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="日期",
                yaxis_title="體重 (kg)",
                legend_title_text="",
                hovermode="x unified" # 統一懸停效果
            )
            st.plotly_chart(fig_weight, use_container_width=True, key="home_weight_chart")
        else:
            st.info("至少需要兩筆紀錄才能繪製體重趨勢圖，加油喔！")

    else:
        st.info("您還沒有任何紀錄，請前往 '新增紀錄' 頁面添加。健康日記期待您的第一筆紀錄！")

    st.markdown("---")
    st.info("健康小提示：多喝水，多運動，保持好心情！💖")
    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)

def add_record_page():
    # Removed specific anchor here, using global 'app_top'

    st.header("✍️ 新增紀錄")
    st.write("每一份用心紀錄，都是對健康的投資！今天有什麼新發現呢？")
    st.write("---")

    # 初始化 meal_food_list 到 session state
    if 'breakfast_food_list' not in st.session_state:
        st.session_state.breakfast_food_list = []
    if 'lunch_food_list' not in st.session_state:
        st.session_state.lunch_food_list = []
    if 'dinner_food_list' not in st.session_state:
        st.session_state.dinner_food_list = []

    # 初始化儲存計數器 (用於圖表 key 的唯一性)
    if 'save_counter' not in st.session_state:
        st.session_state.save_counter = 0

    # --- 飲食紀錄 (整合新增食物區塊) ---
    st.subheader("🍱 飲食紀錄")
    st.write("從豐富的食物資料庫中選擇您今日所食用的餐點，輕鬆計算熱量！")

    # 選擇食物分類 (優化顯示)
    all_categories = sorted(list(set([data["category"] for data in st.session_state.food_database.values()])))
    food_categories_options = ["所有分類"] + all_categories
    selected_category = st.selectbox("選擇食物分類", food_categories_options, key="food_category_select")

    # 根據分類篩選食物選項
    filtered_food_options = []
    if selected_category == "所有分類":
        filtered_food_options = sorted(list(st.session_state.food_database.keys()))
    else:
        filtered_food_options = sorted([name for name, data in st.session_state.food_database.items() if data["category"] == selected_category])

    # 選擇要新增的食物和餐別
    col_food_select, col_meal_type = st.columns([0.7, 0.3])
    with col_food_select:
        food_to_add_name = st.selectbox("選擇要新增的食物", [""] + filtered_food_options, key="food_to_add_selectbox")
    with col_meal_type:
        meal_type_selection = st.selectbox("新增到", ["", "早餐", "午餐", "晚餐"], key="meal_type_select")

    if st.button("將食物新增到餐點", key="add_food_to_meal_button"):
        if food_to_add_name and meal_type_selection:
            if meal_type_selection == "早餐":
                if food_to_add_name not in st.session_state.breakfast_food_list:
                    st.session_state.breakfast_food_list.append(food_to_add_name)
                    st.success(f"'{food_to_add_name}' 已新增到早餐！")
                else:
                    st.warning(f"'{food_to_add_name}' 已在早餐清單中。")
            elif meal_type_selection == "午餐":
                if food_to_add_name not in st.session_state.lunch_food_list:
                    st.session_state.lunch_food_list.append(food_to_add_name)
                    st.success(f"'{food_to_add_name}' 已新增到午餐！")
                else:
                    st.warning(f"'{food_to_add_name}' 已在午餐清單中。")
            elif meal_type_selection == "晚餐":
                if food_to_add_name not in st.session_state.dinner_food_list:
                    st.session_state.dinner_food_list.append(food_to_add_name)
                    st.success(f"'{food_to_add_name}' 已新增到晚餐！")
                else:
                    st.warning(f"'{food_to_add_name}' 已在晚餐清單中。")
            
            # 設定頁面索引，導向新增紀錄頁面 (索引為 1)
            st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
            st.rerun() # 強制重運行以更新顯示並停留在新增紀錄 Tab
        else:
            st.warning("請選擇要新增的食物和餐別。")
    
    st.markdown("---")

    # 顯示各餐的食物清單 (包含移除單項食物功能)
    col_meals_display1, col_meals_display2, col_meals_display3 = st.columns(3)
    
    with col_meals_display1:
        st.subheader("早餐清單 🍞")
        if st.session_state.breakfast_food_list:
            # Display foods as chips
            food_chips_html = ''.join([
                f'<span class="food-chip">{food} ({st.session_state.food_database.get(food, {}).get("calories", "N/A")} 大卡)</span>'
                for food in st.session_state.breakfast_food_list
            ])
            st.markdown(f"<div class='food-chips-container'>{food_chips_html}</div>", unsafe_allow_html=True)

            # Option to remove individual food
            food_to_remove_breakfast = st.selectbox(
                "選擇要移除的早餐食物",
                [""] + st.session_state.breakfast_food_list,
                key="remove_foods_breakfast_selectbox"
            )
            if st.button("移除選定早餐食物", key="remove_selected_breakfast_button"):
                if food_to_remove_breakfast and food_to_remove_breakfast in st.session_state.breakfast_food_list:
                    st.session_state.breakfast_food_list.remove(food_to_remove_breakfast)
                    st.success(f"'{food_to_remove_breakfast}' 已從早餐移除。")
                    st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                    st.rerun()
                else:
                    st.warning("請選擇要移除的早餐食物。")
            
            # Clear all button
            if st.button("清空早餐", key="clear_breakfast_button", help="點擊此按鈕將清空所有早餐紀錄"):
                st.session_state.breakfast_food_list = []
                st.success("早餐清單已清空。")
                st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                st.rerun()
        else:
            st.info("早餐尚未新增食物。")

    with col_meals_display2:
        st.subheader("午餐清單 🍝")
        if st.session_state.lunch_food_list:
            # Display foods as chips
            food_chips_html = ''.join([
                f'<span class="food-chip">{food} ({st.session_state.food_database.get(food, {}).get("calories", "N/A")} 大卡)</span>'
                for food in st.session_state.lunch_food_list
            ])
            st.markdown(f"<div class='food-chips-container'>{food_chips_html}</div>", unsafe_allow_html=True)

            food_to_remove_lunch = st.selectbox(
                "選擇要移除的午餐食物",
                [""] + st.session_state.lunch_food_list,
                key="remove_foods_lunch_selectbox"
            )
            if st.button("移除選定午餐食物", key="remove_selected_lunch_button"):
                if food_to_remove_lunch and food_to_remove_lunch in st.session_state.lunch_food_list:
                    st.session_state.lunch_food_list.remove(food_to_remove_lunch)
                    st.success(f"'{food_to_remove_lunch}' 已從午餐移除。")
                    st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                    st.rerun()
                else:
                    st.warning("請選擇要移除的午餐食物。")
            if st.button("清空午餐", key="clear_lunch_button", help="點擊此按鈕將清空所有午餐紀錄"):
                st.session_state.lunch_food_list = []
                st.success("午餐清單已清空。")
                st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                st.rerun()
        else:
            st.info("午餐尚未新增食物。")

    with col_meals_display3:
        st.subheader("晚餐清單 🍜")
        if st.session_state.dinner_food_list:
            # Display foods as chips
            food_chips_html = ''.join([
                f'<span class="food-chip">{food} ({st.session_state.food_database.get(food, {}).get("calories", "N/A")} 大卡)</span>'
                for food in st.session_state.dinner_food_list
            ])
            st.markdown(f"<div class='food-chips-container'>{food_chips_html}</div>", unsafe_allow_html=True)

            food_to_remove_dinner = st.selectbox(
                "選擇要移除的晚餐食物",
                [""] + st.session_state.dinner_food_list,
                key="remove_foods_dinner_selectbox"
            )
            if st.button("移除選定晚餐食物", key="remove_selected_dinner_button"):
                if food_to_remove_dinner and food_to_remove_dinner in st.session_state.dinner_food_list:
                    st.session_state.dinner_food_list.remove(food_to_remove_dinner)
                    st.success(f"'{food_to_remove_dinner}' 已從晚餐移除。")
                    st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                    st.rerun()
                else:
                    st.warning("請選擇要移除的晚餐食物。")
            if st.button("清空晚餐", key="clear_dinner_button", help="點擊此按鈕將清空所有晚餐紀錄"):
                st.session_state.dinner_food_list = []
                st.success("晚餐清單已清空。")
                st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
                st.rerun()
        else:
            st.info("晚餐尚未新增食物。")

    # 根據 session state 中的食物列表重新計算總熱量
    breakfast_cal, _ = calculate_meal_calories(st.session_state.breakfast_food_list, st.session_state.food_database)
    lunch_cal, _ = calculate_meal_calories(st.session_state.lunch_food_list, st.session_state.food_database)
    dinner_cal, _ = calculate_meal_calories(st.session_state.dinner_food_list, st.session_state.food_database)

    total_daily_intake_calories = breakfast_cal + lunch_cal + dinner_cal
    st.metric("今日總攝取熱量", f"{total_daily_intake_calories} 大卡", help="所有餐點的熱量總和")


    st.markdown("---")

    # --- 運動紀錄與建議 ---
    st.subheader("🏃‍♂️ 運動紀錄與建議")
    st.write("今天您挑戰了哪些運動呢？記錄下來，感受燃燒脂肪的快感！")
    selected_exercises = st.multiselect("選擇運動類型", list(st.session_state.exercise_calories_per_min.keys()), help="可以選擇多種運動喔！")
    exercise_calories_burned = 0
    exercise_details = {}

    for exercise in selected_exercises:
        minutes = st.number_input(f"{exercise} 時間 (分鐘)", min_value=0, value=0, key=f"ex_{exercise}", help=f"每分鐘約消耗 {st.session_state.exercise_calories_per_min[exercise]} 大卡")
        if minutes > 0:
            burned = minutes * st.session_state.exercise_calories_per_min[exercise]
            exercise_calories_burned += burned
            exercise_details[exercise] = minutes

    st.metric("今日運動消耗熱量", f"{exercise_calories_burned} 大卡", help="您今日運動所消耗的總熱量")
    
    st.markdown("---")

    # --- BMI 與體脂分析 ---
    st.subheader("📏 BMI 與體脂分析")
    st.write("輸入您的身體數據，將為您計算 BMI 和體脂肪率，並給出貼心建議！")
    col_bmi1, col_bmi2, col_bmi3 = st.columns(3)
    with col_bmi1:
        height = st.number_input("身高 (公分)", min_value=50.0, max_value=250.0, value=170.0, step=0.1, key="add_record_height", help="請輸入您的身高，單位為公分")
    with col_bmi2:
        weight = st.number_input("體重 (公斤)", min_value=10.0, max_value=200.0, value=65.0, step=0.1, key="add_record_weight", help="請輸入您的體重，單位為公斤")
    with col_bmi3:
        gender = st.selectbox("性別", ["男性", "女性"], key="add_record_gender", help="選擇您的性別以獲得更精確的體脂率計算")

    bmi = 0.0
    body_fat_rate = 0.0
    bmi_advice = ""

    if height > 0 and weight > 0:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"您的 BMI: **{bmi:.2f}**")

        # 修正後的體脂肪率計算公式
        if gender == "男性":
            body_fat_rate = (1.20 * bmi) + (0.23 * st.session_state.get('age', 25)) - 16.2
        else: # 女性
            body_fat_rate = (1.20 * bmi) + (0.23 * st.session_state.get('age', 25)) - 5.4
        
        # 體脂率不能為負數
        if body_fat_rate < 0:
            body_fat_rate = 0.0
        
        st.write(f"您的體脂肪率: **{body_fat_rate:.2f}%**")

        if bmi < 18.5:
            bmi_advice = "體重過輕，要多吃一點營養健康的食物，讓身體更強壯喔！"
        elif 18.5 <= bmi < 24:
            bmi_advice = "恭喜！您的體重非常標準，繼續保持健康的生活習慣！🥳"
        elif 24 <= bmi < 27:
            bmi_advice = "體重略微過重，透過飲食調整和適度運動，很快就能恢復理想狀態！💪"
        elif 27 <= bmi < 30:
            bmi_advice = "輕度肥胖，是時候開始為健康努力了，尋求專業建議會很有幫助喔！"
        elif 30 <= bmi < 35:
            bmi_advice = "中度肥胖，為了您的健康，建議積極減重並尋求醫療協助。健康日記會支持您！"
        else:
            bmi_advice = "重度肥胖，請務必立即尋求專業醫療協助，健康是第一位的！"
        st.info(f"健康建議: {bmi_advice}")
    
    st.markdown("---")

    # --- 天氣資訊 ---
    st.subheader("🌦 天氣資訊與運動建議")
    st.write("即時查看您所在城市的天氣，將為您推薦最適合的運動方式！")
    taiwan_cities = {
        "台北市": "Taipei", "新北市": "New Taipei", "桃園市": "Taoyuan",
        "台中市": "Taichung", "台南市": "Tainan", "高雄市": "Kaohsiung",
        "基隆市": "Keelung", "新竹市": "Hsinchu", "嘉義市": "Chiayi",
        "新竹縣": "Hsinchu County", "苗栗縣": "Miaoli County", "彰化縣": "Changhua County",
        "南投縣": "Nantou County", "雲林縣": "Yunlin County", "嘉義縣": "Chiayi County",
        "屏東縣": "Pingtung County", "宜蘭縣": "Yilan County", "花蓮縣": "Hualien",
        "台東縣": "Taitung County", "澎湖縣": "Penghu", "金門縣": "Kinmen", "連江縣": "Lienchiang"
    }
    selected_city_chinese = st.selectbox("選擇城市", list(taiwan_cities.keys()), index=list(taiwan_cities.keys()).index("花蓮縣"), key="weather_city_select", help="選擇您想查詢天氣的台灣城市")
    selected_city_english = taiwan_cities[selected_city_chinese]

    # --- 重要提示：請替換您的 OpenWeatherMap API Key ---
    # 您可以在這裡替換您的 OpenWeatherMap API Key。
    # 如果您沒有，請前往 https://openweathermap.org/api 註冊獲取。
    # 無效或缺失的 API Key 將導致天氣資訊無法獲取。
    weather_api_key = "038c4da459d3a855825837e76ebf49ff"  # <--- 請在這裡替換為您的有效 API Key，用雙引號包起來

    def get_weather(city, api_key):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric&lang=zh_tw"
        try:
            response = requests.get(complete_url)
            response.raise_for_status() # 檢查 HTTP 請求是否成功 (200 OK)
            data = response.json()
            if data["cod"] == 200:
                weather_desc = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return weather_desc, temp
            else:
                st.error(f"無法取得天氣資訊: {data.get('message', '未知錯誤')}。請檢查 API Key 或城市名稱。")
                return "N/A", "N/A"
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP 錯誤發生: {http_err} (狀態碼: {response.status_code})。請檢查您的 OpenWeatherMap API Key 是否有效。")
            return "N/A", "N/A"
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"網路連線錯誤: {conn_err}。請檢查您的網路連線。")
            return "N/A", "N/A"
        except requests.exceptions.Timeout as timeout_err:
            st.error(f"請求超時: {timeout_err}。請重試或檢查網路連線。")
            return "N/A", "N/A"
        except requests.exceptions.RequestException as req_err:
            st.error(f"呼叫天氣 API 時發生錯誤: {req_err}。")
            return "N/A", "N/A"
        except json.JSONDecodeError:
            st.error("天氣 API 回傳的資料格式不正確，無法解析。")
            return "N/A", "N/A"
        except Exception as e:
            st.error(f"取得天氣資訊時發生未知錯誤: {e}。")
            return "N/A", "N/A"

    weather_desc, temperature = get_weather(selected_city_english, weather_api_key)
    st.info(f"目前 {selected_city_chinese} 的天氣：{weather_desc}，氣溫：{temperature}°C")
    st.markdown(f"**天氣運動建議：** {get_weather_exercise_suggestion(weather_desc, temperature)}")


    st.markdown("---")

    # --- 總結與紀錄按鈕 ---
    st.subheader("📝 紀錄總結")
    st.write("確認所有數據無誤後，點擊下方按鈕，將今日的健康努力永久保存！")

    net_calories = total_daily_intake_calories - exercise_calories_burned
    st.metric("今日淨熱量", f"{net_calories} 大卡", help="總攝取熱量減去運動消耗熱量")

    health_suggestion = ""
    if net_calories > 500:
        health_suggestion = "今日熱量攝取可能偏多，建議明天多加運動或調整飲食，保持平衡喔！"
    elif net_calories < -500:
        health_suggestion = "今日熱量消耗較多，記得補充適量營養，讓身體有足夠能量！"
    else:
        health_suggestion = "恭喜您！今日熱量攝取與消耗達到良好平衡，繼續保持這個好習慣！✨"
    st.success(f"今日健康建議: {health_suggestion}")
    record_date = st.date_input("選擇紀錄日期", datetime.date.today(), key="add_record_final_date", help="選擇您想記錄的日期")

    if st.button("儲存紀錄", key="save_record_button"): # 確保此按鈕有唯一的key
        df_history = st.session_state.df_history # 使用 session state 中的 df_history

        # 將日期從 datetime.date 轉換為 datetime.datetime 以便進行比較和儲存
        record_datetime = datetime.datetime.combine(record_date, datetime.time.min)

        # 檢查是否已存在同日期的紀錄
        existing_record_indices = df_history[df_history['日期'] == record_date].index
        
        breakfast_food_str = ", ".join(st.session_state.breakfast_food_list) if st.session_state.breakfast_food_list else "無"
        lunch_food_str = ", ".join(st.session_state.lunch_food_list) if st.session_state.lunch_food_list else "無"
        dinner_food_str = ", ".join(st.session_state.dinner_food_list) if st.session_state.dinner_food_list else "無"
        
        meal_content_str = f"早餐: ({breakfast_food_str}), 午餐: ({lunch_food_str}), 晚餐: ({dinner_food_str})"

        new_record_data = {
            '日期': record_date, # 直接使用 datetime.date 物件
            '體重(kg)': weight,
            '目標體重(kg)': st.session_state.get('target_weight', 0.0), # 從 Session State 獲取目標體重
            '身高(公分)': height,
            '性別': gender,
            'BMI': round(bmi, 2),
            '體脂肪率': round(body_fat_rate, 2),
            '總攝取熱量': total_daily_intake_calories,
            '運動類型': ", ".join(exercise_details.keys()) if exercise_details else "無",
            '運動時間(分鐘)': sum(exercise_details.values()) if exercise_details else 0,
            '運動消耗熱量': exercise_calories_burned,
            '天氣城市': selected_city_chinese,
            '天氣說明': weather_desc,
            '氣溫': temperature,
            '健康建議': health_suggestion,
            '總淨熱量': net_calories,
            '餐點內容': meal_content_str
        }

        # 將新紀錄轉換為 DataFrame，並確保其列順序與現有 DataFrame 一致
        # 定義所有預期的列名，這與 load_data 中的 columns 應保持一致
        expected_columns = [
            '日期', '體重(kg)', '目標體重(kg)', '身高(公分)', '性別',
            'BMI', '體脂肪率', '總攝取熱量', '運動類型', '運動時間(分鐘)',
            '運動消耗熱量', '天氣城市', '天氣說明', '氣溫', '健康建議', '總淨熱量',
            '餐點內容'
        ]
        new_record_df = pd.DataFrame([new_record_data], columns=expected_columns)


        if not existing_record_indices.empty:
            # 更新現有紀錄
            idx_to_update = existing_record_indices[0]
            for col, value in new_record_data.items():
                st.session_state.df_history.at[idx_to_update, col] = value
            st.success(f"已成功更新 {record_date} 的健康紀錄！太棒了！👏")
        else:
            # 新增紀錄 (使用 pd.concat 確保列一致性)
            st.session_state.df_history = pd.concat([df_history, new_record_df], ignore_index=True)
            st.success("健康紀錄已成功儲存！🎉 每一天的堅持，都是通往健康的里程碑！")
        
        save_data(st.session_state.df_history) # 儲存到 CSV 文件
        st.session_state.save_counter += 1 # 儲存成功後增加計數器
        st.balloons()
        # 清空 session state 中的食物列表，準備下次輸入
        st.session_state.breakfast_food_list = []
        st.session_state.lunch_food_list = []
        st.session_state.dinner_food_list = []
        
        # 設定頁面索引，導向新增紀錄頁面 (索引為 1)
        st.session_state.current_page_index = page_names.index("✍️ 新增紀錄")
        st.rerun() # 強制重運行以更新顯示並停留在新增紀錄 Tab

    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)

def data_analysis_page(df_history):
    # Removed specific anchor here, using global 'app_top'

    st.header("📊 熱量圖表分析")
    st.write("透過視覺化的數據圖表，輕鬆洞悉您的健康模式與趨勢！")
    st.write("---")

    if not df_history.empty:
        # 確保 df_history['日期'] 是 datetime 對象
        df_history['日期'] = pd.to_datetime(df_history['日期']).dt.date
        df_history_sorted = df_history.sort_values(by='日期', ascending=True)

        st.subheader("每日熱量圓餅圖 (最近紀錄)")
        st.write("這張圓餅圖將呈現您最近一次紀錄的熱量攝取與消耗比例，幫助您了解當日能量平衡。")
        if not df_history_sorted.empty:
            latest_record = df_history_sorted.iloc[-1]
            intake = latest_record['總攝取熱量'] if pd.notna(latest_record['總攝取熱量']) else 0
            burned = latest_record['運動消耗熱量'] if pd.notna(latest_record['運動消耗熱量']) else 0

            if intake == 0 and burned == 0:
                st.info("最近紀錄的攝取與消耗熱量皆為零，無法繪製圓餅圖。請先前往新增紀錄頁面填寫資料喔！")
            else:
                fig_pie = go.Figure(data=[go.Pie(labels=['攝取熱量', '消耗熱量'],
                                                values=[intake, burned],
                                                hole=.3,
                                                marker_colors=[CUTE_COLORS[0], CUTE_COLORS[3]])]) # 使用可愛顏色
                # 確保日期物件正確格式化
                latest_record_date_str = latest_record['日期'].strftime('%Y-%m-%d')
                fig_pie.update_layout(title_text=f"{latest_record_date_str} 熱量分佈")
                # 使用基於最新紀錄日期的動態 key，並加入儲存計數器確保唯一性
                st.plotly_chart(fig_pie, key=f"data_analysis_pie_chart_{latest_record_date_str}_{st.session_state.get('save_counter', 0)}")
        else:
            st.info("暫無足夠數據顯示每日熱量圓餅圖。")

        st.markdown("---")
        st.subheader("每週熱量趨勢圖")
        st.write("透過每週的熱量趨勢圖，您可以觀察長期的能量攝取與消耗變化，是您制定健康計畫的好幫手！")
        # 為了週趨勢圖，將日期索引設定為 datetime.datetime
        df_weekly = df_history_sorted.set_index(pd.to_datetime(df_history_sorted['日期'])).resample('W').agg(
            {'總攝取熱量': 'sum', '運動消耗熱量': 'sum', '總淨熱量': 'sum'}
        ).reset_index()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df_weekly['日期'], y=df_weekly['總攝取熱量'], mode='lines+markers', name='攝取熱量',
                                       line=dict(color=CUTE_COLORS[0], width=3), marker=dict(size=8, symbol='circle')))
        fig_trend.add_trace(go.Scatter(x=df_weekly['日期'], y=df_weekly['運動消耗熱量'], mode='lines+markers', name='消耗熱量',
                                       line=dict(color=CUTE_COLORS[3], width=3), marker=dict(size=8, symbol='square')))
        fig_trend.add_trace(go.Scatter(x=df_weekly['日期'], y=df_weekly['總淨熱量'], mode='lines+markers', name='淨熱量',
                                       line=dict(color=CUTE_COLORS[8], width=3), marker=dict(size=8, symbol='diamond')))
        fig_trend.update_layout(
            title='每週熱量趨勢', xaxis_title='日期', yaxis_title='熱量 (大卡)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, key="data_analysis_trend_chart") # 添加 key

        # --- 熱量攝取與消耗比較圖 & 運動量分佈圖 (並排顯示) ---
        st.markdown("---")
        st.subheader("📊 每日數據細覽")
        st.write("這些圖表將幫助您更深入地了解每日的熱量平衡和運動習慣。")
        
        col_chart1, col_chart2 = st.columns(2) # 創建兩個並排的欄位

        with col_chart1:
            st.write("🔥 **每日熱量攝取與消耗比較**")
            st.write("這張圖表讓您一目瞭然每日攝取與消耗的熱量，幫助您更好地平衡能量。")
            # 合併每天的攝取與消耗，確保日期正確為 datetime 物件
            daily_calories = df_history_sorted.copy()
            daily_calories['日期'] = pd.to_datetime(daily_calories['日期']) # 再次確保是 datetime
            daily_calories = daily_calories.groupby(pd.Grouper(key='日期', freq='D')).agg(
                {'總攝取熱量': 'sum', '運動消耗熱量': 'sum'} # 使用新列名
            ).reset_index()

            # 再次確保繪圖前的數值列類型正確
            daily_calories['總攝取熱量'] = pd.to_numeric(daily_calories['總攝取熱量'], errors='coerce').fillna(0)
            daily_calories['運動消耗熱量'] = pd.to_numeric(daily_calories['運動消耗熱量'], errors='coerce').fillna(0)


            fig_calories = px.bar(daily_calories, x='日期', y=['總攝取熱量', '運動消耗熱量'], # 使用新列名
                                   color_discrete_sequence=[CUTE_COLORS[0], CUTE_COLORS[3]], # 粉色和淺藍
                                   labels={'value': '熱量(大卡)', 'variable': '類型'},
                                   title='每日熱量攝取與消耗',
                                   barmode='group') # 並排顯示

            fig_calories.update_traces(marker_line_width=1, marker_line_color='white', # 白色描邊
                                       marker_pattern_shape='.', # 小點填充
                                       marker_color=None) # 讓 color_discrete_sequence 控制顏色
            fig_calories.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="日期",
                yaxis_title="熱量 (大卡)",
                legend_title_text="",
                uniformtext_minsize=10, uniformtext_mode='hide',
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial Rounded MT Bold"),
                height=350 # 調整圖表高度以適應並排顯示
            )
            st.plotly_chart(fig_calories, use_container_width=True, key="data_analysis_calories_chart") # 新增 key

        with col_chart2:
            st.write("🤸‍♀️ **運動項目分佈**")
            st.write("想知道自己最常從事哪些運動嗎？這張圖會告訴您！")
            # 提取所有運動數據並計數
            all_exercises_names = []
            for index, row in df_history_sorted.iterrows():
                if pd.notna(row['運動類型']) and row['運動類型'] != '':
                    exercises = [e.strip() for e in row['運動類型'].split(',')] # 假設運動類型是逗號分隔
                    all_exercises_names.extend([e.split('(')[0].strip() for e in exercises])

            if all_exercises_names:
                exercise_counts = pd.Series(all_exercises_names).value_counts().reset_index()
                exercise_counts.columns = ['運動項目', '次數']

                fig_exercise_dist = px.pie(exercise_counts, values='次數', names='運動項目',
                                            title='運動項目分佈',
                                            color_discrete_sequence=CUTE_COLORS, # 使用可愛顏色
                                            hole=0.5) # 甜甜圈效果

                fig_exercise_dist.update_traces(textinfo='percent+label',
                                                marker=dict(line=dict(color='#ffffff', width=2)), # 白色描邊
                                                pull=[0.05] * len(exercise_counts), # 輕微分離效果
                                                textfont_size=14,
                                                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial Rounded MT Bold"))
                fig_exercise_dist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    uniformtext_minsize=10, uniformtext_mode='hide',
                    showlegend=False, # 甜甜圈圖通常在片上顯示標籤，可以隱藏圖例
                    height=350 # 調整圖表高度以適應並排顯示
                )
                st.plotly_chart(fig_exercise_dist, use_container_width=True, key="data_analysis_exercise_dist_chart") # 新增 key
            else:
                st.info("暫無運動數據可供分析，快去新增一些運動紀錄吧！")

    else:
        st.info("暫無紀錄數據，請先儲存紀錄以查看圖表。期待看到您的健康數據成長！")

    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)

def history_page(df_history):
    # Removed specific anchor here, using global 'app_top'

    st.header("🗂 歷史紀錄")
    st.write("所有走過的健康足跡，都在這裡留下印記。您可以隨時回顧與管理！")
    st.write("---")

    # Initialize session state for editing and deletion if not already present
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'current_edit_record_original_idx' not in st.session_state:
        st.session_state.current_edit_record_original_idx = None
    if 'confirm_delete_original_idx' not in st.session_state:
        st.session_state.confirm_delete_original_idx = None

    if not df_history.empty:
        df_history['日期'] = pd.to_datetime(df_history['日期']).dt.date
        df_history_display = df_history.sort_values(by='日期', ascending=False).reset_index()

        st.subheader("所有紀錄 (選擇日期查看)")
        st.write("請從下方選單中選擇特定日期，即可查看該日的詳細紀錄並進行編輯或刪除。")

        # 優化歷史紀錄顯示：使用 selectbox 選擇日期，然後展開顯示該日期紀錄
        # 將日期格式化為更易讀的字串，包含星期幾
        # 例如: 2023-10-26 (週四)
        formatted_unique_dates = [""] + [
            f"{d.strftime('%Y-%m-%d')} ({d.strftime('%a')})" for d in sorted(df_history_display['日期'].unique().tolist(), reverse=True)
        ]
        selected_formatted_date_to_view = st.selectbox(
            "選擇要查看的日期紀錄",
            formatted_unique_dates,
            key="history_date_selector",
            help="選擇一個日期來展開該日的健康紀錄詳情"
        )

        selected_date_obj = None
        if selected_formatted_date_to_view != "":
            # 從格式化的字串中提取日期部分，轉換回 datetime.date 物件
            date_str_only = selected_formatted_date_to_view.split(' ')[0]
            selected_date_obj = datetime.datetime.strptime(date_str_only, '%Y-%m-%d').date()

            # 過濾出選擇日期的紀錄，並找到其原始索引
            selected_records_df = df_history_display[df_history_display['日期'] == selected_date_obj]
            
            if not selected_records_df.empty:
                # 假設每天只有一筆紀錄，取第一筆進行顯示和編輯
                row = selected_records_df.iloc[0]
                record_date_str = row['日期'].strftime('%Y-%m-%d')
                original_idx = row['index']

                with st.expander(f"🗓️ **{record_date_str}** - 體重: {row['體重(kg)']:.1f} kg, 淨熱量: {row['總淨熱量']:.0f} 大卡", expanded=True):
                    st.markdown("---")
                    st.write(f"- **目標體重(kg)**: {row['目標體重(kg)']:.1f}")
                    st.write(f"- **身高(公分)**: {row['身高(公分)']:.1f}")
                    st.write(f"- **性別**: {row['性別']}")
                    st.write(f"- **BMI**: {row['BMI']:.2f}")
                    st.write(f"- **體脂肪率**: {row['體脂肪率']:.1f}%")
                    st.write(f"- **總攝取熱量**: {row['總攝取熱量']:.0f} 大卡")
                    st.write(f"- **運動類型**: {row['運動類型']}")
                    st.write(f"- **運動時間(分鐘)**: {row['運動時間(分鐘)']:.0f} 分鐘")
                    st.write(f"- **運動消耗熱量**: {row['運動消耗熱量']:.0f} 大卡")
                    st.write(f"- **天氣城市**: {row['天氣城市']}")
                    st.write(f"- **天氣說明**: {row['天氣說明']}")
                    st.write(f"- **氣溫**: {row['氣溫']:.1f}°C")
                    st.write(f"- **健康建議**: {row['健康建議']}")
                    st.write(f"- **餐點內容**: {row['餐點內容']}")
                    
                    col_edit_del = st.columns(2)
                    with col_edit_del[0]:
                        if st.button("編輯此紀錄", key=f"edit_btn_{original_idx}"):
                            st.session_state.current_edit_record_original_idx = original_idx
                            st.session_state.edit_mode = True
                            st.session_state.confirm_delete_original_idx = None
                            st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                            st.rerun()

                    with col_edit_del[1]:
                        if st.button("刪除此紀錄", key=f"delete_btn_{original_idx}"):
                            if st.session_state.get('confirm_delete_original_idx') == original_idx:
                                st.session_state.df_history = st.session_state.df_history.drop(original_idx).reset_index(drop=True)
                                save_data(st.session_state.df_history)
                                st.success(f"已成功刪除 {record_date_str} 的紀錄。")
                                st.session_state.edit_mode = False
                                st.session_state.current_edit_record_original_idx = None
                                st.session_state.confirm_delete_original_idx = None
                                st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                                st.rerun()
                            else:
                                st.session_state.confirm_delete_original_idx = original_idx
                                st.session_state.edit_mode = False
                                st.warning(f"確定要刪除 {record_date_str} 的紀錄嗎？請再點擊「刪除此紀錄」確認。")
                                st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                                st.rerun()

                    if st.session_state.get('confirm_delete_original_idx') == original_idx:
                        st.info(f"**請注意：** 您已點擊刪除 {record_date_str}。再次點擊「刪除此紀錄」將永久移除它。")
            else:
                st.info("在選定日期沒有找到紀錄。")

        # Edit form (remains the same, but only appears if a record is selected for edit)
        if st.session_state.edit_mode and st.session_state.current_edit_record_original_idx is not None:
            original_idx_to_edit = st.session_state.current_edit_record_original_idx
            
            if original_idx_to_edit in st.session_state.df_history.index:
                current_record = st.session_state.df_history.loc[original_idx_to_edit].copy()

                st.subheader(f"✏️ 編輯 {current_record['日期'].strftime('%Y-%m-%d')} 的紀錄")
                st.write("請修改以下資訊，然後點擊「更新紀錄」儲存更改。")

                with st.form(key=f"edit_record_form_{original_idx_to_edit}"):
                    edited_date = st.date_input("紀錄日期", value=current_record['日期'] if pd.notna(current_record['日期']) else datetime.date.today(), key=f"edit_date_{original_idx_to_edit}")
                    edited_weight = st.number_input("體重 (公斤)", value=float(current_record.get('體重(kg)', 0.0)), format="%.1f", key=f"edit_weight_{original_idx_to_edit}")
                    edited_target_weight = st.number_input("目標體重 (公斤)", value=float(current_record.get('目標體重(kg)', 0.0)), format="%.1f", key=f"edit_target_weight_{original_idx_to_edit}")
                    edited_height = st.number_input("身高 (公分)", min_value=50.0, max_value=250.0, value=float(current_record.get('身高(公分)', 0.0)), format="%.1f", key=f"edit_height_{original_idx_to_edit}")
                    
                    current_gender_val = current_record.get('性別', '男性')
                    gender_options = ["男性", "女性"]
                    edited_gender = st.selectbox("性別", gender_options, index=gender_options.index(current_gender_val) if current_gender_val in gender_options else 0, key=f"edit_gender_{original_idx_to_edit}")
                    
                    edited_total_intake = st.number_input("總攝取熱量 (大卡)", value=int(current_record.get('總攝取熱量', 0)), key=f"edit_total_intake_{original_idx_to_edit}")
                    
                    current_exercise_type = current_record.get('運動類型', "")
                    edited_exercise_type = st.text_input("運動類型 (逗號分隔)", value=current_exercise_type, key=f"edit_ex_type_{original_idx_to_edit}")
                    edited_exercise_time = st.number_input("運動時間 (分鐘)", value=int(current_record.get('運動時間(分鐘)', 0)), key=f"edit_ex_time_{original_idx_to_edit}")
                    
                    edited_meal_content = st.text_area("餐點內容", value=current_record.get('餐點內容', ""), key=f"edit_meal_content_{original_idx_to_edit}")
                    edited_weather_city = st.text_input("天氣城市", value=current_record.get('天氣城市', ""), key=f"edit_weather_city_{original_idx_to_edit}")
                    edited_weather_desc = st.text_input("天氣說明", value=current_record.get('天氣說明', ""), key=f"edit_weather_desc_{original_idx_to_edit}")
                    edited_temperature = st.number_input("氣溫 (°C)", value=float(current_record.get('氣溫', 0.0)), format="%.1f", key=f"edit_temperature_{original_idx_to_edit}")
                    edited_health_suggestion = st.text_area("健康建議", value=current_record.get('健康建議', ""), key=f"edit_health_suggestion_{original_idx_to_edit}")

                    recalculated_bmi = calculate_bmi(edited_weight, edited_height)
                    recalculated_body_fat_rate = 0.0
                    if edited_height > 0 and edited_weight > 0:
                        age_for_calc = st.session_state.get('age', 25)
                        if edited_gender == "男性":
                            recalculated_body_fat_rate = (1.20 * recalculated_bmi) + (0.23 * age_for_calc) - 16.2
                        else:
                            recalculated_body_fat_rate = (1.20 * recalculated_bmi) + (0.23 * age_for_calc) - 5.4
                        if recalculated_body_fat_rate < 0:
                            recalculated_body_fat_rate = 0.0
                    
                    # 重新計算運動消耗熱量，這裡可以簡單假設一個平均消耗率，或根據運動類型詳細計算
                    # 為了簡化編輯，我們假設一個平均值。如果需要精確，需要複雜的運動類型解析。
                    recalculated_exercise_burned = edited_exercise_time * 7 # 假設平均每分鐘消耗 7 大卡
                    recalculated_net_calories = edited_total_intake - recalculated_exercise_burned

                    col_update_cancel = st.columns(2)
                    with col_update_cancel[0]:
                        update_button_clicked = st.form_submit_button("更新紀錄", help="儲存修改後的紀錄")
                    with col_update_cancel[1]:
                        cancel_button_clicked = st.form_submit_button("取消編輯", help="放棄修改並關閉表單")
                    
                    if update_button_clicked:
                        st.session_state.df_history.loc[original_idx_to_edit] = {
                            '日期': edited_date,
                            '體重(kg)': edited_weight,
                            '目標體重(kg)': edited_target_weight,
                            '身高(公分)': edited_height,
                            '性別': edited_gender,
                            'BMI': round(recalculated_bmi, 2),
                            '體脂肪率': round(recalculated_body_fat_rate, 2),
                            '總攝取熱量': edited_total_intake,
                            '運動類型': edited_exercise_type,
                            '運動時間(分鐘)': edited_exercise_time,
                            '運動消耗熱量': recalculated_exercise_burned,
                            '天氣城市': edited_weather_city,
                            '天氣說明': edited_weather_desc,
                            '氣溫': edited_temperature,
                            '健康建議': edited_health_suggestion,
                            '總淨熱量': recalculated_net_calories,
                            '餐點內容': edited_meal_content
                        }
                        save_data(st.session_state.df_history)
                        st.success(f"已成功更新 {edited_date.strftime('%Y-%m-%d')} 的紀錄。")
                        st.session_state.edit_mode = False
                        st.session_state.current_edit_record_original_idx = None
                        st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                        st.rerun()
                    
                    if cancel_button_clicked:
                        st.info("已取消編輯。")
                        st.session_state.edit_mode = False
                        st.session_state.current_edit_record_original_idx = None
                        st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                        st.rerun()
            else:
                st.warning("要編輯的紀錄不存在或已被刪除。請重新選擇。")
                st.session_state.edit_mode = False
                st.session_state.current_edit_record_original_idx = None
                st.session_state.current_page_index = page_names.index("🗂 歷史紀錄") # 保持在歷史紀錄頁面
                st.rerun()
        else:
            if selected_formatted_date_to_view == "": # Only show this message if no specific date is selected
                st.info("請從上方選單選擇一個日期，即可查看該日的詳細紀錄並進行編輯。")
            
        if (st.session_state.get('confirm_delete_original_idx') is not None and
            (not st.session_state.edit_mode or
             st.session_state.get('current_edit_record_original_idx') != st.session_state.get('confirm_delete_original_idx'))):
            pass

    else:
        st.info("暫無紀錄可供管理。")

    st.markdown("---")
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df_to_csv(df_history)
    st.download_button(
        label="匯出所有紀錄為 CSV",
        data=csv,
        file_name='健康日記_歷史紀錄.csv',
        mime='text/csv',
        key="export_csv_button",
        help="點擊此按鈕，將您的所有健康紀錄匯出為 CSV 檔案，方便您備份或進一步分析。"
    )
    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)


def settings_page():
    # Removed specific anchor here, using global 'app_top'

    st.header("⚙️ 設定與管理")
    st.write("在這裡，您可以個人化應用程式設定，以及管理食物和運動的資料庫。")
    st.write("---")

    # 確保 session_state 中有 age 和 activity_level 的預設值
    if 'age' not in st.session_state:
        st.session_state.age = 25
    if 'activity_level' not in st.session_state:
        st.session_state.activity_level = "久坐 (很少運動)"
    if 'gender' not in st.session_state:
        st.session_state.gender = "男性"
    if 'target_weight' not in st.session_state:
        st.session_state.target_weight = 0.0
    # Add a session state variable to store the personal health analysis message
    if 'personal_health_analysis_message' not in st.session_state:
        st.session_state.personal_health_analysis_message = ""
    # Add a session state variable to store the personal health analysis for persistence
    if 'saved_personal_analysis' not in st.session_state:
        st.session_state.saved_personal_analysis = {
            'timestamp': None,
            'message': ""
        }
    
    # --- 個人設定區塊使用 st.expander ---
    with st.expander("👤 個人設定", expanded=True): # 預設展開
        st.write("填寫您的基本資料，讓健康日記為您提供更精確的健康分析與建議。")
        with st.form("user_profile_settings"):
            st.session_state.age = st.number_input("年齡", min_value=1, max_value=120, value=st.session_state.age, step=1, key="settings_age_input", help="您的年齡，用於體脂肪率等計算")
            activity_levels = ["久坐 (很少運動)", "輕度運動 (每週1-3天)", "中度運動 (每週3-5天)", "高度運動 (每週6-7天)", "非常高度運動 (每天訓練)"]
            st.session_state.activity_level = st.selectbox("活動程度", activity_levels, index=activity_levels.index(st.session_state.activity_level), key="settings_activity_level_select", help="選擇您的日常活動量，影響每日熱量建議")
            st.session_state.gender = st.radio("性別", ["男性", "女性"], index=0 if st.session_state.gender == "男性" else 1, key="settings_gender_radio", help="您的性別，用於體脂肪率等計算")
            st.session_state.target_weight = st.number_input("目標體重 (kg)", min_value=0.0, format="%.1f", value=st.session_state.target_weight, key="settings_target_weight_input", help="設定您的理想體重，激勵自己達成目標！")
            
            if st.form_submit_button("儲存個人設定並分析"): # 更名按鈕
                # 只有當 df_history 不為空時，才嘗試獲取 last_record
                if not st.session_state.df_history.empty:
                    last_record = st.session_state.df_history.sort_values(by='日期', ascending=False).iloc[0]
                    current_weight = last_record['體重(kg)'] if pd.notna(last_record['體重(kg)']) else 65.0
                    current_height = last_record['身高(公分)'] if pd.notna(last_record['身高(公分)']) else 170.0
                else:
                    # 如果沒有紀錄，使用預設值
                    current_weight = 65.0
                    current_height = 170.0
                    st.warning("目前沒有歷史紀錄，體重和身高將使用預設值進行健康分析。")

                bmr_calc, tdee_calc = calculate_bmr_tdee(
                    st.session_state.gender,
                    current_weight,
                    current_height,
                    st.session_state.age,
                    st.session_state.activity_level
                )

                analysis_message_parts = []
                analysis_message_parts.append(f"太棒了！您已成功更新個人設定。基於最新的數據，為您揭示專屬的健康藍圖：")
                analysis_message_parts.append(f"- 您的**基礎代謝率 (BMR)** 估計約為：**{bmr_calc:.0f} 大卡**。這表示您在靜止狀態下維持生命所需的基本熱量，是您每日熱量規劃的基礎。")
                analysis_message_parts.append(f"- 您的**每日總能量消耗 (TDEE)** 估計約為：**{tdee_calc:.0f} 大卡**。這是您每天包含活動所消耗的總熱量，是實現體重目標的關鍵數值！")

                health_tips = []
                if st.session_state.target_weight > 0 and current_weight > st.session_state.target_weight:
                    health_tips.append(f"**朝目標邁進！** 您的目標體重是 {st.session_state.target_weight:.1f} kg，目前體重 {current_weight:.1f} kg。為了更輕鬆地達成目標，建議您可以嘗試每日創造約 250-500 大卡的熱量赤字，將每日熱量攝取控制在 **{max(0, tdee_calc - 500):.0f} - {tdee_calc - 250:.0f} 大卡** 之間。這需要持之以恆的飲食調整與適度運動，每次堅持都讓您離夢想更近！")
                elif st.session_state.target_weight > 0 and current_weight < st.session_state.target_weight:
                     health_tips.append(f"**健康增重計畫啟動！** 您的目標體重是 {st.session_state.target_weight:.1f} kg，目前體重 {current_weight:.1f} kg。若要健康增重，建議每日熱量攝取可比 TDEE 高出約 **250-500 大卡**，並搭配充足的蛋白質（如優質肉類、豆製品）與力量訓練，讓身體在增長的同時也能強健有力！")
                else:
                    health_tips.append(f"**維持理想，活力無限！** 恭喜您，您的體重管理表現出色！維持健康的關鍵在於均衡的熱量攝取與消耗。建議您持續在每日總能量消耗 (TDEE) 約 **{tdee_calc:.0f} 大卡** 的基礎上，享受多元營養的飲食，並保持規律的運動，讓身體充滿活力！")
                
                if st.session_state.activity_level == "久坐 (很少運動)":
                    health_tips.append("**動起來，更健康！** 您目前的活動程度屬於久坐型。別擔心，從小地方開始改變就能帶來大不同！嘗試每小時起身活動 5-10 分鐘，或每天增加 30 分鐘的快走，讓身體逐漸適應更多活動。每次的微小改變，都是向健康邁進的一大步！")
                elif st.session_state.activity_level == "非常高度運動 (每天訓練)":
                    health_tips.append("**超棒的運動家！** 您的活動量非常高，這令人讚嘆！請務必重視訓練後的恢復，包括充足的睡眠、均衡的營養（尤其是蛋白質和碳水化合物補充），以及適度的伸展和休息。傾聽身體的聲音，避免過度訓練，讓每次訓練都發揮最大效益！")
                
                final_analysis_message = "\n\n".join(analysis_message_parts)
                if health_tips:
                    final_analysis_message += "\n\n**✨ VIVI 貼心健康小建議 ✨**\n" + "\n".join([f"- {tip}" for tip in health_tips])
                
                # Store the message and timestamp
                st.session_state.personal_health_analysis_message = final_analysis_message
                st.session_state.saved_personal_analysis = {
                    'timestamp': datetime.datetime.now(),
                    'message': final_analysis_message
                }
                st.balloons()
                # 設定頁面索引，導向設定頁面 (索引為 4)
                st.session_state.current_page_index = page_names.index("⚙️ 設定")
                st.rerun() # 重新運行以使更改生效並停留在設定Tab

        # Display the stored analysis message if it exists
        if st.session_state.saved_personal_analysis['message']:
            st.markdown("---")
            st.subheader("💡 我的專屬健康分析")
            timestamp_str = st.session_state.saved_personal_analysis['timestamp'].strftime('%Y-%m-%d %H:%M')
            st.info(f"**分析時間：{timestamp_str}**\n\n{st.session_state.saved_personal_analysis['message']}")


    st.markdown("---")

    # Start of "管理食物選項" expander
    with st.expander("🍔 管理食物選項", expanded=True): # Renamed this expander
        st.write("在這裡，您可以自訂食物清單，讓飲食紀錄更符合您的習慣。")
        
        # 智能辨識美食 區塊標題和說明文字修正
        st.markdown(
            """
            <h4 style='color: #d81b60; font-family: "Comic Sans MS", "Arial Rounded MT Bold", sans-serif;'>
                智能辨識美食
            </h4>
            <p style='font-family: "Comic Sans MS", "Arial Rounded MT Bold", sans-serif; color: #5d4037;'>
                上傳一張香噴噴的照片，讓小助手幫你解鎖食物的秘密，輕鬆記錄飲食！
            </p>
            """, unsafe_allow_html=True
        )

        # --- 重要提示：請替換您的 Gemini API Key ---
        # 您可以在這裡替換您的 OpenWeatherMap API Key。
        # 如果您沒有，請前往 Google AI Studio 獲取：https://aistudio.google.com/
        # 無效或缺失的 API Key 將導致 AI 辨識功能無法運作。
        # 在某些部署環境中，API Key 可能會被自動注入，但在本地運行時您可能需要手動設置。
        gemini_api_key = "AIzaSyAC6l7WtS00C6NbfIieSP88iS4BG6P0gog" # Replace with your actual Gemini API Key

        # 上傳圖片按鈕文字修正
        uploaded_food_image_for_ai = st.file_uploader(
            "上傳圖片", # 修正為 "上傳圖片"
            type=["jpg", "jpeg", "png"],
            key="food_image_uploader_ai",
            help="📸 上傳您的食物照片，讓小幫手為您辨識！"
        )
        
        # Display the uploaded image (only display, not save), centered
        if uploaded_food_image_for_ai is not None:
            st.image(uploaded_food_image_for_ai, caption='您上傳的可愛圖片', width=250)
            st.markdown("<style>img[alt='您上傳的可愛圖片'] {display: block; margin-left: auto; margin-right: auto;}</style>", unsafe_allow_html=True)


        # State to store AI food name suggestion
        if 'ai_food_suggestion_name' not in st.session_state:
            st.session_state.ai_food_suggestion_name = ""
        # State to control showing the add food form after AI description
        if 'show_ai_assisted_add_form' not in st.session_state:
            st.session_state.show_ai_assisted_add_form = False
        # State to store the AI suggested calories
        if 'ai_suggested_calories' not in st.session_state:
            st.session_state.ai_suggested_calories = 0


        # Changed button class to 'ai-button' for custom styling
        if st.button("AI分析", key="analyze_food_image_button", help="點擊讓智能小幫手分析圖片中的食物！", disabled=(uploaded_food_image_for_ai is None)): # Disable if no image uploaded
            if uploaded_food_image_for_ai is not None:
                with st.empty(): # For dynamic content (loading animation, then result)
                    st.markdown("<div class='ai-loading-spinner'></div>", unsafe_allow_html=True)
                    st.info("智能小幫手正在努力思考中... 🧠 請稍候喔！")
                
                try:
                    image_bytes = uploaded_food_image_for_ai.read()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')

                    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
                    headers = {"Content-Type": "application/json"}

                    # First Gemini API request: food description
                    prompt_description = {
                        "contents": [
                            {
                                "parts": [
                                    {"text": "這張圖片是什麼食物或餐點？請用一句簡潔、可愛的話來形容，例如：'看起來像美味的義大利麵！'、'這可能是香甜的草莓蛋糕！'、'好像是豐盛的早餐盤呢！' 如果無法辨識，請回答：'這張圖片有點模糊，小幫手還在學習中！' 不要提供卡路里數字。"},
                                    {
                                        "inlineData": {
                                            "mimeType": uploaded_food_image_for_ai.type,
                                            "data": base64_image
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                    response_desc = requests.post(api_url, json=prompt_description, headers=headers)
                    response_desc.raise_for_status()
                    result_desc = response_desc.json()

                    suggestion_text = "這張圖片有點模糊，小幫手還在學習中！"
                    if result_desc and result_desc.get('candidates') and result_desc['candidates'][0].get('content') and result_desc['candidates'][0]['content'].get('parts'):
                        suggestion_text = result_desc['candidates'][0]['content']['parts'][0]['text']
                    
                    st.session_state.ai_food_suggestion_name = suggestion_text # Store the description
                    
                    # Clean up suggestion text for calorie estimation
                    cleaned_food_name_for_cal = suggestion_text.replace("！", "").replace("看起來像美味的", "").replace("這可能是香甜的", "").replace("好像是豐盛的", "").strip()

                    # Second Gemini API request: calorie estimation
                    # Only call for calorie if the description is not the "cannot recognize" message
                    estimated_calories = 0
                    if "這張圖片有點模糊" not in suggestion_text:
                        prompt_calories = {
                            "contents": [
                                {
                                    "parts": [
                                        {"text": f"請估計一下一份'{cleaned_food_name_for_cal}'大約含有多少大卡熱量？請只回覆一個數字，不需要任何文字說明。如果無法估計，請回覆 0。"}
                                    ]
                                }
                            ]
                        }
                        response_cal = requests.post(api_url, json=prompt_calories, headers=headers)
                        response_cal.raise_for_status()
                        result_cal = response_cal.json()

                        if result_cal and result_cal.get('candidates') and result_cal['candidates'][0].get('content') and result_cal['candidates'][0]['content'].get('parts'):
                            try:
                                # Attempt to parse the response as an integer
                                estimated_calories = int(result_cal['candidates'][0]['content']['parts'][0]['text'].strip())
                                if estimated_calories < 0: # Ensure calories are not negative
                                    estimated_calories = 0
                            except ValueError:
                                estimated_calories = 0 # Fallback if parsing fails
                        
                    st.session_state.ai_suggested_calories = estimated_calories # Store found calories or 0
                    st.session_state.show_ai_assisted_add_form = True # Show the manual add form
                    
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"呼叫小幫手時發生連線錯誤：{http_err} (狀態碼: {response_desc.status_code if 'response_desc' in locals() else 'N/A'})。請檢查您的 API Key 或網路連線。")
                    st.session_state.ai_food_suggestion_name = "網路或API連線有問題，請稍後再試。"
                    st.session_state.ai_suggested_calories = 0
                    st.session_state.show_ai_assisted_add_form = False
                except requests.exceptions.ConnectionError as conn_err:
                    st.error(f"網路連線錯誤: {conn_err}。小幫手無法連線。")
                    st.session_state.ai_food_suggestion_name = "網路連線異常，請檢查您的網路。"
                    st.session_state.ai_suggested_calories = 0
                    st.session_state.show_ai_assisted_add_form = False
                except requests.exceptions.Timeout as timeout_err:
                    st.error(f"請求小幫手超時: {timeout_err}。請重試或檢查網路連線。")
                    st.session_state.ai_food_suggestion_name = "請求超時了，小幫手有點累了。"
                    st.session_state.ai_suggested_calories = 0
                    st.session_state.show_ai_assisted_add_form = False
                except requests.exceptions.RequestException as req_err:
                    st.error(f"呼叫小幫手時發生錯誤：{req_err}。")
                    st.session_state.ai_food_suggestion_name = "小幫手出了一點小狀況。"
                    st.session_state.ai_suggested_calories = 0
                    st.session_state.show_ai_assisted_add_form = False
                except Exception as e:
                    st.error(f"分析食物時發生未知錯誤：{e}")
                    st.session_state.ai_food_suggestion_name = "發生了小意外，無法分析。"
                    st.session_state.ai_suggested_calories = 0
                    st.session_state.show_ai_assisted_add_form = False
                
                # After processing, set the current page index to settings to re-render with new state
                st.session_state.current_page_index = page_names.index("⚙️ 設定")
                st.rerun()

        # Display AI suggestion and manual add form
        if st.session_state.ai_food_suggestion_name:
            st.markdown("---")
            st.subheader("🎉 小幫手的分析結果！")
            
            # Customizing error message for AI analysis failure
            if "這張圖片有點模糊" in st.session_state.ai_food_suggestion_name or "發生了小意外" in st.session_state.ai_food_suggestion_name or "網路連線異常" in st.session_state.ai_food_suggestion_name or "請求超時了" in st.session_state.ai_food_suggestion_name:
                cute_error_message = ""
                if "模糊" in st.session_state.ai_food_suggestion_name:
                    cute_error_message = "🥺 這張圖片有點模糊，小幫手還在學習中！換張更清楚的試試？"
                elif "意外" in st.session_state.ai_food_suggestion_name:
                    cute_error_message = "😅 發生了點小意外，小幫手迷路了！請再試一次？"
                elif "網路" in st.session_state.ai_food_suggestion_name:
                    cute_error_message = "🚧 網路有點小堵車，小幫手連不上線啦！請檢查網路後再試？"
                elif "超時" in st.session_state.ai_food_suggestion_name:
                    cute_error_message = "😴 小幫手思考太久了！請耐心一點再試？"
                else: # Generic fallback for other errors
                    cute_error_message = "🤔 哎呀，小幫手暫時無法分析這張圖片，請換張圖片再試試看！"

                st.markdown(
                    f"<div class='ai-suggestion-box' style='background-color: #ffcccc; border-color: #ff6666;'>{cute_error_message}</div>",
                    unsafe_allow_html=True
                )
                # No need to show the input form if AI analysis failed.
                st.session_state.show_ai_assisted_add_form = False
            else:
                st.markdown(
                    f"<div class='ai-suggestion-box'><span class='emoji-large'>💡</span> {st.session_state.ai_food_suggestion_name}</div>",
                    unsafe_allow_html=True
                )
                st.write("根據小幫手的建議，請在下方輸入更詳細的食物資訊：")
            
            # Only show this form if show_ai_assisted_add_form is True
            if st.session_state.show_ai_assisted_add_form:
                with st.form("add_food_based_on_ai_form"):
                    # Pre-fill with AI suggestion, but allow user to edit
                    # Clean up suggestion for pre-fill, ensure it's just the food name
                    clean_for_input = st.session_state.ai_food_suggestion_name.replace("！", "").replace("看起來像美味的", "").replace("這可能是香甜的", "").replace("好像是豐盛的", "").strip()
                    new_food_name_ai_assisted = st.text_input(
                        "食物名稱",
                        value=clean_for_input,
                        key="ai_assisted_food_name_input",
                        help="請輸入食物名稱，可參考上方智能助理的建議"
                    )
                    
                    # Pre-fill calories with AI suggested calories or 0
                    new_food_calories_ai_assisted = st.number_input(
                        "預估熱量 (大卡)",
                        min_value=0,
                        value=st.session_state.ai_suggested_calories, # Use AI suggested calories here
                        key="ai_assisted_calories_input",
                        help="請輸入此食物的熱量值 (精準度由您決定！)"
                    )
                    
                    # Determine initial category for AI-assisted food. If a food item was found in the database, use its category. Otherwise, default to "AI分析"
                    initial_ai_category = "AI分析"
                    # Try to find category from food_database based on input name (which might be the AI suggestion)
                    if new_food_name_ai_assisted in st.session_state.food_database:
                        initial_ai_category = st.session_state.food_database[new_food_name_ai_assisted]['category']
                    
                    food_categories_for_ai_form = ["AI分析", "中式", "西式", "甜點", "水果", "蔬菜", "穀物與澱粉", "堅果與種子", "肉類與海鮮", "乳製品與蛋", "飲料", "其他"]
                    
                    new_food_category_ai_assisted = st.selectbox(
                        "選擇類別",
                        options=food_categories_for_ai_form,
                        index=food_categories_for_ai_form.index(initial_ai_category) if initial_ai_category in food_categories_for_ai_form else 0,
                        key="ai_assisted_category_select"
                    )
                    
                    # Changed button class to 'stButton>button[kind="primary"]' for custom styling in CSS
                    submit_ai_assisted_food = st.form_submit_button("確認並新增到我的食物資料庫 ✨", help="點擊此按鈕，將修改後的食物資訊新增到您的資料庫中。")

                    if submit_ai_assisted_food:
                        if new_food_name_ai_assisted and new_food_calories_ai_assisted >= 0:
                            if new_food_name_ai_assisted not in st.session_state.food_database:
                                st.session_state.food_database[new_food_name_ai_assisted] = {"calories": new_food_calories_ai_assisted, "category": new_food_category_ai_assisted}
                                st.success(f"'{new_food_name_ai_assisted}' (熱量: {new_food_calories_ai_assisted} 大卡) 已成功新增到食物資料庫！太棒了！")
                            else:
                                st.session_state.food_database[new_food_name_ai_assisted].update({"calories": new_food_calories_ai_assisted, "category": new_food_category_ai_assisted})
                                st.info(f"食物 '{new_food_name_ai_assisted}' 已存在資料庫中，已更新其熱量和類別。")
                            
                            st.session_state.ai_food_suggestion_name = "" # Clear suggestion after adding
                            st.session_state.ai_suggested_calories = 0 # Reset suggested calories
                            st.session_state.show_ai_assisted_add_form = False # Hide the form
                            st.session_state.current_page_index = page_names.index("⚙️ 設定")
                            st.rerun()
                        else:
                            st.warning("請確認食物名稱和熱量是否有效。")
        
        st.markdown("---")
        st.markdown("#### 📝 手動新增/刪除 食物選項") # New title for manual food management
        st.write("您也可以手動輸入食物資訊來擴充或刪除您的食物資料庫。")

        # Display current food database
        if st.session_state.food_database:
            food_df = pd.DataFrame([{'食物名稱': name, '熱量(大卡)': data['calories'], '類別': data['category']} for name, data in st.session_state.food_database.items()])
            st.dataframe(food_df, use_container_width=True, key="settings_food_database_df")
        else:
            st.info("食物資料庫目前為空。")

        # Add food section
        with st.form("manual_add_food_form"):
            new_food_name_manual = st.text_input("輸入新食物名稱", key="manual_new_food_name_input", help="例如：滷雞腿便當")
            new_food_calories_manual = st.number_input("輸入新食物熱量 (大卡)", min_value=0, value=0, key="manual_new_food_calories_input", help="此食物的預估熱量值")
            new_food_category_manual = st.selectbox("選擇食物類別",
                                                   options=["中式", "西式", "甜點", "水果", "蔬菜", "穀物與澱粉", "堅果與種子", "肉類與海鮮", "乳製品與蛋", "飲料", "其他", "AI分析"],
                                                   key="manual_new_food_category_select", help="為您的新食物選擇一個分類")
            add_manual_food_button = st.form_submit_button("新增食物")
            
            if add_manual_food_button:
                if new_food_name_manual and new_food_calories_manual >= 0:
                    if new_food_name_manual not in st.session_state.food_database:
                        st.session_state.food_database[new_food_name_manual] = {"calories": new_food_calories_manual, "category": new_food_category_manual}
                        st.success(f"已新增 '{new_food_name_manual}' 到食物選單，類別: {new_food_category_manual}。")
                    else:
                        st.warning(f"食物 '{new_food_name_manual}' 已存在，將更新其熱量為 {new_food_calories_manual} 大卡，類別為 {new_food_category_manual}。")
                        st.session_state.food_database[new_food_name_manual].update({"calories": new_food_calories_manual, "category": new_food_category_manual})
                    st.session_state.current_page_index = page_names.index("⚙️ 設定")
                    st.rerun()
                else:
                    st.warning("請輸入有效的食物名稱、熱量和類別。")
        
        # Delete food section
        with st.form("manual_delete_food_form"):
            food_to_delete_manual = st.selectbox("選擇要刪除的食物", [""] + sorted(list(st.session_state.food_database.keys())), key="manual_delete_food_selectbox", help="選擇您想從列表中移除的食物")
            delete_manual_food_button = st.form_submit_button("刪除選定食物")
            if delete_manual_food_button:
                if food_to_delete_manual and food_to_delete_manual in st.session_state.food_database:
                    del st.session_state.food_database[food_to_delete_manual]
                    st.success(f"已刪除 '{food_to_delete_manual}'。")
                    st.session_state.current_page_index = page_names.index("⚙️ 設定")
                    st.rerun()
                else:
                    st.warning("請選擇要刪除的食物。")
    # End of "管理食物選項" expander


    st.markdown("---")

    # Start of "新增/刪除 運動選項" expander (Moved to a separate expander)
    with st.expander("🏃‍♀️ 新增/刪除 運動選項", expanded=True): # New expander
        st.write("在這裡，您可以自訂運動清單，讓運動紀錄更符合您的習慣。")

        st.write("目前運動選單 (可供選擇):")
        st.write("這是您所有預設和您新增的運動列表，方便您管理。")
        st.dataframe(pd.DataFrame(list(st.session_state.exercise_calories_per_min.items()), columns=['運動', '每分鐘消耗卡路里']), use_container_width=True, key="settings_exercise_database_df")

        # Add new exercise
        with st.form("add_exercise_form"):
            new_exercise_name = st.text_input("輸入新運動名稱", key="new_exercise_name_input", help="例如：跳舞")
            new_exercise_calories_per_min = st.number_input("每分鐘消耗熱量 (大卡)", min_value=0, value=5, step=1, key="new_exercise_calories_input", help="此運動每分鐘的預估熱量消耗值")
            add_exercise_button = st.form_submit_button("新增運動")
            if add_exercise_button:
                if new_exercise_name and new_exercise_calories_per_min >= 0:
                    if new_exercise_name not in st.session_state.exercise_calories_per_min:
                        st.session_state.exercise_calories_per_min[new_exercise_name] = new_exercise_calories_per_min
                        st.success(f"已新增 '{new_exercise_name}' 到運動選單。")
                    else:
                        st.warning(f"運動 '{new_exercise_name}' 已存在，將更新每分鐘消耗熱量為 {new_exercise_calories_per_min} 大卡。")
                        st.session_state.exercise_calories_per_min[new_exercise_name] = new_exercise_calories_per_min
                    st.session_state.current_page_index = page_names.index("⚙️ 設定")
                    st.rerun()
                else:
                    st.warning("請輸入有效的運動名稱和每分鐘消耗熱量。")
        
        # Delete exercise
        with st.form("delete_exercise_form"):
            exercise_to_delete = st.selectbox("選擇要刪除的運動", [""] + sorted(list(st.session_state.exercise_calories_per_min.keys())), key="delete_exercise_selectbox", help="選擇您想從列表中移除的運動")
            delete_button = st.form_submit_button("刪除選定運動")
            if delete_button:
                if exercise_to_delete and exercise_to_delete in st.session_state.exercise_calories_per_min:
                    del st.session_state.exercise_calories_per_min[exercise_to_delete]
                    st.success(f"已刪除 '{exercise_to_delete}'。")
                    st.session_state.current_page_index = page_names.index("⚙️ 設定")
                    st.rerun()
                else:
                    st.warning("請選擇要刪除的運動。")
    # End of "新增/刪除 運動選項" expander

    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)


# --- 小幫手頁面 (新增功能) ---
def assistant_page():
    st.header("🤖 智能小幫手")
    st.write("讓小幫手為您量身打造專屬的養生、健康或減肥菜單與運動計畫！")
    st.write("---")

    # --- 重要提示：請替換您的 Gemini API Key ---
    gemini_api_key = "AIzaSyAC6l7WtS00C6NbfIieSP88iS4BG6P0gog" # Replace with your actual Gemini API Key

    def call_gemini_api_for_plan(prompt_text, gemini_api_key, schema):
        """
        Calls the Gemini API to generate structured meal and exercise plans.
        """
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": schema
            }
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=60) # Increased timeout
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            result = response.json()
            
            if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
                json_string = result['candidates'][0]['content']['parts'][0]['text']
                # Gemini sometimes returns raw JSON string, sometimes a JSON object.
                # Ensure it's a string that can be parsed.
                if isinstance(json_string, dict):
                    return json_string # Already parsed
                return json.loads(json_string)
            else:
                st.error("小幫手沒有生成有效的內容。")
                return None
        except requests.exceptions.HTTPError as http_err:
            st.error(f"小幫手連線錯誤: {http_err}. 請檢查 API Key 是否正確或服務是否可用。")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"網路連線錯誤: {conn_err}. 請檢查您的網路。")
            return None
        except requests.exceptions.Timeout as timeout_err:
            st.error(f"請求小幫手超時: {timeout_err}. 請重試。")
            return None
        except json.JSONDecodeError as json_err:
            st.error(f"解析小幫手回傳資料錯誤: {json_err}. 回傳內容可能不是有效的 JSON。")
            print(f"Failed JSON: {result}") # For debugging
            return None
        except Exception as e:
            st.error(f"呼叫小幫手時發生未知錯誤: {e}")
            return None

    # Define the JSON schema for Gemini's response
    # This schema defines a weekly plan (array of 7 days)
    # Each day has meal and exercise plans
    plan_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "day": {"type": "STRING", "description": "例如：星期一"},
                "meals": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "meal_type": {"type": "STRING", "description": "例如：早餐、午餐、晚餐、點心"},
                            "food_items": {
                                "type": "ARRAY",
                                "items": {"type": "STRING"}
                            },
                            "recipe_notes": {"type": "STRING", "description": "簡單的烹飪建議或組合說明"}
                        },
                        "required": ["meal_type", "food_items"]
                    }
                },
                "exercises": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "exercise_type": {"type": "STRING", "description": "例如：慢跑、重訓、瑜伽"},
                            "duration": {"type": "STRING", "description": "例如：30分鐘"},
                            "intensity": {"type": "STRING", "description": "例如：輕度、中等、高強度"}
                        },
                        "required": ["exercise_type", "duration"]
                    }
                }
            },
            "required": ["day", "meals", "exercises"]
        }
    }


    # Options for goal and duration
    goal_options = ["養生", "健康", "減肥"]
    duration_options = ["一週", "一個月"]

    # Input fields for general plan generation
    st.subheader("💡 智能生成計畫")
    st.write("設定您的健康目標與時長，讓智能小幫手為您量身打造專屬的飲食與運動計畫！")
    col_goal, col_duration = st.columns(2)
    with col_goal:
        goal = st.selectbox("選擇您的健康目標", goal_options, key="assistant_goal_select")
    with col_duration:
        duration = st.selectbox("選擇計畫時長", duration_options, key="assistant_duration_select")

    # Get user profile information from session_state for personalized prompts
    user_age = st.session_state.get('age', 25)
    user_gender = st.session_state.get('gender', '男性')
    user_activity_level = st.session_state.get('activity_level', '久坐 (很少運動)')

    # Try to get latest weight and height for BMR/TDEE calculation
    latest_weight = 65.0
    latest_height = 170.0
    if not st.session_state.df_history.empty:
        last_record = st.session_state.df_history.sort_values(by='日期', ascending=False).iloc[0]
        latest_weight = last_record['體重(kg)'] if pd.notna(last_record['體重(kg)']) and last_record['體重(kg)'] > 0 else 65.0
        latest_height = last_record['身高(公分)'] if pd.notna(last_record['身高(公分)']) and last_record['身高(公分)'] > 0 else 170.0
    else:
        st.warning("請在「設定」頁面更新您的個人資訊（身高、體重、年齡、活動程度），以便小幫手提供更精準的建議。目前將使用預設值。")


    bmr, tdee = calculate_bmr_tdee(user_gender, latest_weight, latest_height, user_age, user_activity_level)

    # Generate Plan Button
    if st.button("生成計畫", key="generate_plan_button"):
        with st.empty():
            st.markdown("<div class='ai-loading-spinner'></div>", unsafe_allow_html=True)
            st.info("小幫手正在為您設計專屬計畫... 🚀 請稍候喔！")

        # Construct the prompt for Gemini
        prompt = f"請為一位{user_age}歲的{user_gender}、身高{latest_height:.1f}公分、體重{latest_weight:.1f}公斤，活動程度為'{user_activity_level}'的用戶，設計一個{duration}的{goal}計畫。\n"
        prompt += f"根據其估計基礎代謝率 (BMR) 約 {bmr:.0f} 大卡，每日總能量消耗 (TDEE) 約 {tdee:.0f} 大卡，請提供詳細的飲食菜單和運動菜單。\n"
        
        if goal == "減肥":
            target_calorie_range = f"{max(0, tdee - 500):.0f} - {tdee - 250:.0f} 大卡"
            prompt += f"飲食菜單的每日總熱量目標範圍大約在 {target_calorie_range} 之間。\n"
            prompt += "飲食應以原型食物為主，低油、低糖、高纖、足量蛋白質。每餐請提供簡單食譜或組合說明。\n"
            prompt += "運動菜單應包含有氧運動和力量訓練，並提供每項運動的時間或組數建議，以及強度標示（輕度、中等、高強度）。\n"
        elif goal == "健康":
            target_calorie_range = f"{tdee - 100:.0f} - {tdee + 100:.0f} 大卡"
            prompt += f"飲食菜單的每日總熱量目標範圍大約在 {target_calorie_range} 之間，強調均衡營養，五大類食物都應包含。\n"
            prompt += "飲食應注重多樣性，色彩豐富，烹飪方式健康。每餐請提供簡單食譜或組合說明。\n"
            prompt += "運動菜單應注重全身協調和心肺功能，包含多樣化的運動類型，並提供每項運動的時間或組數建議，以及強度標示。\n"
        elif goal == "養生":
            target_calorie_range = f"{tdee - 200:.0f} - {tdee:.0f} 大卡"
            prompt += f"飲食菜單的每日總熱量目標範圍大約在 {target_calorie_range} 之間，強調溫和滋補、易於消化，可多使用季節性食材、藥膳食材（如紅棗、枸杞等），但避免過於複雜。\n"
            prompt += "烹飪方式以蒸、煮、燉為主，避免油炸和重口味。每餐請提供簡單食譜或組合說明。\n"
            prompt += "運動菜單應以舒緩、有助於身心放鬆和經絡通暢的運動為主，例如瑜伽、太極、散步等，並提供每項運動的時間或組數建議，以及強度標示（輕度、中等）。\n"

        if duration == "一週":
            prompt += "請生成接下來7天的每日計畫。"
            plan_schema_for_gemini = plan_schema
        else: # 一個月
            prompt += "請生成一個月的計畫，可以按週或每5-7天為一個循環提供計畫。\n"
            # For monthly plan, we might ask Gemini to generate 4 weeks of plans.
            # Or generate a template for a week and suggest repeating it.
            # Let's try to ask for 4 weeks with the same schema for simplicity,
            # or it can generate a smaller array and explain "repeat this"
            prompt += "如果內容過多，您可以提供一個通用的一週計畫並建議重複執行4次，或提供四個不同的週計畫摘要。請清晰標示每一天。"
            plan_schema_for_gemini = plan_schema # Using the same schema for now, might need adaptation if Gemini returns more complex monthly structure.

        st.session_state.generated_plan = call_gemini_api_for_plan(prompt, gemini_api_key, plan_schema_for_gemini)

        if st.session_state.generated_plan:
            st.success("小幫手已為您生成專屬計畫！")
        else:
            st.error("抱歉，小幫手暫時無法生成計畫。請確認輸入資訊或稍後再試。")
        
        # Keep the user on the assistant page
        st.session_state.current_page_index = page_names.index("🤖 小幫手")
        st.rerun()

    # Display generated plan if available in session state
    if st.session_state.get('generated_plan'):
        st.markdown("---")
        st.subheader(f"✨ 您的 {duration} {goal} 計畫")
        st.write("這是一份為您量身打造的健康藍圖，跟著小幫手一起變健康吧！")

        plan_data = st.session_state.generated_plan

        # If the plan is for a month and Gemini generated a weekly template, handle it
        # This part might need refinement based on actual Gemini output structure
        if duration == "一個月" and len(plan_data) < 28: # Heuristic for a condensed monthly plan (e.g., just one week's worth)
            st.info("這是您的一個月計畫的第一週範例。您可以重複此循環四次來完成一個月的計畫！")
            
        for day_plan in plan_data:
            with st.expander(f"🗓️ **{day_plan.get('day', '未命名日')}**", expanded=True):
                st.markdown("<p class='plan-header'>🍽️ 飲食菜單</p>", unsafe_allow_html=True)
                if day_plan.get('meals'):
                    for meal in day_plan['meals']:
                        food_items_str = ", ".join(meal.get('food_items', []))
                        st.markdown(f"<p class='day-header'>{meal.get('meal_type', '餐點')}：</p>", unsafe_allow_html=True)
                        st.markdown(f"- **菜色**: {food_items_str}")
                        if meal.get('recipe_notes'):
                            st.markdown(f"- **備註**: {meal['recipe_notes']}")
                else:
                    st.info("無飲食建議。")

                st.markdown("<p class='plan-header'>🏋️‍♀️ 運動菜單</p>", unsafe_allow_html=True)
                if day_plan.get('exercises'):
                    for exercise in day_plan['exercises']:
                        st.markdown(f"<p class='day-header'>{exercise.get('exercise_type', '運動')}：</p>", unsafe_allow_html=True)
                        st.markdown(f"- **時間**: {exercise.get('duration', 'N/A')}")
                        st.markdown(f"- **強度**: {exercise.get('intensity', 'N/A')}")
                else:
                    st.info("無運動建議。")
            st.markdown("---") # Separator between days

    st.markdown("---")
    # New section for "各類減肥菜單" (Diet Plans)
    st.subheader("🥗 各類減肥菜單")
    st.write("探索不同的飲食方案，找到適合您的健康生活方式！")

    diet_type = st.selectbox(
        "選擇您感興趣的飲食方案",
        [
            "地中海飲食",
            "生酮飲食",
            "168斷食溫和版",
            "1212斷食",
            "減醣飲食",
            "碳水循環",
            "劉亦菲減肥法",
            "五日輕斷食",
            "便利商店減肥菜單商品",
            "藝人減肥菜單"
        ],
        key="diet_type_select"
    )

    # Dictionary containing detailed information for each diet plan.
    # This data structure allows for easy expansion and maintenance of diet information.
    diet_info = {
        "地中海飲食": {
            "描述": "一種強調攝取大量蔬菜、水果、全穀物、豆類、堅果、橄欖油，並適量攝取魚類、乳製品和禽肉，紅肉較少的飲食模式。",
            "適合人群": "追求健康、慢性病預防、心血管健康，或想改善生活方式的人。不適合需要嚴格控制特定營養素攝取的人群。",
            "如何實施": """
            * **多吃：** 蔬菜、水果、全穀物、豆類、堅果、種子、香料、橄欖油。
            * **適量：** 魚類、海鮮（每週至少兩次）、禽肉、蛋、乳製品（優格、起司）。
            * **少吃：** 紅肉、加工食品、精緻碳水化合物、含糖飲料。
            * **飲品：** 水是主要飲品，適量飲用紅酒（如果適用）。
            **一週菜單範例：**
            * **早餐：** 全麥吐司搭配酪梨和水煮蛋；或優格加水果和堅果。
            * **午餐：** 藜麥沙拉搭配烤鮭魚和多種蔬菜；或扁豆湯搭配全麥麵包。
            * **晚餐：** 雞肉燉蔬菜（用橄欖油烹調）；或全麥義大利麵搭配海鮮和番茄醬。
            * **點心：** 水果、堅果、蔬菜棒。
            """,
            "優點": "有益心臟健康、降低慢性病風險、體重管理、抗炎。",
            "缺點": "可能需要花更多時間準備食物，對不習慣地中海食材的人來說可能初期較難適應。",
            "建議": "從逐步增加蔬菜、水果和全穀物的攝取開始，用橄欖油取代其他脂肪。"
        },
        "生酮飲食": {
            "描述": "一種極低碳水化合物、高脂肪、適量蛋白質的飲食方式，旨在讓身體進入「生酮狀態」，燃燒脂肪而非碳水化合物作為主要能量來源。",
            "適合人群": "需快速減重、癲癇患者（在醫生指導下），或對其他飲食法效果不佳者。不適合孕婦、哺乳期婦女、肝腎功能不全者、糖尿病患者（需嚴密監控）。**執行前務必諮詢醫生或營養師。**",
            "如何實施": """
            * **碳水化合物：** 每天攝取通常限制在 20-50 克以下。
            * **脂肪：** 佔總熱量攝取的 70-75%。
            * **蛋白質：：** 佔總熱量攝取的 20-25%。
            **常見食物：**
            * **脂肪：** 酪梨、橄欖油、椰子油、奶油、堅果、種子。
            * **蛋白質：** 肉類、魚類、蛋、起司。
            * **蔬菜：** 綠葉蔬菜（菠菜、羽衣甘藍）、花椰菜、西蘭花。
            **一週菜單範例：**
            * **早餐：** 炒蛋加酪梨和培根。
            * **午餐：** 鮭魚沙拉（高脂醬料）。
            * **晚餐：** 烤雞腿搭配奶油菠菜。
            * **點心：** 堅果、起司、防彈咖啡。
            """,
            "優點": "快速減重、控制血糖、改善癲癇、可能降低食慾。",
            "缺點": "可能導致「酮流感」（疲勞、頭痛、噁心）、營養不均、對心臟健康影響尚有爭議、長期執行困難。",
            "建議": "必須在專業人士指導下進行，注意電解質補充，多喝水，並監測身體反應。"
        },
        "168斷食溫和版": {
            "描述": "每日將進食時間限制在 8 小時內，其餘 16 小時禁食（包含睡眠時間）。溫和版可能允許在禁食期間飲用無糖咖啡、茶、水等。",
            "適合人群": "想嘗試間歇性斷食的初學者、體重管理者、想改善胰島素敏感度者。不適合孕婦、哺乳期婦女、糖尿病患者（需在醫生指導下）、體重過輕者、飲食失調者。",
            "如何實施": """
            * 選擇一個 8 小時的進食窗口，例如中午 12 點到晚上 8 點。
            * 在進食窗口內正常飲食（健康均衡的餐點）。
            * 在禁食期間只飲用無熱量飲品。
            **溫和版特點：**
            * 可能允許在禁食期攝取少量（例如 50 卡以下）的食物，但這會削弱斷食效果，較建議只喝無熱量飲品。
            **一日菜單範例（進食窗口 12:00-20:00）：**
            * **12:00 午餐：** 糙米飯、烤雞胸肉、多種蔬菜。
            * **16:00 點心：** 一份水果或優格。
            * **19:00 晚餐：** 蔬菜湯麵或雜糧飯搭配魚肉。
            * **禁食期：** 只喝水、黑咖啡、無糖茶。
            """,
            "優點": "有助於體重管理、改善胰島素敏感度、簡化飲食、可能改善細胞修復。",
            "缺點": "初期可能感到飢餓或疲勞、部分人可能出現頭暈、注意力不集中。",
            "建議": "循序漸進，從縮短進食窗口開始；在進食期間確保營養均衡；多喝水。"
        },
        "1212斷食": {
            "描述": "最溫和的間歇性斷食形式，每天有 12 小時的進食窗口和 12 小時的禁食窗口。例如，早上 8 點到晚上 8 點進食，其餘時間禁食。",
            "適合人群": "間歇性斷食的入門者、作息規律的人、想改善消化和輕微體重管理者。",
            "如何實施": """
            * 選擇一個方便的 12 小時進食窗口。
            * 確保在進食窗口內攝取均衡的三餐。
            * 禁食期間只飲用無熱量飲品。
            **一日菜單範例（進食窗口 08:00-20:00）：**
            * **08:00 早餐：** 燕麥粥加水果和堅果。
            * **13:00 午餐：** 雞肉蔬菜捲餅。
            * **19:00 晚餐：** 豆腐蔬菜炒飯。
            * **禁食期：：** 只喝水、黑咖啡、無糖茶。
            """,
            "優點": "非常容易執行、對身體負擔小、有助於建立規律飲食習慣、改善消化。",
            "缺點": "減重效果可能不如更長時間的斷食顯著。",
            "建議": "這是個很好的入門方式，可以慢慢過渡到 14:10 或 16:8。"
        },
        "減醣飲食": {
            "描述": "相對低碳水化合物的飲食方式，通常將每日碳水化合物攝取量控制在 100-150 克（或更低，但高於生酮飲食）。強調優質蛋白質、健康脂肪和大量蔬菜。",
            "適合人群": "想控制血糖、體重管理、改善代謝症候群、或對高碳水飲食敏感者。相對生酮飲食更具彈性，適合長期執行。",
            "如何實施": """
            * **減少：** 精緻碳水化合物（白米、白麵包、含糖飲料、甜點）。
            * **選擇：** 全穀物（糙米、藜麥）、豆類、大量非澱粉類蔬菜、優質蛋白質（雞蛋、魚、肉、豆腐）、健康脂肪（酪梨、橄欖油、堅果）。
            **一週菜單範例：**
            * **早餐：** 全麥三明治（無糖花生醬、蛋、生菜）；或水煮蛋配小黃瓜和番茄。
            * **午餐：** 雞胸肉沙拉（多樣蔬菜、酪梨）；或雜糧飯搭配烤魚和炒青菜。
            * **晚餐：** 豆腐菇菇煲；或低醣花椰菜米炒飯。
            * **點心：** 一小把堅果、優格、蔬菜棒。
            """,
            "優點": "有助於穩定血糖、控制體重、改善飽足感、相對容易長期維持。",
            "缺點": "初期可能對澱粉類食物的戒斷反應；需要學習食物的碳水含量。",
            "建議": "從逐步減少精緻澱粉開始，增加蛋白質和纖維攝取，保持均衡。"
        },
        "碳水循環": {
            "描述": "一種在低碳日、中碳日和高碳日之間切換的飲食策略。旨在最大化脂肪燃燒、維持肌肉量和優化訓練表現。",
            "適合人群": "健身愛好者、運動員、有減脂增肌需求的人，或想突破減重平台期者。不適合對飲食控制要求較低或時間不充裕者。",
            "如何實施": """
            * **低碳日：：** 通常在不訓練或輕度訓練日，攝取極低碳水化合物（如 50 克以下），高脂肪、高蛋白質。
            * **中碳日：：** 在中等強度訓練日，適量碳水化合物，中等脂肪、高蛋白質。
            * **高碳日：：** 在高強度訓練日或身體需要補充糖原時，攝取高碳水化合物，低脂肪、中等蛋白質。
            **注意事項：** 碳水化合物的來源以複合碳水化合物為主（糙米、燕麥、地瓜），避免精緻碳水。
            **範例：**
            * 週一、週三、週五：低碳日（休息或輕度訓練）
            * 週二、週四：高碳日（高強度訓練）
            * 週六、週日：中碳日（活動日或恢復）
            """,
            "優點": "有助於燃燒脂肪、維持肌肉量、提供訓練能量、防止代謝適應。",
            "缺點": "執行複雜，需要精確計算宏量營養素、不適合所有人、初期較難適應。",
            "建議": "需配合運動計畫，建議在專業人士指導下進行，學習精確追蹤食物攝取。"
        },
        "劉亦菲減肥法": {
            "描述": "據傳劉亦菲在拍攝《花木蘭》期間採用的減肥方法，核心是**低油、低鹽、低糖、高蛋白、高纖維**，並強調食物原型。",
            "適合人群": "追求健康、均衡飲食的減重者，或想改善飲食習慣的人。不適合需要快速減重或有特殊營養需求的人。",
            "如何實施": """
            * **原則：**
                * **低油：** 烹飪方式以清蒸、水煮、涼拌、烤為主。
                * **低鹽：** 少鹽或無鹽，以天然香料調味。
                * **低糖：** 避免所有含糖飲料和甜點，選擇天然甜味（水果）。
                * **高蛋白：** 充足的雞胸肉、魚肉、蛋、豆腐等。
                * **高纖維：** 大量蔬菜、全穀物、水果。
            * **食物選擇：**
                * **主食：** 糙米、玉米、藜麥、全麥麵包。
                * **蛋白質：** 雞胸肉、魚肉、蝦、蛋、豆腐。
                * **蔬菜：** 各種顏色的蔬菜。
                * **水果：：** 新鮮水果。
                * **飲品：** 白開水、無糖茶。
            **一日菜單範例：**
            * **早餐：** 水煮蛋兩顆、一杯無糖豆漿、一小份雜糧饅頭。
            * **午餐：：** 清蒸鱸魚、涼拌花椰菜、一小碗糙米飯。
            * **晚餐：** 烤雞胸肉沙拉（不加醬或低脂醬）、玉米半根。
            * **點心：** 一份水果。
            """,
            "優點": "健康均衡、有益長期維持、改善皮膚狀態、身體負擔小。",
            "缺點": "可能見效較慢、對於重口味的人來說可能初期較難適應。",
            "建議": "循序漸進調整飲食習慣，多嘗試不同的健康烹飪方式。"
        },
        "五日輕斷食": {
            "描述": "一種流行的間歇性斷食變體，通常指每週有 5 天正常飲食，2 天限制熱量攝取（通常為 500-600 大卡）。著名的有 5:2 斷食法。",
            "適合人群": "想嘗試間歇性斷食、輕度減重、改善代謝健康、或不想每天嚴格控制飲食者。不適合孕婦、哺乳期婦女、糖尿病患者（需在醫生指導下）、體重過輕者、飲食失調者。",
            "如何實施": """
            * 選擇每週的非連續的 2 天作為輕斷食日。
            * **輕斷食日：** 女性攝取約 500 大卡，男性約 600 大卡。通常分兩餐或三餐，以高蛋白、高纖維、低碳水食物為主。
            * **正常飲食日：** 保持健康、均衡的飲食，避免暴飲暴食。
            **輕斷食日範例菜單（500大卡）：**
            * **早餐：** 一顆水煮蛋 (70大卡) + 一杯無糖黑咖啡 (5大卡)。
            * **午餐：** 烤雞胸肉 100克 (165大卡) + 燙青菜 150克 (30大卡)。
            * **晚餐：** 鮪魚罐頭 (水煮) 半罐 (80大卡) + 小黃瓜一根 (15大卡) + 一小碗蔬菜湯 (50大卡)。
            """,
            "優點": "減重效果顯著、改善胰島素敏感度、有助於細胞修復、相對靈活。",
            "缺點": "斷食日可能感到飢餓、精力不足、初期較難適應。",
            "建議": "斷食日確保攝取足夠水分，並選擇能提供飽足感的蛋白質和纖維。非斷食日保持健康飲食。"
        },
        "便利商店減肥菜單商品": {
            "描述": "利用便利商店現有商品搭配出的減肥菜單，方便快捷，適合忙碌的上班族或外食族。",
            "適合人群": "忙碌、經常外食、沒有時間自己準備三餐的減重者。",
            "如何實施": """
            * **選擇原則：**
                * **高蛋白：** 茶葉蛋、雞胸肉、無糖豆漿、牛奶、優格。
                * **高纖維：** 沙拉（醬料分開或選和風/油醋）、玉米、地瓜、水果。
                * **低精緻碳水：** 選擇糙米飯糰、御飯糰（避開油炸餡料）。
                * **健康脂肪：：** 堅果（適量）。
                * **飲品：** 無糖茶、黑咖啡、水。
            **一日菜單範例：**
            * **早餐：** 茶葉蛋兩顆 + 無糖豆漿一杯 + 御飯糰（鮪魚或肉鬆，非油炸）。
            * **午餐：** 義式雞胸肉沙拉（醬料減半或不加）+ 烤地瓜。
            * **晚餐：** 關東煮（選擇清湯、無加工火鍋料、蔬菜、豆腐）+ 一顆水煮蛋。
            * **點心：** 水果（蘋果或香蕉）或無糖優格。
            """,
            "優點": "方便、省時、易於執行、選擇多樣。",
            "缺點": "可能較難精確控制熱量和營養素、加工食品較多、部分商品鈉含量可能較高。",
            "建議": "仔細閱讀營養標示，選擇低加工、低糖、低鈉的產品；醬料獨立包裝的盡量減少使用。"
        },
        "藝人減肥菜單": {
            "描述": "蒐集整理部分藝人公開分享的減肥飲食策略。這些菜單通常非常嚴格，目標是快速達到特定體態。",
            "適合人群": "了解自身體質、有強大自律性、並在專業人士（醫生、營養師）指導下進行短期目標減重的人。**不建議長期執行，且可能不適合一般大眾。**",
            "如何實施": """
            * **範例（某藝人減肥菜單，僅供參考，實際請勿盲目模仿）：**
                * **早餐：** 一顆水煮蛋、一杯無糖黑咖啡、半片全麥麵包。
                * **午餐：** 少量水煮雞胸肉、一大盤清燙蔬菜。
                * **晚餐：** 一小份魚肉、綠葉蔬菜沙拉（無醬）。
                * **飲品：** 大量白開水。
            * **共同特點：**
                * 極低的熱量攝取。
                * 高蛋白質，以防肌肉流失。
                * 極低的碳水化合物和脂肪。
                * 幾乎無加工食品、無調味。
                * 通常會配合高強度運動。
            """,
            "優點": "短期內見效快。",
            "缺點": "極端、難以持續、容易反彈、可能造成營養不良、對身體健康有潛在風險。**強烈不建議在無專業人士指導下嘗試。**",
            "建議": "藝人減肥菜單通常是為了應對特定的工作需求，並有專業團隊指導。請勿盲目跟隨，應以自身健康為重，選擇均衡、可持續的飲食方式。如有減重需求，務必諮詢醫生或營養師。"
        }
    }

    # Using Streamlit expanders to make the content collapsible, keeping the layout clean and cute.
    # Each diet plan information is wrapped in a custom styled div for consistent look
    st.markdown("---")
    st.markdown(f"<div class='diet-plan-card'>", unsafe_allow_html=True) # Start of custom card
    st.markdown(f"<h4>關於 {diet_type}</h4>", unsafe_allow_html=True) # Title for the specific diet type

    info = diet_info.get(diet_type, {"描述": "無相關資訊。", "適合人群": "", "如何實施": "", "優點": "", "缺點": "", "建議": ""})
    
    with st.expander(f"✨ **描述與適合人群**", expanded=True):
        st.markdown(f"**描述：** {info['描述']}")
        st.markdown(f"**適合人群：** {info['適合人群']}")

    with st.expander(f"🍽️ **如何實施 (菜單範例)**"):
        st.markdown(info['如何實施'])

    with st.expander(f"📈 **優缺點與建議**"):
        st.markdown(f"**優點：** {info['優點']}")
        st.markdown(f"**缺點：** {info['缺點']}")
        st.markdown(f"**建議：** {info['建議']}")
    
    st.markdown("</div>", unsafe_allow_html=True) # End of custom card

    st.markdown("---")
    st.info("**免責聲明：** 這裡提供的飲食資訊僅供參考，不應替代專業醫療或營養建議。在開始任何新的飲食計畫前，請務必諮詢您的醫生或註冊營養師。")

    # 將「回到頂部」按鈕置中，並使用新的樣式，指向 app_top
    st.markdown("<div style='text-align: center;'><a href='#app_top' class='scroll-to-top-btn'><span class='emoji'>⬆️</span> 回到頂部</a></div>", unsafe_allow_html=True)


# --- 主應用程式邏輯 ---
# 應用程式標題、LOGO 和 Slogan
st.markdown(
    f"""
    <div style='display: flex; align-items: center; margin-bottom: 5px;'>
        <img src='data:image/png;base64,{logo_base64}' class='logo-img' width='60' style='margin-right: 15px;'>
        <h1 style='color: #d81b60; margin: 0; font-family: "Comic Sans MS", "Arial Rounded MT Bold", sans-serif;'>健康日記 Health Diary</h1>
    </div>
    """,
    unsafe_allow_html=True
)
# 歡迎語和健康小語現在由 home_page 函數處理，這裡不需要重複顯示
st.markdown("---") # 保持分隔線

# 新的導覽方式：使用 st.radio 模擬分頁
page_names = ["🏠 首頁", "✍️ 新增紀錄", "📊 數據分析", "🗂 歷史紀錄", "⚙️ 設定", "🤖 小幫手"]

# 初始化 current_page_index，確保它始終是有效的索引
if 'current_page_index' not in st.session_state:
    st.session_state.current_page_index = 0 # 預設為首頁
elif not (0 <= st.session_state.current_page_index < len(page_names)):
    # 如果 current_page_index 超出範圍，重置為 0
    st.session_state.current_page_index = 0

# st.radio 的 index 參數直接使用 session state 中的索引
# 為了隱藏 "導覽" 字串，這裡將 label 設為空字串，並使用 CSS 隱藏預設的 label
selected_page_index_from_radio = st.radio(
    "頁面導覽", # <-- 將這裡的空字串替換為您想要的導覽文字
    options=page_names,
    index=st.session_state.current_page_index,
    horizontal=True,
    key="main_navigation_radio"
)

# 根據用戶在 radio button 上的選擇，更新 session state 的索引
# 這確保了當用戶點擊導覽按鈕時，current_page_index 會被正確更新
st.session_state.current_page_index = page_names.index(selected_page_index_from_radio)


# 根據選擇的頁面索引呼叫對應的函數
if st.session_state.current_page_index == page_names.index("🏠 首頁"):
    home_page(st.session_state.df_history)
elif st.session_state.current_page_index == page_names.index("✍️ 新增紀錄"):
    add_record_page()
elif st.session_state.current_page_index == page_names.index("📊 數據分析"):
    data_analysis_page(st.session_state.df_history)
elif st.session_state.current_page_index == page_names.index("🗂 歷史紀錄"):
    history_page(st.session_state.df_history)
elif st.session_state.current_page_index == page_names.index("⚙️ 設定"):
    settings_page()
elif st.session_state.current_page_index == page_names.index("🤖 小幫手"):
    assistant_page()

# 頁尾插圖 (已包含在 CSS 中進行居中)
if footer_image_base64:
    st.markdown(
        f"""
        <div class='footer-image-container'>
            <img src='data:image/png;base64,{footer_image_base64}' width='200'>
        </div>
        """,
        unsafe_allow_html=True
    )
