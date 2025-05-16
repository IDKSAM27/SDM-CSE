def get_emails(websites):
    return [{"website": site, "email": f"contact@{site}"} for site in websites]
