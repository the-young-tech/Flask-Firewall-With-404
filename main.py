from flask import Flask, render_template, request, abort

app = Flask(__name__)

@app.route('/')
def example():
    return render_template('example.html')

### Custom Firewall -> Forbidden Agents, Characters, Extensions

forbidden_agents = ['sqlmap', 'wget', 'curl']

forbidden_characters = ['//', '..', '~', '\\', '$', '$$' '%', '&', '%%', '&&', '!', '!!']

forbidden_extensions = ['.php', '.py']

def is_user_agent_forbidden(user_agent):
    return any(agent in user_agent.lower() for agent in forbidden_agents)

def does_path_contain_forbidden_characters(path):
    for char in forbidden_characters:
        if char in path:
            return True
    for ext in forbidden_extensions:
        if path.endswith(ext):
            return True
    return False

@app.before_request
def firewall():
    if is_user_agent_forbidden(request.user_agent.string):
        abort(403)

    if does_path_contain_forbidden_characters(request.path):
        abort(403)

### The 404 Redirect
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
