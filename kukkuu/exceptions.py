from graphql import GraphQLError


class KukkuuGraphQLError(GraphQLError):
    """GraphQLError that is not sent to Sentry."""
