def apply_filters(sites, exclude_list, active, shopify, fast):
    filtered = [s for s in sites if s["domain"] not in exclude_list]

    if active:
        filtered = [s for s in filtered if s["status"] != "down"]

    if shopify:
        filtered = [s for s in filtered if s["shopify"]]

    if fast:
        filtered = [s for s in filtered if s["load_time"] is not None and s["load_time"] <= 5]

    return filtered
