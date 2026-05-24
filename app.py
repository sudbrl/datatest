import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Entry App",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    .record-card:hover { border-color: #4f8bf9; }
    .tag {
        background: #e8f0fe;
        color: #1a73e8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ── Supabase connection (FIXED) ───────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    # Primary: Streamlit secrets
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")

    # Fallback: environment variables (local dev)
    if not url:
        url = os.getenv("SUPABASE_URL")
    if not key:
        key = os.getenv("SUPABASE_KEY")

    # Safety check
    if not url or not key:
        st.error("❌ Missing Supabase credentials. Add them to st.secrets or environment variables.")
        st.stop()

    return create_client(url, key)


def get_client():
    try:
        return get_supabase()
    except Exception as e:
        st.error(f"❌ Could not connect to Supabase: {e}")
        st.stop()


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
    st.caption("Powered by Streamlit + Supabase")
    st.divider()
    page = st.radio(
        "Navigate",
        ["➕ Add Record", "🔍 Search & Browse", "📊 Stats"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Supabase Table:** `records`")
    st.markdown("**Schema fields:**")
    st.code("id, name, email, category,\ndescription, status, created_at", language="text")


client = get_client()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Add Record
# ═══════════════════════════════════════════════════════════════════════════════
if page == "➕ Add Record":
    st.header("➕ Add New Record")

    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. Jane Doe")
            email = st.text_input("Email *", placeholder="e.g. jane@example.com")
        with col2:
            category = st.selectbox(
                "Category *",
                ["Customer", "Lead", "Partner", "Vendor", "Other"],
            )
            status = st.selectbox("Status", ["Active", "Inactive", "Pending"])

        description = st.text_area(
            "Description / Notes",
            placeholder="Any additional information...",
            height=100,
        )

        submitted = st.form_submit_button("💾 Save Record", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip():
            st.warning("⚠️ Name and Email are required.")
        else:
            try:
                insert_record(client, {
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "category": category,
                    "status": status,
                    "description": description.strip(),
                })
                st.success(f"✅ Record for **{name}** saved successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error saving record: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Search & Browse
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search & Browse":
    st.header("🔍 Search & Browse Records")

    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="Type to search...",
            label_visibility="collapsed",
        )
    with col2:
        search_field = st.selectbox(
            "Search by",
            ["Name", "Email", "Category", "Description", "Status"],
            label_visibility="collapsed",
        )
    with col3:
        do_search = st.button("🔍 Search", use_container_width=True)

    st.divider()

    try:
        if search_query and do_search:
            result = search_records(client, search_query, search_field)
            records = result.data
            st.caption(f"Found **{len(records)}** result(s)")
        else:
            result = fetch_all(client)
            records = result.data
            st.caption(f"Showing all **{len(records)}** record(s)")
    except Exception as e:
        st.error(f"❌ Error fetching records: {e}")
        records = []

    if records:
        with st.expander("⚙️ Filter & Sort", expanded=False):
            cat_filter = st.multiselect(
                "Category",
                ["Customer", "Lead", "Partner", "Vendor", "Other"],
            )
            status_filter = st.multiselect(
                "Status",
                ["Active", "Inactive", "Pending"]
            )

            if cat_filter:
                records = [r for r in records if r["category"] in cat_filter]
            if status_filter:
                records = [r for r in records if r["status"] in status_filter]

    if not records:
        st.info("No records found.")
    else:
        for rec in records:
            with st.container():
                st.markdown(f"""
                <div class="record-card">
                    <strong>{rec['name']}</strong>
                    <span class="tag">{rec['category']}</span>
                    <span class="tag">{rec['status']}</span><br>
                    <small>📧 {rec['email']}</small><br>
                    <small>{rec.get('description', '')[:120]}</small><br>
                    <small style="color:#999">🕒 {rec['created_at'][:19].replace('T',' ')}</small>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"Edit / Delete — ID {rec['id']}"):
                    new_name = st.text_input("Name", rec["name"], key=f"name_{rec['id']}")
                    new_email = st.text_input("Email", rec["email"], key=f"email_{rec['id']}")
                    new_desc = st.text_area("Description", rec.get("description", ""), key=f"desc_{rec['id']}")
                    new_cat = st.selectbox(
                        "Category",
                        ["Customer", "Lead", "Partner", "Vendor", "Other"],
                        index=["Customer","Lead","Partner","Vendor","Other"].index(rec["category"]),
                        key=f"cat_{rec['id']}",
                    )
                    new_status = st.selectbox(
                        "Status",
                        ["Active", "Inactive", "Pending"],
                        index=["Active","Inactive","Pending"].index(rec["status"]),
                        key=f"status_{rec['id']}",
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("💾 Save", key=f"save_{rec['id']}"):
                            update_record(client, rec["id"], {
                                "name": new_name,
                                "email": new_email,
                                "category": new_cat,
                                "status": new_status,
                                "description": new_desc,
                            })
                            st.rerun()

                    with c2:
                        if st.button("🗑️ Delete", key=f"del_{rec['id']}"):
                            delete_record(client, rec["id"])
                            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Stats
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Stats":
    st.header("📊 Statistics")

    try:
        records = fetch_all(client).data
    except Exception as e:
        st.error(f"❌ Error fetching records: {e}")
        records = []

    if not records:
        st.info("No records yet.")
    else:
        total = len(records)
        active = sum(1 for r in records if r["status"] == "Active")
        inactive = sum(1 for r in records if r["status"] == "Inactive")
        pending = sum(1 for r in records if r["status"] == "Pending")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", total)
        c2.metric("Active", active)
        c3.metric("Inactive", inactive)
        c4.metric("Pending", pending)