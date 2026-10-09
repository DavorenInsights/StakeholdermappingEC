# Eastern Cape Hydrogen Stakeholder Dashboard — V1

A deliberately simple first draft focused on the interface.

## Included
- Clean visual clickable organogram/dashboard
- Profile search and filtered directory
- Individual stakeholder profiles
- Public sources and data-quality indicators
- Edit profile / add working notes button
- Export of edited stakeholder database

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy privately
1. Create a **private** GitHub repository.
2. Upload `streamlit_app.py`, `requirements.txt`, and the `data/` folder.
3. Deploy `streamlit_app.py` with Streamlit Community Cloud.
4. Restrict app sharing to approved users.

## Editing in V1
Profile edits are intentionally **session-based**. This avoids adding a database before the interface has been tested.

Use **Download edited database** in the sidebar to preserve your changes as `stakeholders_updated.csv`.

Once the interface proves useful, persistent saving can be added without redesigning the dashboard.
