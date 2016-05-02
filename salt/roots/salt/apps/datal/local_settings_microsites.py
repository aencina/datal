RAVEN_CONFIG = {
    'dsn': '{{ pillar["sentry_dns_microsites"] }}',
}

DEBUG = {{ pillar["application"]["settings"]["debug"]}}