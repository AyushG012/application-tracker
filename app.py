import streamlit as st
import pandas as pd

from gmail_client import scan_emails


st.set_page_config(
    page_title="ApplicationTracker",
    page_icon="📨",
    layout="wide",
)

st.title("📨 ApplicationTracker")
st.write("Track internship application updates from your Gmail inbox.")

if "emails" not in st.session_state:
    st.session_state.emails = []

if st.button("🔄 Scan Gmail", type="primary"):
    with st.spinner("Scanning Gmail for application updates..."):
        try:
            st.session_state.emails = scan_emails()
            st.success(
                f"Found {len(st.session_state.emails)} matching emails."
            )
        except Exception as exc:
            st.error(f"Could not scan Gmail: {exc}")

emails = st.session_state.emails

if emails:
    df = pd.DataFrame(emails)

    statuses = [
        "Offer",
        "Interview",
        "Assessment",
        "Applied",
        "Rejected",
        "Update",
    ]

    st.subheader("Overview")
    columns = st.columns(len(statuses))

    for column, status in zip(columns, statuses):
        count = int((df["status"] == status).sum())
        column.metric(status, count)

    st.divider()
    st.subheader("Application emails")

    search = st.text_input("Search by subject, sender, or email preview")
    selected_statuses = st.multiselect(
        "Filter by status",
        options=statuses,
        default=statuses,
    )

    filtered = df[df["status"].isin(selected_statuses)]

    if search:
        search_mask = (
            filtered["subject"].str.contains(search, case=False, na=False)
            | filtered["sender"].str.contains(search, case=False, na=False)
            | filtered["snippet"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[search_mask]

    display_df = filtered[
        ["date", "status", "subject", "sender", "snippet"]
    ].rename(
        columns={
            "date": "Date",
            "status": "Status",
            "subject": "Subject",
            "sender": "From",
            "snippet": "Preview",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Open an email")
    for email in filtered.to_dict("records"):
        with st.expander(f'{email["status"]}: {email["subject"]}'):
            
            st.write(f'**From:** {email["sender"]}')
            st.write(f'**Date:** {email["date"]}')

            if email.get("company"):
                st.write(f'**Company:** {email["company"]}')

            if email.get("role"):
                st.write(f'**Role:** {email["role"]}')

            if email.get("confidence") is not None:
                st.write(
                    f'**Classification confidence:** '
                    f'{email["confidence"]:.0%}'
                )

            if email.get("reason"):
                st.write(f'**Reason:** {email["reason"]}')

            st.write(email["snippet"])
            st.link_button("Open in Gmail", email["link"])


else:
    st.info("Click **Scan Gmail** to find internship application updates.")

st.caption("Gmail access is read-only. Your email contents are not stored in a database.")