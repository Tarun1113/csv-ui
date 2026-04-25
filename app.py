import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Viewer", page_icon="📂", layout="wide")

st.markdown("""
<style>
.stApp { background: #f4f6fb; }
div[data-testid="stButton"] > button {
    width: 100%; background: #1e88e5; color: white;
    font-size: 17px; font-weight: 800; border-radius: 10px;
    padding: 14px 0; border: none;
}
div[data-testid="stButton"] > button:hover { background: #1565c0; color: white; }
.kpi-row { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:16px; }
.kpi { background:#e8eaf6; border-radius:10px; padding:14px 22px; min-width:120px; text-align:center; }
.kpi-val { font-size:26px; font-weight:900; color:#283593; }
.kpi-lbl { font-size:11px; color:#5c6bc0; font-weight:600; text-transform:uppercase; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def read_csv(f):
    try:
        return pd.read_csv(f, encoding="utf-8")
    except UnicodeDecodeError:
        f.seek(0)
        return pd.read_csv(f, encoding="latin-1")

def show_kpi(df):
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-val">{df.shape[0]:,}</div><div class="kpi-lbl">Rows</div></div>
      <div class="kpi"><div class="kpi-val">{df.shape[1]}</div><div class="kpi-lbl">Columns</div></div>
      <div class="kpi"><div class="kpi-val">{df.isnull().sum().sum()}</div><div class="kpi-lbl">Missing</div></div>
      <div class="kpi"><div class="kpi-val">{df.duplicated().sum()}</div><div class="kpi-lbl">Duplicates</div></div>
    </div>""", unsafe_allow_html=True)

# ── Header ──
st.title("📂 CSV File Viewer")
st.markdown("Upload up to **4 CSV files** → click **Submit** → explore your data instantly.")
st.divider()

# ── 4 Upload Blocks ──
st.markdown("### 📤 Step 1 — Upload CSV Files")
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("**📄 File 1**")
    f1 = st.file_uploader("File 1", type="csv", key="f1", label_visibility="collapsed")
    st.markdown("**📄 File 3**")
    f3 = st.file_uploader("File 3", type="csv", key="f3", label_visibility="collapsed")
with col2:
    st.markdown("**📄 File 2**")
    f2 = st.file_uploader("File 2", type="csv", key="f2", label_visibility="collapsed")
    st.markdown("**📄 File 4**")
    f4 = st.file_uploader("File 4", type="csv", key="f4", label_visibility="collapsed")

uploads = {"File 1": f1, "File 2": f2, "File 3": f3, "File 4": f4}
n = sum(1 for v in uploads.values() if v)

st.markdown("<br>", unsafe_allow_html=True)
if n == 0:
    st.info("ℹ️  Upload at least one CSV file to continue.")
elif n < 4:
    st.warning(f"⚠️  {n} of 4 files uploaded. You can still submit.")
else:
    st.success("✅  All 4 files uploaded and ready!")

# ── Submit Block ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🚀 Step 2 — Submit")
submit = st.button("Submit & View Output", disabled=(n == 0))

# ── Output ──
if submit:
    st.divider()
    st.markdown("### 📊 Step 3 — Output")
    active = {k: v for k, v in uploads.items() if v}
    tabs = st.tabs(list(active.keys()))

    for tab, (name, f) in zip(tabs, active.items()):
        with tab:
            try:
                df = read_csv(f)
                st.markdown(f"**File:** `{f.name}`")
                show_kpi(df)
                t1, t2, t3 = st.tabs(["📋 Data Preview", "📈 Column Info", "📉 Statistics"])
                with t1:
                    st.caption(f"First 200 rows of {df.shape[0]:,} total")
                    st.dataframe(df.head(200), use_container_width=True, height=400)
                with t2:
                    info = pd.DataFrame({
                        "Column": df.columns,
                        "Type": df.dtypes.astype(str).values,
                        "Non-Null": df.notnull().sum().values,
                        "Null Count": df.isnull().sum().values,
                        "Null %": (df.isnull().mean()*100).round(1).astype(str)+"%",
                        "Unique": df.nunique().values,
                    })
                    st.dataframe(info, use_container_width=True, height=400)
                with t3:
                    num = df.select_dtypes(include="number")
                    if num.empty:
                        st.info("No numeric columns in this file.")
                    else:
                        st.dataframe(num.describe().T.round(4), use_container_width=True, height=400)
            except Exception as e:
                st.error(f"❌ Could not read {name}: {e}")

    st.divider()
    frames = []
    for name, f in active.items():
        try:
            f.seek(0)
            d = read_csv(f)
            d.insert(0, "Source", f.name)
            frames.append(d)
        except Exception:
            pass
    if frames:
        out = pd.concat(frames, ignore_index=True)
        st.download_button("⬇️  Download All as One CSV",
            data=out.to_csv(index=False).encode("utf-8"),
            file_name="combined_output.csv", mime="text/csv")
