import streamlit.report_thread as ReportThread
from streamlit.server.server import Server


class SessionState():
    """SessionState: Add per-session state to Streamlit."""
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    
    session_id = ReportThread.get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError('Could not get Streamlit session object.')

    this_session = session_info.session

    if not hasattr(this_session, '_custom_session_state'):
        this_session._custom_session_state = SessionState(**kwargs)

    return this_session._custom_session_state