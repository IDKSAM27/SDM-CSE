def apply_filters(sites, exclude_list, active, shopify, fast):
    filtered = [s for s in sites if s not in exclude_list]
    # Dummy filters for now
    if shopify:
        filtered = [s for s in filtered if "shop" in s]
    return filtered