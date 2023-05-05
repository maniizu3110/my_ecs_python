def lambda_handler(event, context):
    headers = event.get("headers", {})

    # ALB Health check
    if headers.get("user-agent") == "ELB-HealthChecker/2.0":
        return {
            "statusCode": 200,
            "statusDescription": "200 OK",
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "text/html"
            }
        }

    return {
        "statusCode": 401,
        "statusDescription": "401 Unauthorized",
        "body": "Unauthorized",
        "isBase64Encoded": False,
        "headers": {
            "WWW-Authenticate": "Basic",
            "Content-Type": "text/html"
        }
    }