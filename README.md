# Smart File Organizer

Smart File Organizer is a Streamlit dashboard that helps you keep folders tidy by organizing files (by extension), browsing them folder-wise, and safely renaming/deleting when needed. It also supports undoing the last organization and shows a live log.

## Features
- Create new empty files
- Upload/add files into your main folder
- Organize files into category folders
- Folder-wise browsing (Main Folder, Documents, Images, Audio, Videos, Archives, Code, Others, Duplicates)
- Open, rename, and delete files
- Undo the last organization action
- Duplicate detection
- Logs panel
- Watchdog backend for real-time updates

## Tech Stack
- Python
- Streamlit
- Pandas
- Watchdog

## How to Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Project Structure (high level)
- `streamlit_app.py` — UI (tabs/radio + table + actions)
- `main.py` — organize/scan logic
- `organizer/*` — organizing utilities (renamer/mover/scanner/history, etc.)
- `undo.py` — undo last organization
- `watcher.py` — watchdog integration

## Use Case
- You dump files into one folder.
- Smart File Organizer helps you sort them and inspect the results.
- If something looks wrong, you can undo the last organization.

## Screenshots
![Dashboard](screenshots/dashboard.png)

## Future Improvements
- More detailed history (multiple undo steps)
- Custom rules for file categorization
- Bulk actions (select multiple files)


