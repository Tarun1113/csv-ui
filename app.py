import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CSV Viewer",
    page_icon="📂",
    layout="wide",
)

# ─────────────────────────────────────────────
#  STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Background ── */
.stApp { background: #f4f6fb; }

/* ── Card wrapper ── */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border: 1.5px solid #e3e8f0;
}

/* ── Section heading ── */
.sec-title {
    font-size: 20px;
    font-weight: 800;
    color: #1a237e;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
}

/* ── File slot label ── */
.slot-label {
    font-size: 14px;
    font-weight: 700;
    color: #3949ab;
    margin-bottom: 4px;
    margin-top: 10px;
}

/* ── Submit button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(90deg, #1e88e5 0%, #1565c0 100%);
    color: #ffffff;
    font-size: 18px;
    font-weight: 800;
    border-radius: 12px;
    padding: 16px 0;
    border: none;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(30,136,229,0.35);
    transition: opacity 0.2s;
}
div[data-testid="stButton"] > button:hover { opacity: 0.88; color: #fff; }

/* ── Metric cards ── */
.kpi-row { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:18px; }
.kpi {
    background: #e8eaf6;
    border-radius: 12px;
    padding: 16px 26px;
    min-width: 130px;
    text-align: center;
    border: 1.5px solid #c5cae9;
}
.kpi-val { font-size: 28px; font-weight: 900; color: #283593; }
.kpi-lbl { font-size: 11px; color: #5c6bc0; font-weight: 600; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Status banners ── */
.status-warn {
    background:#fff8e1; border:1.5px solid #ffe082; border-radius:10px;
    padding:10px 18px; color:#f57f17; font-weight:600; margin-bottom:12px;
}
.status-ok {
    background:#e8f5e9; border:1.5px solid #a5d6a7; border-radius:10px;
    padding:10px 18px; color:#2e7d32; font-weight:600; margin-bottom:12px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def read_csv(f):
    try:
        return pd.read_csv(f, encoding="utf-8")
    except UnicodeDecodeError:
        f.seek(0)
        return pd.read_csv(f, encoding="latin-1")

def kpi(df):
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-val">{df.shape[0]:,}</div><div class="kpi-lbl">Rows</div></div>
      <div class="kpi"><div class="kpi-val">{df.shape[1]}</div><div class="kpi-lbl">Columns</div></div>
      <div class="kpi"><div class="kpi-val">{df.isnull().sum().sum()}</div><div class="kpi-lbl">Missing</div></div>
      <div class="kpi"><div class="kpi-val">{df.duplicated().sum()}</div><div class="kpi-lbl">Duplicates</div></div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding:28px 0 10px 0;">
  <div style="font-size:32px;font-weight:900;color:#1a237e;">📂 CSV File Viewer</div>
  <div style="font-size:15px;color:#546e7a;margin-top:4px;">
      Upload up to 4 CSV files → click <b>Submit</b> → explore your data instantly
  </div>
</div>
""", unsafe_allow_html=True)
st.divider()


# ─────────────────────────────────────────────
#  BLOCK 1-4 : UPLOAD SLOTS
# ─────────────────────────────────────────────
st.markdown('<div class="sec-title">📤 Step 1 — Upload CSV Files</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="slot-label">📄 File 1</div>', unsafe_allow_html=True)
    f1 = st.file_uploader("File 1", type="csv", key="f1", label_visibility="collapsed")

    st.markdown('<div class="slot-label">📄 File 3</div>', unsafe_allow_html=True)
    f3 = st.file_uploader("File 3", type="csv", key="f3", label_visibility="collapsed")

with col2:
    st.markdown('<div class="slot-label">📄 File 2</div>', unsafe_allow_html=True)
    f2 = st.file_uploader("File 2", type="csv", key="f2", label_visibility="collapsed")

    st.markdown('<div class="slot-label">📄 File 4</div>', unsafe_allow_html=True)
    f4 = st.file_uploader("File 4", type="csv", key="f4", label_visibility="collapsed")

uploads = {"File 1": f1, "File 2": f2, "File 3": f3, "File 4": f4}
n = sum(1 for v in uploads.values() if v)

st.markdown("<br>", unsafe_allow_html=True)
if n == 0:
    st.info("ℹ️  No files uploaded yet — please upload at least one CSV file.")
elif n < 4:
    st.markdown(f'<div class="status-warn">⚠️  {n} of 4 files uploaded. You can still submit.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-ok">✅  All 4 files uploaded and ready!</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BLOCK 5 : SUBMIT BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sec-title">🚀 Step 2 — Submit</div>', unsafe_allow_html=True)
submit = st.button("  Submit & View Output  ", disabled=(n == 0))


# ─────────────────────────────────────────────
#  OUTPUT SECTION
# ─────────────────────────────────────────────
if submit:
    st.divider()
    st.markdown('<div class="sec-title">📊 Step 3 — Output</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    active = {k: v for k, v in uploads.items() if v}
    tabs   = st.tabs(list(active.keys()))

    for tab, (name, f) in zip(tabs, active.items()):
        with tab:
            try:
                df = read_csv(f)
                st.markdown(f"**File name:** `{f.name}`")
                kpi(df)

                t1, t2, t3 = st.tabs(["📋 Data Preview", "📈 Column Info", "📉 Statistics"])

                with t1:
                    st.caption(f"Showing first 200 rows of {df.shape[0]:,} total")
                    st.dataframe(df.head(200), use_container_width=True, height=400)

                with t2:
                    info = pd.DataFrame({
                        "Column":        df.columns,
                        "Type":          df.dtypes.astype(str).values,
                        "Non-Null":      df.notnull().sum().values,
                        "Null Count":    df.isnull().sum().values,
                        "Null %":        (df.isnull().mean()*100).round(1).astype(str)+"%",
                        "Unique Values": df.nunique().values,
                    })
                    st.dataframe(info, use_container_width=True, height=400)

                with t3:
                    num = df.select_dtypes(include="number")
                    if num.empty:
                        st.info("No numeric columns found in this file.")
                    else:
                        st.dataframe(num.describe().T.round(4), use_container_width=True, height=400)

            except Exception as e:
                st.error(f"❌ Could not read **{name}** (`{f.name}`): {e}")

    # ── Combined download ──────────────────────────────────────────
    st.divider()
    st.markdown("#### 💾 Download Combined Data")
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
        st.download_button(
            "⬇️  Download All as One CSV",
            data=out.to_csv(index=False).encode("utf-8"),
            file_name="combined_output.csv",
            mime="text/csv",
        )
