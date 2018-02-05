from empty import Empty


class App(Empty):
    def configure_views(self):
        @self.route('/')
        def index():
            """Use this to make sure your web app is reachable"""
            return """
            <html><head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.14/semantic.min.css" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.14/semantic.min.js"></script>
            </head><body>
            <div class="ui grid container">
                <div class="row">
                    <h1 class="ui header">Flask Empty API</h1>
                </div>
                <div class="row">
                Hello. This boilerplate was done to help those interested in the
                Flask web framework to rapidly start coding robust API's. Most
                tools are setup with sensible defaults.</div>

                <div class="row">
                This boilerplate is websocket ready (flask-socketio), can handle
                async tasks (flask-rq2), json requests and response with
                serialization, token authentication, has ORM support
                (sqlalchemy+alembic) and so on.</div>

                <div class="row">
                The app service supports pdb debugging (just run the project in
                daemon mode and attach to app), you have a few nice helpful
                commands available through fabric out-of-the-box and a neat
                project structure.</div>

                <div class="row">
                For deployment, just remember to setup your swarm secrets and
                you should be ready to go. If you wish to help, create an issue
                for any bugs that you find and leave a star. PR's are welcomed.
                </div>
                <div class="row">
                    <div class="ui horizontal list">
                        <div class="item">
                        <a target="_blank" href="https://github.com/italomaia/flask-empty-api">Github</a>
                        </div>
                        <div class="item">
                            <a target="_blank" href="https://github.com/italomaia">Author</a>
                        </div>
                    </div>
                </div>
            </div>
            </body></html>
            """

    def configure_error_handlers(self):
        """SPA"""
        pass


if __name__ == '__main__':
    from auto import app
    from extensions import io

    io.run(app)
