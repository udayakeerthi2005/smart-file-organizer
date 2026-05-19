- [ ] Inspect current streamlit_app.py for UI/UX issues (messages, rerun usage, tab structure, selection validation)
- [ ] Edit streamlit_app.py:
  - [x] Keep build_folder_dataframe exactly as fixed (empty-safe columns)
  - [x] Update open_file() to exact helper logic requested
  - [x] Clean up action messages (Opened/Deleted/Renamed/Created)
  - [x] Enforce validation: Open/Rename/Delete warn when no file is selected
- [x] Fix Create File UX: ensure only runs inside Create button handler; remove any initial-load opening behavior
  - [x] Remove/limit st.rerun(): only after Organize Files / Undo Last Organization
  - [x] Replace st.tabs with radio (selected_tab/current_tab in session_state) while keeping folder-wise sections
  - [x] Reduce over-commenting and improve spacing/layout grouping

- [ ] Edit README.md:
  - [x] Make wording more natural
  - [x] Add Screenshots section with placeholders
- [ ] Edit .gitignore to match requested content

- [ ] Run python compile check and `streamlit run streamlit_app.py` (manually verify critical flows)
- [ ] Final verification checklist: Create/Add/Organize/Undo/Open/Rename/Delete, Logs, folder-wise sections, no KeyError

