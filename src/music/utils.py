def get_correct_name(title: str, all_titles: list) -> str:
    n = 1
    if title[-1] == ')' and title[-3] == '(' and title[-2].isdigit() and len(title) > 3:
        title = title[:-3]
    new_title = title
    while new_title in all_titles:
        new_title = f'{title}({n})'
        n += 1
    return new_title
