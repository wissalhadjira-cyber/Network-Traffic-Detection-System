import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import time
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Network Traffic Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. Custom CSS Theme
# ==========================================
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Cairo:wght@400;600;700&display=swap');
    
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2e 0%, #0f0c29 50%, #000000 100%);
    }
    
    /* Headings */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        letter-spacing: 1px;
    }
    
    h4, h5, h6, p, span, div, label, li {
        font-family: 'Cairo', sans-serif;
        color: #e0e0e0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 2px solid rgba(123, 47, 247, 0.4);
        box-shadow: 5px 0 20px rgba(123, 47, 247, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(123, 47, 247, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(123, 47, 247, 0.7);
        background: linear-gradient(90deg, #7b2ff7, #00d4ff);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 47, 247, 0.1));
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(123, 47, 247, 0.4);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-size: 32px !important;
        font-weight: bold !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0 !important;
        font-size: 14px !important;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(102, 126, 234, 0.08);
        border: 2px dashed rgba(123, 47, 247, 0.5);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.08);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #7b2ff7, transparent);
        margin: 25px 0;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.1), rgba(123, 47, 247, 0.1));
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Select boxes / Inputs */
    .stSelectbox > div > div, .stNumberInput > div > div {
        background: rgba(15, 12, 41, 0.8);
        border: 1px solid rgba(123, 47, 247, 0.4);
        border-radius: 10px;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(15, 12, 41, 0.5);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
    }
    
    /* Main Header Card */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    .main-header h1 {
        color: white !important;
        -webkit-text-fill-color: white !important;
        font-size: 42px;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    }
    
    .main-header p {
        color: #f0f0f0 !important;
        margin-top: 12px;
        font-size: 16px;
        position: relative;
        z-index: 1;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #7b2ff7;
        font-family: 'Orbitron', sans-serif;
        font-size: 13px;
        letter-spacing: 1px;
        margin-top: 40px;
        border-top: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f0c29;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00d4ff, #7b2ff7);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Language Dictionary
# ==========================================
LANG = {
    "en": {
        "title": "🛡️ Network Traffic Detection System",
        "subtitle": "Analyze network traffic (CSV / Realtime)",
        "settings": "⚙️ Settings",
        "language": "🌐 Language",
        "mode": "📊 Analysis Mode",
        "mode_csv": "📂 CSV File",
        "mode_realtime": "⚡ Realtime Capture",
        "upload_label_csv": "Choose a CSV file to scan",
        "start_btn": "🚀 Start Analysis",
        "analyzing": "Analyzing...",
        "status_header": "🔍 Network Status",
        "safe": "🟢 **Network is SAFE** ✅",
        "safe_caption": "No suspicious traffic detected",
        "danger": "🔴 **{count:,} suspicious flows detected!** 🚨",
        "danger_caption": "Attack ratio: {pct:.2f}%",
        "total_flows": "📊 Total Flows",
        "attacks": "🔴 Attacks",
        "details_header": "📊 Traffic Details",
        "distribution": "**📈 Type Distribution:**",
        "pie_title": "Traffic Distribution",
        "attacks_header": "🚨 Detected Attacks",
        "attack_types": "**Attack Types:**",
        "attack_chart": "Attack Distribution",
        "view_attacks": "📋 View Attack Details",
        "no_file": "⏳ Please upload a file to begin.",
        "rt_header": "⚡ Realtime Packet Capture",
        "rt_select_iface": "🌐 Select Network Interface",
        "rt_duration": "⏱️ Capture Duration (seconds)",
        "rt_packet_limit": "📦 Max Packets",
        "rt_start": "▶️ Start Capture",
        "rt_capturing": "🔄 Capturing...",
        "rt_aggregating": "📦 Captured {count} packets. Aggregating flows...",
        "rt_analyzing": "🔍 Analyzed {count} flows. Running prediction...",
        "rt_captured": "✅ Captured {count} packets → {flows} flows",
        "rt_no_packets": "⚠️ No packets captured. Try again.",
        "rt_no_flows": "⚠️ No flows could be aggregated",
        "rt_error": "❌ Capture error: {error}",
        "rt_tip": "💡 Tip: Open YouTube during capture to generate traffic",
    },
    "ar": {
        "title": "🛡️ نظام كشف التسلل الشبكي (NIDS)",
        "subtitle": "تحليل حركة المرور (CSV / مباشر)",
        "settings": "⚙️ الإعدادات",
        "language": "🌐 اللغة",
        "mode": "📊 وضع التحليل",
        "mode_csv": "📂 ملف CSV",
        "mode_realtime": "⚡ التقاط مباشر",
        "upload_label_csv": "اختر ملف CSV للفحص",
        "start_btn": "🚀 بدء التحليل",
        "analyzing": "جارٍ التحليل...",
        "status_header": "🔍 حالة الشبكة",
        "safe": "🟢 **الشبكة آمنة تماماً** ✅",
        "safe_caption": "لم يتم اكتشاف أي حركة مرور مشبوهة",
        "danger": "🔴 **تم اكتشاف {count:,} حركة مرور مشبوهة!** 🚨",
        "danger_caption": "نسبة الهجمات: {pct:.2f}%",
        "total_flows": "📊 إجمالي التدفقات",
        "attacks": "🔴 الهجمات",
        "details_header": "📊 تفاصيل حركة المرور",
        "distribution": "**📈 توزيع الأنواع:**",
        "pie_title": "توزيع حركة المرور",
        "attacks_header": "🚨 الهجمات المكتشفة",
        "attack_types": "**أنواع الهجمات:**",
        "attack_chart": "توزيع الهجمات",
        "view_attacks": "📋 عرض تفاصيل الهجمات",
        "no_file": "⏳ الرجاء رفع ملف للبدء.",
        "rt_header": "⚡ التقاط الحزم المباشر",
        "rt_select_iface": "🌐 اختر واجهة الشبكة",
        "rt_duration": "⏱️ مدة الالتقاط (ثواني)",
        "rt_packet_limit": "📦 الحد الأقصى للحزم",
        "rt_start": "▶️ بدء الالتقاط",
        "rt_capturing": "🔄 جارٍ الالتقاط...",
        "rt_aggregating": "📦 تم التقاط {count} حزمة. تجميع التدفقات...",
        "rt_analyzing": "🔍 تم تحليل {count} تدفق. جارٍ التنبؤ...",
        "rt_captured": "✅ تم التقاط {count} حزمة → {flows} تدفق",
        "rt_no_packets": "⚠️ لم يتم التقاط أي حزمة. حاول مرة أخرى.",
        "rt_no_flows": "⚠️ لم يتم تجميع أي تدفق",
        "rt_error": "❌ خطأ في الالتقاط: {error}",
        "rt_tip": "💡 نصيحة: افتح YouTube أثناء الالتقاط لتوليد حركة مرور",
    }
}

# ==========================================
# 4. Language Selector (Sidebar)
# ==========================================
st.sidebar.title(LANG["en"]["settings"])

lang_choice = st.sidebar.radio(
    LANG["en"]["language"],
    ["English", "العربية"],
    index=0
)

lang = "ar" if lang_choice == "العربية" else "en"
t = LANG[lang]

# ==========================================
# 5. Mode Selector (Sidebar)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader(t["mode"])

mode = st.sidebar.radio(
    t["mode"],
    [t["mode_csv"], t["mode_realtime"]],
    index=0,
    label_visibility="collapsed"
)

# ==========================================
# 6. Load Model
# ==========================================
@st.cache_resource
def load_models():
    try:
        model = joblib.load("random_forest_model.pkl")
        encoder = joblib.load("label_encoder.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, encoder, scaler
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

model, encoder, scaler = load_models()

# ==========================================
# 7. Helper Functions
# ==========================================
def prepare_data(df):
    """Prepare data for prediction"""
    df_prepared = df.copy()
    df_prepared.columns = df_prepared.columns.str.strip()
    df_prepared.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_prepared.fillna(0, inplace=True)

    if df_prepared.shape[1] > 15:
        df_prepared = df_prepared.iloc[:, :15]

    try:
        return scaler.transform(df_prepared)
    except:
        return df_prepared.values

def analyze_data(data):
    """Analyze data and return results"""
    X_scaled = prepare_data(data)
    predictions = model.predict(X_scaled)
    labels = encoder.inverse_transform(predictions)

    total = len(labels)
    malware_count = np.sum(labels != "BENIGN")

    return {
        'labels': labels,
        'total': total,
        'malware_count': malware_count,
        'is_safe': malware_count == 0,
        'df': data
    }

def display_results(results, data, t):
    """Display analysis results"""
    st.markdown("---")
    st.subheader(t["status_header"])

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if results['is_safe']:
            st.success(t["safe"])
            st.caption(t["safe_caption"])
        else:
            st.error(t["danger"].format(count=results['malware_count']))
            st.caption(
                t["danger_caption"].format(
                    pct=results['malware_count'] / results['total'] * 100
                )
            )

    with col2:
        st.metric(t["total_flows"], f"{results['total']:,}")

    with col3:
        st.metric(t["attacks"], f"{results['malware_count']:,}")

    # Traffic Details
    st.markdown("---")
    st.subheader(t["details_header"])

    data['Prediction'] = results['labels']
    traffic_dist = pd.Series(results['labels']).value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.write(t["distribution"])
        for label, count in traffic_dist.items():
            percentage = (count / results['total']) * 100
            emoji = "🔴" if label != "BENIGN" else "🟢"
            bar = "█" * int(percentage / 2)
            st.write(f"{emoji} {label}: {count:,} ({percentage:.2f}%) {bar}")

    with col2:
        fig = px.pie(
            values=traffic_dist.values,
            names=traffic_dist.index,
            title=t["pie_title"],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family='Cairo'),
            title_font=dict(color='#00d4ff', size=18)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detected Attacks
    if not results['is_safe']:
        st.subheader(t["attacks_header"])

        attacks = data[data['Prediction'] != 'BENIGN']
        attack_dist = attacks['Prediction'].value_counts()

        col1, col2 = st.columns(2)

        with col1:
            st.write(t["attack_types"])
            for attack, count in attack_dist.items():
                st.write(f"• {attack}: {count:,}")

        with col2:
            fig_attacks = px.bar(
                x=attack_dist.index,
                y=attack_dist.values,
                title=t["attack_chart"],
                color=attack_dist.index
            )
            fig_attacks.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0', family='Cairo'),
                title_font=dict(color='#00d4ff', size=18),
                xaxis=dict(gridcolor='rgba(123,47,247,0.2)'),
                yaxis=dict(gridcolor='rgba(123,47,247,0.2)')
            )
            st.plotly_chart(fig_attacks, use_container_width=True)

        with st.expander(t["view_attacks"]):
            st.dataframe(attacks)

# ==========================================
# 8. Custom Header
# ==========================================
st.markdown(f"""
<div class="main-header">
    <h1>{t["title"]}</h1>
    <p>{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 9. MODE: CSV File
# ==========================================
if mode == t["mode_csv"]:
    uploaded_file = st.file_uploader(t["upload_label_csv"], type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.info(f"✅ Loaded {len(data):,} rows")

        with st.expander("📊 Data Preview"):
            st.dataframe(data.head(10))

        if st.button(t["start_btn"], type="primary"):
            with st.spinner(t["analyzing"]):
                results = analyze_data(data)
                display_results(results, data, t)
    else:
        st.info(t["no_file"])

# ==========================================
# 10. MODE: Realtime Capture
# ==========================================
elif mode == t["mode_realtime"]:
    st.header(t["rt_header"])

    try:
        from scapy.all import IP, TCP, UDP, get_working_ifaces, sniff
    except ImportError:
        st.error("❌ Scapy not installed. Run: pip install scapy")
        st.stop()

    try:
        interfaces = [iface.name for iface in get_working_ifaces()]
    except Exception as e:
        st.error(f"❌ Cannot get interfaces: {e}")
        st.info("Make sure you're running as Administrator")
        st.stop()

    selected_iface = st.selectbox(t["rt_select_iface"], interfaces)

    col1, col2 = st.columns(2)
    with col1:
        duration = st.slider(t["rt_duration"], 5, 60, 15)
    with col2:
        packet_limit = st.number_input(t["rt_packet_limit"], 10, 2000, 200)

    st.caption(t["rt_tip"])

    def aggregate_flows(packets):
        """Aggregate packets into flows and compute 15 features"""
        from collections import defaultdict

        flows = defaultdict(lambda: {
            'fwd_packets': [], 'bwd_packets': [],
            'fwd_times': [], 'bwd_times': [],
            'fwd_sizes': [], 'bwd_sizes': [],
        })

        for pkt in packets:
            if IP not in pkt:
                continue

            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            if TCP in pkt:
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
            elif UDP in pkt:
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
            else:
                continue

            flow_key = tuple(sorted([(src_ip, sport), (dst_ip, dport)]))
            pkt_size = len(pkt)
            pkt_time = float(pkt.time)

            if (src_ip, sport) == flow_key[0]:
                flows[flow_key]['fwd_packets'].append(pkt)
                flows[flow_key]['fwd_times'].append(pkt_time)
                flows[flow_key]['fwd_sizes'].append(pkt_size)
            else:
                flows[flow_key]['bwd_packets'].append(pkt)
                flows[flow_key]['bwd_times'].append(pkt_time)
                flows[flow_key]['bwd_sizes'].append(pkt_size)

        flow_features = []

        for flow_key, data in flows.items():
            fwd_pkts = data['fwd_packets']
            bwd_pkts = data['bwd_packets']

            if not fwd_pkts:
                continue

            first_pkt = fwd_pkts[0]
            if TCP in first_pkt:
                dst_port = first_pkt[TCP].dport
            elif UDP in first_pkt:
                dst_port = first_pkt[UDP].dport
            else:
                dst_port = 0

            all_times = data['fwd_times'] + data['bwd_times']
            if len(all_times) > 1:
                flow_duration = (max(all_times) - min(all_times)) * 1_000_000
            else:
                flow_duration = 0

            total_fwd = len(fwd_pkts)
            total_bwd = len(bwd_pkts)

            fwd_sizes = data['fwd_sizes'] if data['fwd_sizes'] else [0]
            bwd_sizes = data['bwd_sizes'] if data['bwd_sizes'] else [0]

            total_len_fwd = sum(fwd_sizes)
            total_len_bwd = sum(bwd_sizes)

            fwd_max = max(fwd_sizes)
            fwd_min = min(fwd_sizes)
            fwd_mean = sum(fwd_sizes) / len(fwd_sizes)

            bwd_max = max(bwd_sizes) if bwd_sizes else 0
            bwd_min = min(bwd_sizes) if bwd_sizes else 0
            bwd_mean = sum(bwd_sizes) / len(bwd_sizes) if bwd_sizes else 0

            if flow_duration > 0:
                flow_bytes_s = (total_len_fwd + total_len_bwd) / (flow_duration / 1_000_000)
                flow_pkts_s = (total_fwd + total_bwd) / (flow_duration / 1_000_000)
            else:
                flow_bytes_s = 0
                flow_pkts_s = 0

            sorted_times = sorted(all_times)
            if len(sorted_times) > 1:
                iats = [(sorted_times[i+1] - sorted_times[i]) * 1_000_000
                        for i in range(len(sorted_times) - 1)]
                flow_iat_mean = sum(iats) / len(iats)
            else:
                flow_iat_mean = 0

            features = {
                'Destination Port': dst_port,
                'Flow Duration': flow_duration,
                'Total Fwd Packets': total_fwd,
                'Total Backward Packets': total_bwd,
                'Total Length of Fwd Packets': total_len_fwd,
                'Total Length of Bwd Packets': total_len_bwd,
                'Fwd Packet Length Max': fwd_max,
                'Fwd Packet Length Min': fwd_min,
                'Fwd Packet Length Mean': fwd_mean,
                'Bwd Packet Length Max': bwd_max,
                'Bwd Packet Length Min': bwd_min,
                'Bwd Packet Length Mean': bwd_mean,
                'Flow Bytes/s': flow_bytes_s,
                'Flow Packets/s': flow_pkts_s,
                'Flow IAT Mean': flow_iat_mean,
            }

            flow_features.append(features)

        return pd.DataFrame(flow_features)

    if st.button(t["rt_start"], type="primary"):
        st.info(t["rt_capturing"])

        progress = st.progress(0)
        status = st.empty()

        captured_packets = []

        def packet_callback(pkt):
            captured_packets.append(pkt)

        try:
            sniff(
                iface=selected_iface,
                prn=packet_callback,
                timeout=duration,
                count=packet_limit,
                store=False
            )

            progress.progress(50)
            status.info(t["rt_aggregating"].format(count=len(captured_packets)))

            if captured_packets:
                flows_df = aggregate_flows(captured_packets)
                progress.progress(80)

                if len(flows_df) > 0:
                    status.info(t["rt_analyzing"].format(count=len(flows_df)))

                    results = analyze_data(flows_df)
                    progress.progress(100)
                    status.success(
                        t["rt_captured"].format(
                            count=len(captured_packets),
                            flows=len(flows_df)
                        )
                    )

                    display_results(results, flows_df, t)
                else:
                    progress.progress(100)
                    status.warning(t["rt_no_flows"])
            else:
                progress.progress(100)
                status.warning(t["rt_no_packets"])

        except Exception as e:
            status.error(t["rt_error"].format(error=str(e)))
            st.info("💡 Try running PowerShell as Administrator")