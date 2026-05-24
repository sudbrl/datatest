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

# ── Custom CSS ────────────────────────────────────────────────────────────────
# Moved CSS up so it applies to the login screen as well
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .stTextInput > div > div > input { border-radius: 8px; }
    .stTextArea textarea { border-radius: 8px; }
    .stSelectbox > div > div { border-radius: 8px; }
    div[data-testid="stForm"] { border-radius: 12px; }
    .record-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .tag {
        background: #e8f0fe;
        color: #1a73e8;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 5px;
    }
    .tag-status {
        background: #e6f4ea;
        color: #1e8e3e;
    }
</style>
""", unsafe_allow_html=True)

# ── SIMPLE LOGIN SYSTEM ──────────────────────────────────────────────────────
def check_login(username, password):
    correct_user = st.secrets.get("APP_USERNAME")
    correct_pass = st.secrets.get("APP_PASSWORD")
    return username == correct_user and password == correct_pass

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # Use columns to make the login box small and centered
    _, col2, _ = st.columns([1, 1.2, 1])
    
    with col2:
        st.write("") # Spacing
        st.write("")
        st.markdown("<h2 style='text-align: center;'>🔐 Secure Login</h2>", unsafe_allow_html=True)
        st.write("")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

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
    st.write("Professional Data Management")
    st.divider()

    page = st.radio(
        "Navigation",
        ["➕ Add Record", "🔍 Search & Browse", "📊 Stats"],
        label_visibility="collapsed"
    )

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

client = get_client()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1
# ═══════════════════════════════════════════════════════════════════════════════
if page == "➕ Add Record":
    st.header("➕ Add New Record")
    st.markdown("Fill out the details below to add a new entity to the database.")

    with st.form("entry_form", clear_on_submit=True):
        # Two-column layout for professional form appearance
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            category = st.selectbox("Category", ["Customer", "Lead", "Partner", "Vendor", "Other"])
        with col2:
            email = st.text_input("Email *")
            status = st.selectbox("Status", ["Active", "Inactive", "Pending"])
        
        description = st.text_area("Description")

        st.write("") # Spacing
        submitted = st.form_submit_button("💾 Save Record", type="primary")

    if submitted:
        if not name or not email:
            st.warning("⚠️ Name and Email are required fields.")
        else:
            insert_record(client, {
                "name": name,
                "email": email,
                "category": category,
                "status": status,
                "description": description,
            })
            st.success(f"✅ Record for **{name}** saved successfully!")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search & Browse":
    st.header("🔍 Search & Browse")

    # Search bar layout
    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        search_query = st.text_input("Search query", placeholder="Search records...", label_visibility="collapsed")
    with s_col2:
        search_field = st.selectbox("Field", ["Name", "Email", "Category", "Status"], label_visibility="collapsed")

    st.divider()

    if search_query:
        result = search_records(client, search_query, search_field)
        records = result.data
    else:
        records = fetch_all(client).data

    if records:
        for r in records:
            # Professional Card UI
            st.markdown(f"""
            <div class="record-card">
                <div>
                    <h5 style="margin:0; padding:0; color:#333;">{r['name']}</h5>
                    <small style="color:#666;">{r['email']}</small>
                </div>
                <div>
                    <span class="tag">{r['category']}</span>
                    <span class="tag tag-status">{r['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Manage Record"):
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    new_name = st.text_input("Name", r["name"], key=f"n{r['id']}")
                with edit_col2:
                    new_email = st.text_input("Email", r["email"], key=f"e{r['id']}")

                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button("Update Record", key=f"u{r['id']}", use_container_width=True, type="primary"):
                        update_record(client, r["id"], {
                            "name": new_name,
                            "email": new_email,
                            "category": r["category"],
                            "status": r["status"],
                            "description": r.get("description", ""),
                        })
                        st.rerun()
                with btn_col2:
                    if st.button("Delete Record", key=f"d{r['id']}", use_container_width=True):
                        delete_record(client, r["id"])
                        st.rerun()
                st.write("")
    else:
        st.info("No records found matching your criteria.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Stats":
    st.header("📊 Database Statistics")
    st.write("Overview of your current data inventory.")

    records = fetch_all(client).data
    total = len(records)
    active = sum(1 for r in records if r["status"] == "Active")
    pending = sum(1 for r in records if r["status"] == "Pending")
    inactive = total - active - pending

    # Use columns for a professional dashboard look
    st.write("")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Records", total)
    m_col2.metric("Active", active)
    m_col3.metric("Pending", pending)
    m_col4.metric("Inactive", inactive)
    
    st.divider()
