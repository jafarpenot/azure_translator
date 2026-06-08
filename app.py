from pathlib import Path

import streamlit as st

from languages import TARGET_LANGUAGES
from translator import TranslationError, translate_document

st.set_page_config(page_title="Azure Document Translator (POC)", page_icon="🌐")

_logo = next(iter(sorted(Path("assets").glob("kpmg_logo.*"))), None)
if _logo is not None:
    st.logo(str(_logo), size="large")

st.title("Azure Document Translator")
st.caption("Upload a document, pick a target language, get the translated file back.")

with st.sidebar:
    st.header("Settings")

    AUTO = "Auto-detect"
    source_options = [AUTO] + [name for _, name in TARGET_LANGUAGES]
    source_choice = st.selectbox("Source language", source_options, index=0)
    source_code = None
    if source_choice != AUTO:
        source_code = next(c for c, n in TARGET_LANGUAGES if n == source_choice)

    target_names = [name for _, name in TARGET_LANGUAGES]
    default_target_idx = target_names.index("Russian")
    target_choice = st.selectbox(
        "Target language", target_names, index=default_target_idx
    )
    target_code = next(c for c, n in TARGET_LANGUAGES if n == target_choice)

    st.divider()
    st.subheader("Glossary (optional)")
    glossary_file = st.file_uploader(
        "Upload glossary (.tsv, .csv, .xlf)",
        type=["tsv", "csv", "xlf"],
        key="glossary",
    )

doc_file = st.file_uploader(
    "Document to translate",
    type=["docx", "pptx", "xlsx", "pdf", "txt"],
)

translate_clicked = st.button(
    "Translate", type="primary", disabled=(doc_file is None)
)

if translate_clicked and doc_file is not None:
    with st.spinner(f"Translating to {target_choice}..."):
        try:
            translated_bytes = translate_document(
                file_bytes=doc_file.getvalue(),
                filename=doc_file.name,
                target_lang=target_code,
                source_lang=source_code,
                glossary_bytes=glossary_file.getvalue() if glossary_file else None,
                glossary_filename=glossary_file.name if glossary_file else None,
            )
        except TranslationError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        else:
            stem = Path(doc_file.name).stem
            ext = Path(doc_file.name).suffix
            out_name = f"{stem}_{target_code}{ext}"
            st.success(f"Done — {len(translated_bytes):,} bytes")
            st.download_button(
                "Download translated file",
                data=translated_bytes,
                file_name=out_name,
                mime="application/octet-stream",
            )
