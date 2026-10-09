import streamlit as st
import pandas as pd
from pathlib import Path
from urllib.parse import quote
import html

st.set_page_config(
    page_title="Eastern Cape Hydrogen Stakeholder Map",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DATA = ROOT / "data"

@st.cache_data
def load_data():
    people = pd.read_csv(DATA / "stakeholders.csv").fillna("")
    sources = pd.read_csv(DATA / "sources.csv").fillna("")
    return people, sources

base_people, sources = load_data()
if "people" not in st.session_state:
    st.session_state.people = base_people.copy()
people = st.session_state.people

def truth(v):
    return str(v).strip().upper() in {"TRUE", "YES", "1"}

def esc(v):
    return html.escape(str(v if v is not None else ""))

def person(pid):
    hit = people[people["id"].astype(str) == str(pid)]
    return None if hit.empty else hit.iloc[0].to_dict()

def person_sources(pid):
    return sources[sources["stakeholder_id"].astype(str) == str(pid)]

def url_for(pid):
    return f"?person={quote(str(pid))}"

st.markdown("""
<style>
:root{--ink:#18212b;--muted:#6c7886;--navy:#17365d;--blue:#2f5597;--line:#dbe3ec;--soft:#f6f8fb;--amber:#8a6400;--amberbg:#fff7df;--green:#235d43;--greenbg:#edf8f2}
.block-container{max-width:1450px;padding-top:1.15rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#f8fafc;border-right:1px solid #e7ebf0}
h1,h2,h3{letter-spacing:-.025em}
.hero{border:1px solid var(--line);border-radius:16px;padding:23px 25px;background:linear-gradient(135deg,#fff 0%,#f2f6fa 100%);box-shadow:0 3px 16px rgba(23,54,93,.05);margin-bottom:18px}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}
.hero-title{font-size:29px;font-weight:780;color:var(--ink);margin-top:4px}.hero-copy{font-size:14px;color:var(--muted);max-width:900px;margin-top:5px;line-height:1.45}
.org-shell{border:1px solid var(--line);border-radius:16px;background:white;padding:22px 24px;box-shadow:0 3px 16px rgba(23,54,93,.05)}
.org-label{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8290a0;margin:6px 0 9px}.org-row{display:flex;gap:13px;justify-content:center;align-items:stretch;flex-wrap:wrap;margin:8px 0}.org-arrow{text-align:center;color:#9ca8b5;font-size:21px;line-height:1;margin:5px 0}.divider{height:1px;background:#e8edf2;margin:18px 0}
.person-card{display:flex;flex-direction:column;justify-content:center;width:235px;min-height:72px;border:1px solid #d4dee8;border-radius:10px;padding:12px 14px;background:#fbfcfe;text-decoration:none!important;color:var(--ink)!important;box-shadow:0 1px 2px rgba(18,30,45,.03);transition:.12s ease}.person-card:hover{transform:translateY(-1px);border-color:#7f9fc3;background:#f0f5fa;box-shadow:0 5px 14px rgba(23,54,93,.09)}.person-card.primary{background:var(--navy);border-color:var(--navy)}.person-card.primary .pc-name,.person-card.primary .pc-role,.person-card.primary .pc-org{color:white}.person-card.soft{background:#edf4fb}.pc-name{font-size:14px;font-weight:760;color:#20344b}.pc-role{font-size:12px;color:#4f6072;margin-top:3px;line-height:1.25}.pc-org{font-size:10px;color:#8290a0;margin-top:5px;text-transform:uppercase;letter-spacing:.05em}.review-dot{display:inline-block;width:7px;height:7px;background:#c18400;border-radius:50%;margin-right:5px}
.profile-head{border:1px solid var(--line);border-radius:15px;padding:20px 22px;background:#fff;box-shadow:0 3px 14px rgba(23,54,93,.05);margin-bottom:14px}.profile-name{font-size:30px;font-weight:790;color:var(--ink);letter-spacing:-.03em}.profile-role{font-size:15px;color:var(--blue);font-weight:650;margin-top:3px}.profile-org{font-size:12px;color:var(--muted);margin-top:3px}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:15px}.kpi{border:1px solid var(--line);background:#fafbfd;border-radius:10px;padding:10px 12px}.k-label{font-size:10px;color:#7d8997;text-transform:uppercase;letter-spacing:.07em;font-weight:700}.k-val{font-size:13px;color:#27384b;font-weight:650;margin-top:3px}
.section{border:1px solid var(--line);border-radius:12px;padding:15px 17px;background:white;margin-bottom:12px}.section-title{font-size:10px;color:var(--blue);font-weight:800;text-transform:uppercase;letter-spacing:.09em;margin-bottom:7px}.section-body{font-size:14px;color:#283645;line-height:1.52}.good,.warn{border-radius:9px;padding:9px 11px;font-size:12px;margin:8px 0 14px}.good{background:var(--greenbg);border:1px solid #cfe9db;color:var(--green)}.warn{background:var(--amberbg);border:1px solid #ead89e;color:#745400}.source{border-bottom:1px solid #edf0f4;padding:8px 0}.source:last-child{border-bottom:none}.source-type{font-size:10px;color:#8491a0;text-transform:uppercase;letter-spacing:.05em}.hit{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:8px;background:white}.small{font-size:12px;color:var(--muted)}.edit-note{background:#f4f7fa;border:1px solid #dbe3ec;border-radius:9px;padding:10px 12px;color:#566575;font-size:12px}
@media(max-width:900px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.person-card{width:100%}}
</style>
""", unsafe_allow_html=True)

def card(pid, css=""):
    p = person(pid)
    if not p:
        return ""
    review = '<span class="review-dot"></span>' if truth(p.get("needs_review", "")) else ""
    return (f'<a class="person-card {css}" href="{url_for(pid)}">'
            f'<div class="pc-name">{review}{esc(p["name"])}</div>'
            f'<div class="pc-role">{esc(p["role"])}</div>'
            f'<div class="pc-org">{esc(p["organisation"])}</div></a>')

def row(ids, styles=None):
    styles = styles or {}
    return '<div class="org-row">' + ''.join(card(pid, styles.get(pid,"")) for pid in ids if person(pid)) + '</div>'

def section(title, text):
    body = esc(text) if str(text).strip() else "—"
    st.markdown(f'<div class="section"><div class="section-title">{esc(title)}</div><div class="section-body">{body}</div></div>', unsafe_allow_html=True)

def save_updates(pid, updates):
    idx = st.session_state.people.index[st.session_state.people["id"].astype(str) == str(pid)]
    if len(idx):
        i = idx[0]
        for k,v in updates.items():
            if k in st.session_state.people.columns:
                st.session_state.people.at[i,k] = v

# Sidebar
with st.sidebar:
    st.markdown("### Eastern Cape Hydrogen")
    st.caption("Stakeholder intelligence · V1")
    nav = st.radio("Navigate", ["Dashboard", "Directory"], label_visibility="collapsed")
    st.divider()
    q = st.text_input("Search profiles", placeholder="Name, role, organisation…")
    if q:
        cols=["name","role","organisation","category","hydrogen_relevance","mandate_or_public_focus"]
        mask=people[cols].astype(str).apply(lambda c:c.str.contains(q,case=False,na=False)).any(axis=1)
        hits=people[mask].head(8)
        st.caption(f"{len(hits)} result(s)")
        for _,r in hits.iterrows():
            st.markdown(f'**[{r["name"]}]({url_for(r["id"])})**  \n<span class="small">{esc(r["role"])} · {esc(r["organisation"])}</span>', unsafe_allow_html=True)
    st.divider()
    flagged=int(people["needs_review"].astype(str).str.upper().eq("TRUE").sum())
    st.caption("Data quality")
    st.write(f"**{len(people)}** profiles")
    st.write(f"**{people.organisation.nunique()}** organisations")
    st.write(f"**{flagged}** flagged for review")
    st.download_button("Download edited database",st.session_state.people.to_csv(index=False).encode("utf-8"),"stakeholders_updated.csv","text/csv",use_container_width=True)
    st.caption("V1 edits are session-based. Download the CSV to preserve them.")

# Profile route
pid = st.query_params.get("person", "")
p = person(pid) if pid else None
if p:
    st.markdown(f'''<div class="profile-head"><div class="eyebrow">{esc(p["sphere"])} · {esc(p["category"])}</div><div class="profile-name">{esc(p["name"])}</div><div class="profile-role">{esc(p["role"])}</div><div class="profile-org">{esc(p["organisation"])}</div><div class="kpis"><div class="kpi"><div class="k-label">Influence</div><div class="k-val">{esc(p["influence"])}</div></div><div class="kpi"><div class="k-label">Evidence confidence</div><div class="k-val">{esc(p["confidence"])}</div></div><div class="kpi"><div class="k-label">Last verified</div><div class="k-val">{esc(p["last_verified"])}</div></div><div class="kpi"><div class="k-label">Public sources</div><div class="k-val">{len(person_sources(p["id"]))}</div></div></div></div>''', unsafe_allow_html=True)

    b1,b2=st.columns([1,5])
    with b1:
        if st.button("← Dashboard", use_container_width=True):
            st.query_params.clear(); st.rerun()
    with b2:
        if st.button("✎ Edit profile / add notes"):
            st.session_state["editing_person"] = p["id"]

    if truth(p.get("needs_review","")):
        st.markdown('<div class="warn"><b>Needs review.</b> Reconfirm the role or source evidence before formal engagement.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="good"><b>Current profile.</b> No review flag is set. Re-check critical appointments before major engagements.</div>', unsafe_allow_html=True)

    if st.session_state.get("editing_person") == p["id"]:
        with st.expander("Edit this profile", expanded=True):
            st.markdown('<div class="edit-note">For V1, Save updates this session only. Use <b>Download edited database</b> in the sidebar to preserve changes. Persistent saving can be added later if this interface proves useful.</div>', unsafe_allow_html=True)
            with st.form("edit_profile"):
                c1,c2=st.columns(2)
                role=c1.text_input("Role",p["role"])
                org=c2.text_input("Organisation",p["organisation"])
                qualifications=st.text_area("Qualifications",p["qualifications"],height=90)
                background=st.text_area("Professional background",p["background"],height=110)
                focus=st.text_area("Mandate / public focus",p["mandate_or_public_focus"],height=100)
                relevance=st.text_area("Hydrogen relevance",p["hydrogen_relevance"],height=100)
                engagement=st.text_area("Engagement route",p["engagement_route"],height=100)
                st.markdown("#### Your working information")
                opts=["","Not yet engaged","Intro made","Active relationship","Follow-up due","Dormant"]
                cur=p.get("relationship_status","")
                status=st.selectbox("Relationship status",opts,index=opts.index(cur) if cur in opts else 0)
                last=st.text_input("Last interaction",p.get("last_interaction",""),placeholder="e.g. 9 Oct 2026 — onboarding meeting")
                next_action=st.text_input("Next action",p.get("next_action",""))
                notes=st.text_area("Working notes",p.get("private_notes",""),height=110)
                needs_review=st.checkbox("Flag profile for review",value=truth(p.get("needs_review","")))
                if st.form_submit_button("Save changes",type="primary"):
                    save_updates(p["id"],{"role":role,"organisation":org,"qualifications":qualifications,"background":background,"mandate_or_public_focus":focus,"hydrogen_relevance":relevance,"engagement_route":engagement,"relationship_status":status,"last_interaction":last,"next_action":next_action,"private_notes":notes,"needs_review":"TRUE" if needs_review else "FALSE"})
                    st.session_state["editing_person"]=""
                    st.success("Saved for this session.")
                    st.rerun()

    st.markdown("### Profile")
    left,right=st.columns([1.05,.95])
    with left:
        section("Hydrogen relevance",p["hydrogen_relevance"])
        section("Mandate / public focus",p["mandate_or_public_focus"])
        section("Qualifications",p["qualifications"])
    with right:
        section("Professional background",p["background"])
        section("Engagement route",p["engagement_route"])
        if p.get("reports_to") and person(p["reports_to"]):
            st.markdown('<div class="section-title">Formal / structural route</div>', unsafe_allow_html=True)
            st.markdown(card(p["reports_to"],"soft"), unsafe_allow_html=True)

    if any(str(p.get(k,"")).strip() for k in ["relationship_status","last_interaction","next_action","private_notes"]):
        st.markdown("### Your working notes")
        n1,n2=st.columns(2)
        with n1:
            section("Relationship status",p.get("relationship_status","")); section("Last interaction",p.get("last_interaction",""))
        with n2:
            section("Next action",p.get("next_action","")); section("Notes",p.get("private_notes",""))

    st.markdown("### Public sources")
    ps=person_sources(p["id"])
    if ps.empty: st.info("No public source is currently attached to this profile.")
    else:
        for _,s in ps.iterrows():
            st.markdown(f'<div class="source"><a href="{esc(s["url"])}" target="_blank"><b>{esc(s["label"])}</b></a><div class="source-type">{esc(s["source_type"])} · checked {esc(s["checked_on"])}</div></div>', unsafe_allow_html=True)

    with st.expander("Data quality details"):
        st.write("**Confidence:**",p["confidence"]); st.write("**Last verified:**",p["last_verified"]); st.write("**Needs review:**","Yes" if truth(p["needs_review"]) else "No"); st.write("**Source count:**",len(ps))
        st.caption("Public facts/source-backed activity are kept separate from analytical fields such as hydrogen relevance and engagement route.")
    st.stop()

# Dashboard
if nav == "Dashboard":
    st.markdown('''<div class="hero"><div class="eyebrow">Eastern Cape · Green hydrogen / strategic energy</div><div class="hero-title">Stakeholder intelligence dashboard</div><div class="hero-copy">Click a person to open their profile. Search from the sidebar to jump directly to anyone. The visual map stays deliberately focused on the provincial delivery chain; the wider ecosystem remains searchable below.</div></div>''', unsafe_allow_html=True)
    st.markdown('<div class="org-shell">', unsafe_allow_html=True)
    st.markdown('<div class="org-label">Provincial apex</div>', unsafe_allow_html=True)
    st.markdown(row(["mabuyane"],{"mabuyane":"primary"}), unsafe_allow_html=True)
    st.markdown('<div class="org-arrow">↓</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="org-label">DEDEAT · Political & administrative chain</div>', unsafe_allow_html=True)
        st.markdown(row(["pieters"],{"pieters":"soft"}), unsafe_allow_html=True); st.markdown('<div class="org-arrow">↓</div>', unsafe_allow_html=True)
        st.markdown(row(["mama"],{"mama":"soft"}), unsafe_allow_html=True); st.markdown('<div class="org-arrow">↓</div>', unsafe_allow_html=True)
        st.markdown(row(["booi","jongile"]), unsafe_allow_html=True); st.markdown('<div class="org-arrow">↓</div>', unsafe_allow_html=True)
        st.markdown(row(["mcmaster","lazarus"]), unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="org-label">Office of the Premier · Coordination / escalation</div>', unsafe_allow_html=True)
        st.markdown(row(["sogoni"],{"sogoni":"soft"}), unsafe_allow_html=True); st.markdown('<div class="org-arrow">↓</div>', unsafe_allow_html=True)
        st.markdown(row(["qwase"]), unsafe_allow_html=True)
        st.markdown('<div class="divider"></div><div class="org-label">Transversal provincial interfaces</div>', unsafe_allow_html=True)
        st.markdown(row(["mvoko","williams","lusithi","nqatha"]), unsafe_allow_html=True)
    st.markdown('<div class="divider"></div><div class="org-label">Delivery & implementation interfaces</div>', unsafe_allow_html=True)
    st.markdown(row(["koza","zweni","wakaba","mosana","tinta"]), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Wider ecosystem")
    st.caption("Kept outside the main organogram so the front page stays readable.")
    t1,t2,t3=st.tabs(["Municipalities","National government","Grid / ports / finance"])
    with t1: st.markdown(row(["faku","yawa","ntsasela","ncokazi","mqoqi","lobishe","kamana","mnqokoyi"]), unsafe_allow_html=True)
    with t2: st.markdown(row(["ramokgopa","pillay","tau","hamilton","majodina","phillips","creecy","mokonyama","maynier","tshabalala","nzimande","cele","godongwana","pieterse","baleni"]), unsafe_allow_html=True)
    with t3: st.markdown(row(["bala","abdool","lekhethe","mosako","fyfe"]), unsafe_allow_html=True)

    st.markdown("### Data quality snapshot")
    a,b,c,d=st.columns(4); a.metric("Profiles",len(people)); b.metric("Organisations",people.organisation.nunique()); c.metric("Public sources",len(sources)); d.metric("Review flags",flagged)
    st.caption("Review flags are intentional: they show where current public evidence is thinner or a role may need reconfirmation.")

else:
    st.markdown('''<div class="hero"><div class="eyebrow">Directory</div><div class="hero-title">Search the stakeholder ecosystem</div><div class="hero-copy">Filter the wider database without crowding the visual organogram.</div></div>''', unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    sphere=f1.selectbox("Sphere",["All"]+sorted(people.sphere.unique().tolist()))
    org=f2.selectbox("Organisation",["All"]+sorted(people.organisation.unique().tolist()))
    cat=f3.selectbox("Category",["All"]+sorted(people.category.unique().tolist()))
    search=st.text_input("Search directory",placeholder="e.g. water, investment, grid, Coega…")
    df=people.copy()
    if sphere!="All": df=df[df.sphere==sphere]
    if org!="All": df=df[df.organisation==org]
    if cat!="All": df=df[df.category==cat]
    if search:
        cols=["name","role","organisation","category","hydrogen_relevance","mandate_or_public_focus","engagement_route"]
        mask=df[cols].astype(str).apply(lambda c:c.str.contains(search,case=False,na=False)).any(axis=1); df=df[mask]
    for _,r in df.iterrows():
        flag=" · ⚠ review" if truth(r["needs_review"]) else ""
        st.markdown(f'<div class="hit"><a href="{url_for(r["id"])}"><b>{esc(r["name"])}</b></a><div class="small">{esc(r["role"])} · {esc(r["organisation"])}{flag}</div><div class="small" style="margin-top:5px">{esc(r["hydrogen_relevance"])}</div></div>', unsafe_allow_html=True)
