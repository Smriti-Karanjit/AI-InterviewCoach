import streamlit as st
from Theme import apply_neon_theme, add_sidebar_navigation # pyright: ignore[reportMissingImports]
from Theme import require_login


apply_neon_theme()
require_login()
add_sidebar_navigation()