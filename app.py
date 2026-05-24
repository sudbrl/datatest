import streamlit as st
from supabase import create_client, Client
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataPortal",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SIMPLE LOGIN SYSTEM ──────────────────────────────────────────────────────
def check_login(username, password):
    correct_user = st.secrets.get("APP_USERNAME")
    correct_pass = st.secrets.get("APP_PASSWORD")
    return username == correct_user and password == correct_pass


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def login_page():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background: #0f1117;
        }

        /* Hide default streamlit elements on login */
        #MainMenu, footer, header { visibility: hidden; }

        .login-wrap {
            max-width: 360px;
            margin: 8vh auto 0 auto;
            padding: 2.5rem 2rem 2rem;
            background: #16181f;
            border: 1px solid #2a2d3a;
            border-radius: 12px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.5);
        }

        .login-logo {
            font-family: 'DM Mono', monospace;
            font-size: 1.1rem;
            font-weight: 500;
            color: #4f8ef7;
            letter-spacing: 0.04em;
            margin-bottom: 0.25rem;
        }

        .login-title {
            font-size: 1.45rem;
            font-weight: 600;
            color: #e8eaf0;
            margin-bottom: 0.2rem;
        }

        .login-sub {
            font-size: 0.8rem;
            color: #5a5f72;
            margin-bottom: 1.8rem;
        }

        .stTextInput label {
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            color: #7a8099 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .stTextInput > div > div > input {
            background: #0f1117 !important;
            border: 1px solid #2a2d3a !important;
            border-radius: 6px !important;
            color: #e8eaf0 !important;
            font-size: 0.875rem !important;
            padding: 0.5rem 0.75rem !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #4f8ef7 !important;
            box-shadow: 0 0 0 2px rgba(79,142,247,0.15) !important;
        }

        .stFormSubmitButton > button {
            width: 100% !important;
            background: #4f8ef7 !important;
            color: #fff !important;
            border: none !important;
            border-radius: 6px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            padding: 0.55rem 1rem !important;
            margin-top: 0.5rem !important;
            transition: background 0.2s !important;
        }

        .stFormSubmitButton > button:hover {
            background: #3a7be8 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrap">
        <div class="login-logo">◈ DATAPORTAL</div>
        <div class="login-title">Sign in</div>
        <div class="login-sub">Authorized personnel only</div>
    </div>
    """, unsafe_allow_html=True)

    # Use columns to center the form tightly
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

        if submitted:
            if check_login(username, password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")


# ── STOP HERE IF NOT LOGGED IN ───────────────────────────────────────────────
if not st.session_state.authenticated:
    login_page()
    st.stop()


# ── Professional CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── App background ── */
    .stApp {
        background: #0f1117;
        color: #c8cad6;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #13151d !important;
        border-right: 1px solid #1e2130 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.82rem !important;
        color: #7a8099 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 0.82rem;
        color: #7a8099;
    }

    /* ── Hide default header ── */
    #MainMenu, footer { visibility: hidden; }

    /* ── Page header style ── */
    .page-header {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        margin-bottom: 1.75rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #1e2130;
    }

    .page-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #e8eaf0;
        letter-spacing: -0.01em;
    }

    .page-badge {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        color: #4f8ef7;
        background: rgba(79,142,247,0.1);
        border: 1px solid rgba(79,142,247,0.2);
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ── Form labels ── */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        font-size: 0.72rem !important;
        font-weight: 500 !important;
        color: #5a5f72 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: #13151d !important;
        border: 1px solid #1e2130 !important;
        border-radius: 6px !important;
        color: #c8cad6 !important;
        font-size: 0.875rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #4f8ef7 !important;
        box-shadow: 0 0 0 2px rgba(79,142,247,0.12) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: #13151d !important;
        border: 1px solid #1e2130 !important;
        border-radius: 6px !important;
        color: #c8cad6 !important;
    }

    /* ── Buttons ── */
    .stFormSubmitButton > button,
    .stButton > button {
        background: #1e2130 !important;
        color: #c8cad6 !important;
        border: 1px solid #2a2d3a !important;
        border-radius: 6px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.15s !important;
    }

    .stFormSubmitButton > button:hover,
    .stButton > button:hover {
        background: #2a2d3a !important;
        border-color: #4f8ef7 !important;
        color: #e8eaf0 !important;
    }

    /* Primary submit gets accent color */
    .stFormSubmitButton > button[kind="primaryFormSubmit"],
    .stFormSubmitButton > button[data-testid="baseButton-primaryFormSubmit"] {
        background: #4f8ef7 !important;
        border-color: #4f8ef7 !important;
        color: #fff !important;
    }

    .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover {
        background: #3a7be8 !important;
    }

    /* ── Record card ── */
    .record-card {
        background: #13151d;
        border: 1px solid #1e2130;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.15s;
    }

    .record-card:hover {
        border-color: #2a2d3a;
    }

    .record-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e8eaf0;
        margin-bottom: 0.2rem;
    }

    .record-meta {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: #5a5f72;
    }

    .badge {
        display: inline-block;
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        padding: 2px 7px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .badge-active   { background: rgba(52,199,89,0.12);  color: #34c759; border: 1px solid rgba(52,199,89,0.2); }
    .badge-inactive { background: rgba(255,69,58,0.1);   color: #ff453a; border: 1px solid rgba(255,69,58,0.2); }
    .badge-pending  { background: rgba(255,159,10,0.1);  color: #ff9f0a; border: 1px solid rgba(255,159,10,0.2); }

    .badge-customer { background: rgba(79,142,247,0.1);  color: #4f8ef7; border: 1px solid rgba(79,142,247,0.2); }
    .badge-lead     { background: rgba(175,82,222,0.1);  color: #af52de; border: 1px solid rgba(175,82,222,0.2); }
    .badge-partner  { background: rgba(52,199,89,0.1);   color: #34c759; border: 1px solid rgba(52,199,89,0.2); }
    .badge-vendor   { background: rgba(255,159,10,0.1);  color: #ff9f0a; border: 1px solid rgba(255,159,10,0.2); }
    .badge-other    { background: rgba(90,95,114,0.15);  color: #7a8099; border: 1px solid #2a2d3a; }

    /* ── Stat cards ── */
    .stat-card {
        background: #13151d;
        border: 1px solid #1e2130;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
    }

    .stat-label {
        font-size: 0.7rem;
        font-weight: 500;
        color: #5a5f72;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.35rem;
    }

    .stat-value {
        font-family: 'DM Mono', monospace;
        font-size: 2rem;
        font-weight: 500;
        color: #e8eaf0;
        line-height: 1;
    }

    .stat-sub {
        font-size: 0.75rem;
        color: #5a5f72;
        margin-top: 0.3rem;
    }

    /* ── Divider ── */
    hr {
        border-color: #1e2130 !important;
    }

    /* ── Metrics override ── */
    [data-testid="stMetric"] {
        background: #13151d;
        border: 1px solid #1e2130;
        border-radius: 8px;
        padding: 1rem 1.25rem;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #5a5f72 !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'DM Mono', monospace !important;
        color: #e8eaf0 !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #13151d !important;
        border: 1px solid #1e2130 !important;
        border-radius: 6px !important;
    }

    [data-testid="stExpander"] summary {
        font-size: 0.8rem !important;
        color: #7a8099 !important;
    }

    /* ── Alerts ── */
    .stSuccess > div {
        background: rgba(52,199,89,0.08) !important;
        border: 1px solid rgba(52,199,89,0.2) !important;
        color: #34c759 !important;
        border-radius: 6px !important;
    }

    .stWarning > div {
        background: rgba(255,159,10,0.08) !important;
        border: 1px solid rgba(255,159,10,0.2) !important;
        color: #ff9f0a !important;
        border-radius: 6px !important;
    }

    .stError > div {
        background: rgba(255,69,58,0.08) !important;
        border: 1px solid rgba(255,69,58,0.2) !important;
        color: #ff453a !important;
        border-radius: 6px !important;
    }

    /* ── Sidebar nav ── */
    .sidebar-logo {
        font-family: 'DM Mono', monospace;
        font-size: 0.9rem;
        font-weight: 500;
        color: #4f8ef7;
        letter-spacing: 0.06em;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #1e2130;
    }

    .sidebar-section {
        font-size: 0.65rem;
        font-weight: 500;
        color: #3a3f52;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Supabase connection ───────────────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("Missing Supabase credentials")
        st.stop()

    return create_client(url, key)


def get_client():
    return get_supabase()


# ── DB helpers ────────────────────────────────────────────────────────────────
def insert_record(client, data: dict):
    return client.table("records").insert(data).execute()


def fetch_all(client):
    return client.table("records").select("*").order("created_at", desc=True).execute()


def search_records(client, query: str, field: str):
    col = field.lower().replace(" ", "_")
    return (
        client.table("records")
        .select("*")
        .ilike(col, f"%{query}%")
        .order("created_at", desc=True)
        .execute()
    )


def delete_record(client, record_id: int):
    return client.table("records").delete().eq("id", record_id).execute()


def update_record(client, record_id: int, data: dict):
    return client.table("records").update(data).eq("id", record_id).execute()


# ── Badge helpers ─────────────────────────────────────────────────────────────
def status_badge(status):
    cls = f"badge badge-{status.lower()}"
    return f'<span class="{cls}">{status}</span>'


def category_badge(cat):
    cls = f"badge badge-{cat.lower()}"
    return f'<span class="{cls}">{cat}</span>'


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">◈ DATAPORTAL</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "",
        ["➕ Add Record", "🔍 Search & Browse", "📊 Stats"],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown(
        '<div style="font-size:0.65rem;color:#3a3f52;margin-top:1rem;font-family:\'DM Mono\',monospace;">v1.0.0 · Internal</div>',
        unsafe_allow_html=True,
    )


client = get_client()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ADD RECORD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "➕ Add Record":
    st.markdown("""
    <div class="page-header">
        <span class="page-title">New Record</span>
        <span class="page-badge">Entry</span>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_spacer = st.columns([1.8, 1])

    with col_form:
        with st.form("entry_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
            with c2:
                email = st.text_input("Email *")

            c3, c4 = st.columns(2)
            with c3:
                category = st.selectbox("Category", ["Customer", "Lead", "Partner", "Vendor", "Other"])
            with c4:
                status = st.selectbox("Status", ["Active", "Inactive", "Pending"])

            description = st.text_area("Description", height=100)

            submitted = st.form_submit_button("Save Record", use_container_width=True)

        if submitted:
            if not name or not email:
                st.warning("Name and Email are required fields.")
            else:
                insert_record(client, {
                    "name": name,
                    "email": email,
                    "category": category,
                    "status": status,
                    "description": description,
                })
                st.success("Record saved successfully.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SEARCH & BROWSE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search & Browse":
    st.markdown("""
    <div class="page-header">
        <span class="page-title">Records</span>
        <span class="page-badge">Browse</span>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns([3, 1])
    with sc1:
        search_query = st.text_input("Search", placeholder="Search records…", label_visibility="collapsed")
    with sc2:
        search_field = st.selectbox("Field", ["Name", "Email", "Category", "Status"], label_visibility="collapsed")

    if search_query:
        result = search_records(client, search_query, search_field)
        records = result.data
    else:
        records = fetch_all(client).data

    st.markdown(
        f'<div style="font-size:0.72rem;color:#5a5f72;margin-bottom:1rem;font-family:\'DM Mono\',monospace;">'
        f'{len(records)} record{"s" if len(records) != 1 else ""} found</div>',
        unsafe_allow_html=True,
    )

    if records:
        for r in records:
            with st.container():
                st.markdown(f"""
                <div class="record-card">
                    <div class="record-name">{r['name']}</div>
                    <div class="record-meta" style="margin-bottom:0.5rem">{r['email']}</div>
                    <div style="display:flex;gap:0.4rem;flex-wrap:wrap">
                        {category_badge(r['category'])}
                        {status_badge(r['status'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Edit record"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        new_name = st.text_input("Name", r["name"], key=f"n{r['id']}")
                    with ec2:
                        new_email = st.text_input("Email", r["email"], key=f"e{r['id']}")

                    ec3, ec4 = st.columns(2)
                    with ec3:
                        cat_opts = ["Customer", "Lead", "Partner", "Vendor", "Other"]
                        new_cat = st.selectbox("Category", cat_opts,
                                               index=cat_opts.index(r["category"]) if r["category"] in cat_opts else 0,
                                               key=f"c{r['id']}")
                    with ec4:
                        st_opts = ["Active", "Inactive", "Pending"]
                        new_status = st.selectbox("Status", st_opts,
                                                  index=st_opts.index(r["status"]) if r["status"] in st_opts else 0,
                                                  key=f"s{r['id']}")

                    new_desc = st.text_area("Description", r.get("description", ""), key=f"desc{r['id']}", height=80)

                    btn1, btn2, _ = st.columns([1, 1, 3])
                    with btn1:
                        if st.button("Update", key=f"u{r['id']}"):
                            update_record(client, r["id"], {
                                "name": new_name,
                                "email": new_email,
                                "category": new_cat,
                                "status": new_status,
                                "description": new_desc,
                            })
                            st.rerun()
                    with btn2:
                        if st.button("Delete", key=f"d{r['id']}"):
                            delete_record(client, r["id"])
                            st.rerun()
    else:
        st.markdown(
            '<div style="text-align:center;padding:3rem;color:#3a3f52;font-size:0.85rem;">No records found.</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — STATS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Stats":
    st.markdown("""
    <div class="page-header">
        <span class="page-title">Overview</span>
        <span class="page-badge">Stats</span>
    </div>
    """, unsafe_allow_html=True)

    records = fetch_all(client).data

    total = len(records)
    active = sum(1 for r in records if r["status"] == "Active")
    inactive = sum(1 for r in records if r["status"] == "Inactive")
    pending = sum(1 for r in records if r["status"] == "Pending")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Records</div>
            <div class="stat-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Active</div>
            <div class="stat-value" style="color:#34c759">{active}</div>
            <div class="stat-sub">{round(active/total*100) if total else 0}% of total</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Inactive</div>
            <div class="stat-value" style="color:#ff453a">{inactive}</div>
            <div class="stat-sub">{round(inactive/total*100) if total else 0}% of total</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Pending</div>
            <div class="stat-value" style="color:#ff9f0a">{pending}</div>
            <div class="stat-sub">{round(pending/total*100) if total else 0}% of total</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Category breakdown
    st.markdown('<div class="sidebar-section" style="color:#5a5f72;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.75rem">By Category</div>', unsafe_allow_html=True)

    categories = ["Customer", "Lead", "Partner", "Vendor", "Other"]
    cols = st.columns(len(categories))
    for col, cat in zip(cols, categories):
        count = sum(1 for r in records if r.get("category") == cat)
        with col:
            st.markdown(f"""
            <div class="stat-card" style="text-align:center">
                <div style="margin-bottom:0.4rem">{category_badge(cat)}</div>
                <div class="stat-value" style="font-size:1.4rem">{count}</div>
            </div>
            """, unsafe_allow_html=True)
