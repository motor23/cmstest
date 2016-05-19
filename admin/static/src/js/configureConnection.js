class Connection {
    constructor(url) {
        this._url = url;
        this._websocket = null;
        this._calls = {};
        this._queue = [];
        this._ready = false;
        this._connect();
    }

    _connect() {
        //this._websocket && this._websocket.close();
        this._websocket = new WebSocket(this._url);
        this._websocket.addEventListener('open', this._open.bind(this));
        this._websocket.addEventListener('close', this._close.bind(this));
        this._websocket.addEventListener('message', this._message.bind(this));
    }

    _send(message) {
        if (this._ready) {
            this._websocket.send(JSON.stringify(message));
            return true;
        }
        this._queue.push(message);
        return false;
    }

    _open(event) {
        this._ready = true;
        this._queue = this._queue.filter(this._send.bind(this));
    }

    _close(event) {
        this._ready = false;
        this._websocket = null;
        this._connect();
    }

    _message(event) {
        const {request_id, name, body} = JSON.parse(event.data);
        const call = this._calls[request_id];
        call && delete this._calls[request_id];
        call && call.resolve(body);
    }

    call(method, payload) {
        return new Promise((resolve, reject) => {
            const requestId = Math.floor(Math.random() * 10e12);
            this._calls[requestId] = {resolve, reject};
            this._send({request_id: requestId, name: method, body: payload});
        });
    }
}



export default function configureConnection(url) {
    return new Connection(url);
};