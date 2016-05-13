class Connection {
    constructor(url, dispatch, endpoints) {
        this.url = url;
        this.ready = false;
        this.socket = null;
        this.reconnects = -1;
        this.dispatch = dispatch;
        this.endpoints = endpoints;
        this.queue = [];
        this._open = this._open.bind(this);
        this._close = this._close.bind(this);
        this._message = this._message.bind(this);
        this.connect();
    }

    connect() {
        this.socket = new WebSocket(this.url);
        this.socket.addEventListener('open', this._open);
        this.socket.addEventListener('close', this._close);
        this.socket.addEventListener('message', this._message);
    }

    send(message) {
        if (this.ready) {
            this.socket.send(JSON.stringify(message));
            return true;
        }
        this.queue.push(message);
        return false;
    }

    flush() {
        this.queue = this.queue.filter(message => this.send(message));
    }

    _open(event) {
        this.ready = true;
        this.reconnects = this.reconnects + 1;
        this.flush();
    }

    _close(event) {
        this.ready = false;
        this.connect();
    }

    _message(event) {
        const {name, body} = JSON.parse(event.data);
        if (this.endpoints[name]) {
            this.endpoints[name](this.dispatch, body);
        }
    }
}


export default function configureConnection(url, dispatch, endpoints) {
    return new Connection(url, dispatch, endpoints);
};