import streamlit as st
from supabase import create_client, Client
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Entry App",
    page_icon="📋",
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
    st.title("🔐 Login Required")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if check_login(username, password):
            st.session_state.authenticated = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")


# ── STOP HERE IF NOT LOGGED IN ───────────────────────────────────────────────
if not st.session_state.authenticated:
    login_page()
    st.stop()


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .stTextInput > div > div > input { border-radius: 8px; }
    .stTextArea textarea { border-radius: 8px; }
    .stSelectbox > div > div { border-radius: 8px; }
    .record-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .tag {
        background: #e8f0fe;
        color: #1a73e8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 500;
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


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📋 Data Entry App")

    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.divider()

    page = st.radio(
        "Navigate",
        ["➕ Add Record", "🔍 Search & Browse", "📊 Stats"],
    )


client = get_client()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1
# ═══════════════════════════════════════════════════════════════════════════════
if page == "➕ Add Record":
    st.header("➕ Add New Record")

    with st.form("entry_form", clear_on_submit=True):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        category = st.selectbox("Category", ["Customer", "Lead", "Partner", "Vendor", "Other"])
        status = st.selectbox("Status", ["Active", "Inactive", "Pending"])
        description = st.text_area("Description")

        submitted = st.form_submit_button("Save")

    if submitted:
        if not name or not email:
            st.warning("Name and Email required")
        else:
            insert_record(client, {
                "name": name,
                "email": email,
                "category": category,
                "status": status,
                "description": description,
            })
            st.success("Saved")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search & Browse":
    st.header("Search")

    search_query = st.text_input("Search")
    search_field = st.selectbox("Field", ["Name", "Email", "Category", "Status"])

    if search_query:
        result = search_records(client, search_query, search_field)
        records = result.data
    else:
        records = fetch_all(client).data

    if records:
        for r in records:
            st.write(f"{r['name']} | {r['email']} | {r['category']} | {r['status']}")

            with st.expander("Edit"):
                new_name = st.text_input("Name", r["name"], key=f"n{r['id']}")
                new_email = st.text_input("Email", r["email"], key=f"e{r['id']}")

                if st.button("Update", key=f"u{r['id']}"):
                    update_record(client, r["id"], {
                        "name": new_name,
                        "email": new_email,
                        "category": r["category"],
                        "status": r["status"],
                        "description": r.get("description", ""),
                    })
                    st.rerun()

                if st.button("Delete", key=f"d{r['id']}"):
                    delete_record(client, r["id"])
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Stats":
    st.header("Stats")

    records = fetch_all(client).data

    total = len(records)
    active = sum(1 for r in records if r["status"] == "Active")

    st.metric("Total", total)
    st.metric("Active", active)
