import streamlit as st


def dropdown(
    label: str,
    options: list,
    placeholder: str,
    key: str | None = None,
    help: str | None = None,
    disabled: bool = False
):
    """
    Reusable searchable dropdown component.
    """

    return st.selectbox(
        label=label,
        options=options,
        index=None,
        placeholder=placeholder,
        key=key,
        help=help,
        disabled=disabled
    )