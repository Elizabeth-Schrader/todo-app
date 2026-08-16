def prompt_nonblank(prompt):
    text = input(prompt).strip()
    if not text:
        return None
    return text
