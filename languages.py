TARGET_LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
    ("kk", "Kazakh"),
    ("uz", "Uzbek (Latin)"),
    ("uz-Cyrl", "Uzbek (Cyrillic)"),
    ("ky", "Kyrgyz"),
    ("tg", "Tajik"),
    ("tk", "Turkmen"),
    ("az", "Azerbaijani"),
    ("ka", "Georgian"),
    ("hy", "Armenian"),
    ("tr", "Turkish"),
    ("fa", "Persian (Farsi)"),
    ("prs", "Dari"),
    ("ps", "Pashto"),
    ("mn-Cyrl", "Mongolian (Cyrillic)"),
    ("tt", "Tatar"),
    ("ba", "Bashkir"),
    ("uk", "Ukrainian"),
    ("zh-Hans", "Chinese (Simplified)"),
]

SOURCE_LANGUAGES = TARGET_LANGUAGES

CONTENT_TYPES = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".pdf":  "application/pdf",
    ".txt":  "text/plain",
}

GLOSSARY_CONTENT_TYPES = {
    ".tsv": "text/tab-separated-values",
    ".csv": "text/csv",
    ".xlf": "application/xliff+xml",
}
