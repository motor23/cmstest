export class API {
    constructor(url, onSuccess, onFailure) {
        this.requestId = 0;
        this.executors = {};
        this.socket = null;
        this.url = url;
        this.onSuccess = onSuccess || function () {};
        this.onFailure = onFailure || function () {};
        this.successes = 0;
        this.retryTimer = null;
        this.retryCount = 0;
        this.retryCountMax = 10;
        this.retryDelay = 0; /* seconds */
        this.retryDelayMax = 30; /* seconds */
        this.retryDelayInitial = 1.5; /* seconds */
        this.retryDelayGrowth = 1.5;
        this.retryDelayJitter = 0.1;
    }

    connect() {
        if (this.socket === null) {
            this.socket = new WebSocket(this.url);
            this.socket.addEventListener('open', this.onOpen.bind(this));
            this.socket.addEventListener('close', this.onClose.bind(this));
            this.socket.addEventListener('message', this.onMessage.bind(this));
        }
    }

    disconnect() {
        if (this.socket !== null) {
            this.socket.close();
        }
    }

    call(endpoint, payload) {
        const requestId = this.requestId_++;
        const message = {name: 'request', request_id: requestId.toString(), handler: endpoint, body: payload};
        return new Promise((resolve, reject) => {
            this.executors[requestId] = {resolve, reject};
            this.socket.send(JSON.stringify(message));
        });
    }

    onMessage(event) {
        const {request_id, name, body} = JSON.parse(event.data);
        const executor = this.executors[request_id];
        delete this.executors[request_id];
        if (executor && name === 'response') {
            executor.resolve(body);
            return;
        }
        if (executor && name === 'error') {
            executor.reject(body);
            return;
        }
        assert(false, 'Unknown message type: %s', name);
    }

    onOpen(event) {
        this.successes += 1;
        this.retryCount = 0;
        this.retryDelay = this.retryDelayInitial;
        if (this.retryTimer) {
            clearTimeout(this.retryTimer);
            this.retryTimer = null;
        }
        this.onSuccess({url: this.url, successes: this.successes});
    }

    onClose(event) {
        this.socket = null;
        this.retryDelay = Math.max(this.retryDelay * this.retryDelayGrowth, this.retryDelayMax);
        this.retryCount += 1;
        let reason = this.successes === 0 ? 'unreachable' : event.wasClean ? 'lost' : 'closed';
        let retry = this.retryCount < this.retryCountMax ? this.retryDelay : null;
        if (retry) {
            this.retryTimer = setTimeout(this.connect.bind(this), retry);
        }
        this.onFailure({reason, retry});
    }
}


export default function configureApi(url, onSuccess, onFailure, cls=API) {
    return new cls(url, onSuccess, onFailure);
}