import unicodedata

def get_subject_options(records):
    subjects = set()

    for record in records:
        subjects.add(record["subject"])

    return sorted(subjects)

def find_existing_subject(subject, records):
    normalized_subject = normalize_subject(subject)

    for existing_subject in get_subject_options(records):
        if normalize_subject(existing_subject) == normalized_subject:
            return existing_subject

    return subject

def normalize_subject(subject):
     subject = unicodedata.normalize("NFKC", subject)
     return subject.strip().casefold()
