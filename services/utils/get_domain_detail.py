def get_domain_and_subdomain(domain: str) -> dict:
    domain_parts = domain.split(".")
    subdomain = None

    if len(domain_parts) >= 3:
        subdomain = ".".join(domain_parts[:-2])
        main_domain = ".".join(domain_parts[-2:])
    else:
        main_domain = domain

    return {
        "main_domain": main_domain,
        "subdomain": subdomain
    }