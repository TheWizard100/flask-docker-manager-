from flask import Flask, render_template, request, redirect, url_for
import docker

app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def home():
    containers = client.containers.list(all=True)
    return render_template('index.html', containers=containers)


@app.route('/create', methods=['GET', 'POST'])
def create_container():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        host_port = request.form['host_port']
        container_port = request.form['container_port']

        container = client.containers.run(image, name=name, ports={f"{container_port}/tcp": host_port}, detach=True)
        return redirect(url_for('home'))
    
    return render_template('create_container.html')


@app.route('/container/<container_id>')
def access_container(container_id):
    container = client.containers.get(container_id)
    return redirect(f'http://{container.attrs["NetworkSettings"]["Ports"][f"80/tcp"][0]["HostIp"]}:{container.attrs["NetworkSettings"]["Ports"][f"80/tcp"][0]["HostPort"]}')


@app.route('/delete/<container_id>')
def delete_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

