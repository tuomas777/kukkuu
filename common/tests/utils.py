def assert_permission_denied(response):
    assert (
        response["errors"][0]["message"]
        == "You do not have permission to perform this action"
    )
