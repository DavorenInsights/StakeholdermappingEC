
import streamlit as st
import pandas as pd
from pathlib import Path
from urllib.parse import quote
import html

st.set_page_config(
    page_title="Eastern Cape Hydrogen Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).parent
DATA = ROOT / "data"

@st.cache_data
def load_all():
    return (
        pd.read_csv(DATA/"stakeholders.csv").fillna(""),
        pd.read_csv(DATA/"sources.csv").fillna(""),
        pd.read_csv(DATA/"relationships.csv").fillna(""),
        pd.read_csv(DATA/"projects.csv").fillna(""),
        pd.read_csv(DATA/"issue_routes.csv").fillna("")
    )

people, sources, relationships, projects, issue_routes = load_all()

st.markdown("""
<style>
.block-container {max-width:1450px;padding-top:1.1rem;padding-bottom:2rem}
h1,h2,h3 {font-family:Arial,sans-serif}
.kicker {font-size:12px;font-weight:700;letter-spacing:.06em;color:#2f5597;margin-bottom:4px}
.card {border:1px solid #dbe3ec;border-radius:6px;padding:14px 16px;background:#fff;margin-bottom:10px}
.person-card {display:block;border:1px solid #cfd9e4;border-radius:5px;padding:11px 13px;background:#f8fafc;text-decoration:none!important;color:#222!important;height:100%}
.person-card:hover {border-color:#2f5597;background:#edf4fb}
.person-card strong {color:#17365d;font-size:14px}
.person-card small {color:#555;font-size:12px}
.premier {background:#17365d!important;color:white!important;border-color:#17365d!important}
.premier strong,.premier small {color:white!important}
.review {padding:8px 11px;background:#fff3cd;border:1px solid #d6b656;border-radius:4px}
.muted {color:#6b7280;font-size:13px}
.route {border-left:4px solid #2f5597;background:#f8fafc;padding:12px 16px;margin:8px 0}
</style>
""", unsafe_allow_html=True)

def truth(v):
    return str(v).strip().upper() in ("TRUE","1","YES")

def get_person(pid):
    h = people[people.id == pid]
    return None if h.empty else h.iloc[0].to_dict()

def profile_url(pid):
    return f"?person={quote(str(pid))}"

def person_html(pid, premier=False):
    p=get_person(pid)
    if not p: return ""
    cls="person-card premier" if premier else "person-card"
    return (
      f'<a class="{cls}" href="{profile_url(pid)}">'
      f'<strong>{html.escape(str(p["name"]))}</strong><br>'
      f'<small>{html.escape(str(p["role"]))}<br>{html.escape(str(p["organisation"]))}</small></a>'
    )

def cards(ids, cols=3, premier_id=None):
    ids=[x for x in ids if get_person(x)]
    for start in range(0,len(ids),cols):
        cc=st.columns(cols)
        for j,pid in enumerate(ids[start:start+cols]):
            cc[j].markdown(person_html(pid, pid==premier_id), unsafe_allow_html=True)

def split_text(x):
    x=str(x or "").strip()
    if not x: return []
    parts=[p.strip() for p in x.replace("•","\n").split("\n") if p.strip()]
    return parts if len(parts)>1 else [x]

def section(title, text):
    st.markdown(f'<div class="kicker">{html.escape(title.upper())}</div>',unsafe_allow_html=True)
    items=split_text(text)
    if len(items)<=1:
        body=html.escape(items[0]) if items else "—"
    else:
        body="<ul>"+"".join(f"<li>{html.escape(i)}</li>" for i in items)+"</ul>"
    st.markdown(f'<div class="card">{body}</div>',unsafe_allow_html=True)

with st.sidebar:
    st.title("EC Hydrogen Intelligence")
    page=st.radio("View",[
        "Dashboard","Stakeholder map","Directory","Issue router",
        "Projects","Relationship tracker","Sources & quality"
    ])
    st.divider()
    st.caption("Public professional profiles + role-based planning analysis. Private working fields are blank by default.")
    if st.button("Clear selected profile"):
        st.query_params.clear()
        st.rerun()

pid=st.query_params.get("person","")
p=get_person(pid) if pid else None

if p:
    st.title(p["name"])
    st.subheader(f'{p["role"]} · {p["organisation"]}')
    a,b,c,d=st.columns(4)
    a.metric("Sphere",p["sphere"])
    b.metric("Influence",p["influence"])
    c.metric("Confidence",p["confidence"])
    d.metric("Last verified",p["last_verified"])
    if truth(p["needs_review"]):
        st.markdown('<div class="review"><b>Needs review.</b> Reconfirm this role before formal engagement.</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        section("Hydrogen relevance",p["hydrogen_relevance"])
        section("Mandate / public focus",p["mandate_or_public_focus"])
        section("Qualifications",p["qualifications"])
    with c2:
        section("Background",p["background"])
        section("Engagement route",p["engagement_route"])
        if p["reports_to"]:
            boss=get_person(p["reports_to"])
            if boss:
                st.markdown("**Reports / escalates structurally toward:**")
                st.markdown(person_html(boss["id"]),unsafe_allow_html=True)
    ps=sources[sources.stakeholder_id==p["id"]]
    if not ps.empty:
        st.markdown("### Public sources")
        for _,s in ps.iterrows():
            st.markdown(f'- [{s["label"]}]({s["url"]}) — {s["source_type"]}')
    st.divider()

if page=="Dashboard":
    st.title("Eastern Cape hydrogen stakeholder intelligence")
    st.caption("A working navigation system for project facilitation—not a replacement for official reporting lines.")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Stakeholders",len(people))
    c2.metric("Organisations",people.organisation.nunique())
    c3.metric("Issue routes",len(issue_routes))
    c4.metric("Profiles needing review",int(people.needs_review.astype(str).str.upper().eq("TRUE").sum()))
    st.markdown("### Core operating logic")
    st.markdown("""
1. **Start with the actual blocker**, not the most senior person.
2. Route it to the **functional owner**.
3. Escalate through DEDEAT / the relevant institution only when the working-level route cannot resolve it.
4. Use **OTP for cross-government coordination**, not routine project management.
5. Keep a record of **owner, action, decision, deadline and last verification date**.
""")
    st.markdown("### Current strategic context")
    st.info("The Eastern Cape Green Hydrogen Strategy positions Coega and ELIDZ as industrial platforms, while the Coega Green Ammonia Project is now in South Africa's first-wave green-hydrogen priority portfolio.")
    st.markdown("### Fast routes")
    for label in ["Grid / transmission","Water","Port / export logistics","Investment / investor facilitation","Cross-government deadlock"]:
        r=issue_routes[issue_routes.issue_type==label].iloc[0]
        st.markdown(f'**{label}:** {r["first_route"]}')

elif page=="Stakeholder map":
    st.title("Stakeholder map")
    st.caption("Click any card to open the profile. This view separates formal authority from delivery interfaces.")
    st.markdown("#### Provincial apex")
    cards(["mabuyane"],1,"mabuyane")
    st.markdown("#### DEDEAT core")
    cards(["pieters","mama","booi"],3)
    cards(["mcmaster","lazarus","jongile"],3)
    st.markdown("#### Office of the Premier / transversal provincial coordination")
    cards(["sogoni","qwase","mvoko","majeke","williams","mlokothi","nqatha","fani","lusithi","penxa"],3)
    st.markdown("#### Provincial delivery entities")
    cards(["koza","zweni","wakaba","mosana","tinta"],3)
    st.markdown("#### Municipal interfaces")
    cards(["faku","yawa","ntsasela","ncokazi","mqoqi","lobishe","kamana","mnqokoyi"],3)
    st.markdown("#### National policy / regulatory interfaces")
    cards(["ramokgopa","pillay","tau","hamilton","majodina","phillips","creecy","mokonyama","maynier","tshabalala","nzimande","cele","godongwana","pieterse","baleni"],3)
    st.markdown("#### Grid, ports and development finance")
    cards(["bala","abdool","lekhethe","mosako","fyfe"],3)

elif page=="Directory":
    st.title("Stakeholder directory")
    f1,f2,f3=st.columns(3)
    sphere=f1.selectbox("Sphere",["All"]+sorted(people.sphere.unique().tolist()))
    org=f2.selectbox("Organisation",["All"]+sorted(people.organisation.unique().tolist()))
    category=f3.selectbox("Category",["All"]+sorted(people.category.unique().tolist()))
    q=st.text_input("Search name, role, organisation, relevance or focus")
    df=people.copy()
    if sphere!="All": df=df[df.sphere==sphere]
    if org!="All": df=df[df.organisation==org]
    if category!="All": df=df[df.category==category]
    if q:
        cols=["name","role","organisation","hydrogen_relevance","mandate_or_public_focus","engagement_route"]
        mask=df[cols].astype(str).apply(lambda c:c.str.contains(q,case=False,na=False)).any(axis=1)
        df=df[mask]
    st.dataframe(df[["name","role","organisation","sphere","category","influence","confidence","last_verified","needs_review"]],hide_index=True,use_container_width=True)
    choice=st.selectbox("Open profile",[""]+df.name.tolist())
    if choice:
        st.query_params["person"]=df[df.name==choice].iloc[0]["id"]
        st.rerun()

elif page=="Issue router":
    st.title("Issue router")
    st.caption("Choose the blocker. The app suggests the route before escalation.")
    issue=st.selectbox("What is stuck?",issue_routes.issue_type.tolist())
    r=issue_routes[issue_routes.issue_type==issue].iloc[0]
    st.markdown(f'<div class="route"><b>Typical signals</b><br>{html.escape(str(r["signals"]))}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="route"><b>1 — Start here</b><br>{html.escape(str(r["first_route"]))}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="route"><b>2 — Provincial / organisational escalation</b><br>{html.escape(str(r["second_route"]))}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="route"><b>3 — National / executive escalation</b><br>{html.escape(str(r["national_escalation"]))}</div>',unsafe_allow_html=True)
    st.info(r["why"])
    st.markdown("### Relevant people")
    ids=[x for x in str(r["key_people"]).split(";") if x]
    cards(ids,3)

elif page=="Projects":
    st.title("Projects and strategic initiatives")
    for _,pr in projects.iterrows():
        with st.expander(f'{pr["project_name"]} — {pr["stage"]}',expanded=pr["project_id"]=="coega_green_ammonia"):
            a,b=st.columns([2,1])
            with a:
                st.markdown(f'**Location:** {pr["location"]}')
                st.markdown(f'**Developer / owner:** {pr["developer"]}')
                st.markdown(f'**Scale:** {pr["scale"]}')
                st.markdown(f'**Next milestone:** {pr["next_milestone"]}')
                st.markdown(f'**Key dependencies:** {pr["key_dependencies"]}')
                st.markdown(f'**Provincial route:** {pr["provincial_route"]}')
            with b:
                st.markdown(f'**Status date:** {pr["status_as_of"]}')
                st.link_button("Open public source",pr["public_source"])

elif page=="Relationship tracker":
    st.title("Relationship tracker")
    st.caption("The public seed data leaves personal engagement fields blank. Use this as your working layer.")
    working=people[["id","name","role","organisation","relationship_status","last_interaction","next_action","private_notes"]].copy()
    edited=st.data_editor(
        working,
        hide_index=True,
        num_rows="fixed",
        use_container_width=True,
        disabled=["id","name","role","organisation"],
        column_config={
            "relationship_status": st.column_config.SelectboxColumn(
                "relationship_status",
                options=["","Not yet engaged","Intro made","Active relationship","Follow-up due","Dormant"]
            )
        }
    )
    st.download_button(
        "Download updated relationship tracker",
        edited.to_csv(index=False).encode("utf-8"),
        "relationship_tracker.csv","text/csv"
    )
    st.warning("On Community Cloud these edits are session-only. Do not rely on them as a shared database yet. For persistent multi-user notes, connect a private database later.")

elif page=="Sources & quality":
    st.title("Sources and data quality")
    st.markdown("### Profiles flagged for review")
    review=people[people.needs_review.astype(str).str.upper()=="TRUE"]
    if review.empty:
        st.success("No profiles are currently flagged.")
    else:
        st.dataframe(review[["name","role","organisation","last_verified","confidence","next_action"]],hide_index=True,use_container_width=True)
    st.markdown("### Public source register")
    st.dataframe(sources,hide_index=True,use_container_width=True)
    st.markdown("### Relationship register")
    st.dataframe(relationships,hide_index=True,use_container_width=True)
    st.caption("A source proves the public role/activity shown; strategic relevance and engagement guidance are analytical fields.")
