# Webhook

Examples of working with GitHub Webhooks using PyGithub and Pyramid.

## Creating and Listening to Webhooks

This example demonstrates how to:
1. Create a webhook programmatically using PyGithub
2. Set up a Pyramid-based server to listen for webhook events
3. Handle different types of webhook events (push, pull request, ping)

### Complete Example

```python
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from github import Github

ENDPOINT = "webhook"

@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
)
class PayloadView(object):
    """
    View receiving of Github payload. By default, this view it's fired only if
    the request is json and method POST.
    """

    def __init__(self, request):
        self.request = request
        # Payload from Github, it's a dict
        self.payload = self.request.json

    @view_config(header="X-Github-Event:push")
    def payload_push(self):
        """This method is triggered if header HTTP-X-Github-Event type is Push"""
        print("No. commits in push:", len(self.payload['commits']))
        return Response("success")

    @view_config(header="X-Github-Event:pull_request")
    def payload_pull_request(self):
        """This method is triggered if header HTTP-X-Github-Event type is Pull Request"""
        print("PR", self.payload['action'])
        print("No. Commits in PR:", self.payload['pull_request']['commits'])
        return Response("success")

    @view_config(header="X-Github-Event:ping")
    def payload_else(self):
        print("Pinged! Webhook created with id {}!".format(self.payload["hook"]["id"]))
        return {"status": 200}

def create_webhook():
    """Creates a webhook for the specified repository.
    
    This is a programmatic approach to creating webhooks with PyGithub's API.
    Alternatively, webhooks can be created manually in the repository's Settings page.
    """
    USERNAME = ""
    PASSWORD = ""
    OWNER = ""
    REPO_NAME = ""
    EVENTS = ["push", "pull_request"]
    HOST = ""

    config = {
        "url": f"http://{HOST}/{ENDPOINT}",
        "content_type": "json"
    }

    g = Github(USERNAME, PASSWORD)
    repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
    repo.create_hook("web", config, EVENTS, active=True)

if __name__ == "__main__":
    config = Configurator()

    create_webhook()

    config.add_route(ENDPOINT, f"/{ENDPOINT}")
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 80, app)
    server.serve_forever()
```

### Example Output

Here's what the server output looks like when receiving various webhook events:

```
x.y.w.z - - [15/Oct/2018 23:49:19] "POST /webhook HTTP/1.1" 200 15
Pinged! Webhook created with id <redacted id>!

No. commits in push: 1
x.y.w.z - - [15/Oct/2018 23:49:32] "POST /webhook HTTP/1.1" 200 7

PR synchronize
x.y.w.z - - [15/Oct/2018 23:49:33] "POST /webhook HTTP/1.1" 200 7
No. Commits in PR: 10

PR closed
x.y.w.z - - [15/Oct/2018 23:49:56] "POST /webhook HTTP/1.1" 200 7
No. Commits in PR: 10

x.y.w.z - - [15/Oct/2018 23:50:00] "POST /webhook HTTP/1.1" 200 7
PR reopened
No. Commits in PR: 10
```

## Key Components

1. **Webhook Creation**
   - Use `repo.create_hook()` to create a webhook
   - Specify the events to listen for (e.g., "push", "pull_request")
   - Configure the webhook URL and content type

2. **Event Handling**
   - Use Pyramid view decorators to handle different event types
   - Access webhook payload through `request.json`
   - Process events based on the `X-Github-Event` header

3. **Event Types**
   - `push`: Triggered when commits are pushed
   - `pull_request`: Triggered for PR actions (open, close, sync)
   - `ping`: Triggered when webhook is created

For a complete list of available event types, see [GitHub's documentation](https://developer.github.com/v3/issues/events/).

Note: This example uses Pyramid, but the webhook handling can be implemented with any web framework that can handle POST requests and JSON payloads.
