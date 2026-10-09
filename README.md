# Eastern Cape Hydrogen Stakeholder Intelligence

This is a lightweight private Streamlit app for navigating the Eastern Cape green-hydrogen / strategic-energy stakeholder ecosystem.

## What is included
- 48 public-professional stakeholder profiles across provincial, municipal, national, SOE and DFI interfaces
- clickable stakeholder map
- searchable directory
- issue-routing tool
- project / strategy tracker
- relationship-tracking working table
- source / verification register
- editable CSV data layer

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy privately on Streamlit Community Cloud
1. Create a PRIVATE GitHub repository.
2. Upload this folder's contents (keep the `data` folder).
3. In Streamlit Community Cloud choose **Create app**.
4. Select the private repository and `streamlit_app.py`.
5. Deploy.
6. In the app's Sharing settings choose **Only specific people can view this app** and add approved emails.

## Maintenance
The app code should rarely need changing. Most maintenance is in:
- `data/stakeholders.csv`
- `data/sources.csv`
- `data/relationships.csv`
- `data/projects.csv`
- `data/issue_routes.csv`

Commit edited data files to GitHub and the deployment will update.

## Important privacy rule
The seed dataset contains only public professional information. If you start adding private meeting notes, relationship assessments or non-public project information:
- keep the GitHub repository private,
- keep the Streamlit app private,
- restrict viewers deliberately,
- do not put secrets/passwords/API keys into CSV files.

## Current verification date
Seed review: 2026-10-09.
Municipal political profiles should be rechecked around/after the 2026 local-government election cycle.
