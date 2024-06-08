from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def normalize_uri(database_uri: str) -> str:
    parsed_uri = urlparse(database_uri)
    query_params = parse_qs(parsed_uri.query)
    if 'reinitialize' in query_params:
        del query_params['reinitialize']

    normalized_uri = parsed_uri._replace(query=urlencode(query_params, doseq=True))
    normalized_url = urlunparse(normalized_uri)

    return normalized_url


def has_reinitialize(database_uri: str) -> bool:
    parsed_uri = urlparse(database_uri)
    query_params = parse_qs(parsed_uri.query)
    reinitialize_values = query_params.get('reinitialize', [])

    return False if not reinitialize_values else reinitialize_values[0].lower() == 'true'
