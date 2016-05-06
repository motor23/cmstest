import assert from './util/assert';


class Connection {
    constructor(endpoint) {
        assert(typeof endpoint === 'string', 'Argument `endpoint` must be a string');
        this.subscriptions = [];
        this.endpoint = endpoint;
        this.reconnect();
    }

    reconnect() {
        this.socket = new WebSocket(this.endpoint);
        this.socket.addEventListener('error', this.onError.bind());
        this.socket.addEventListener('close', this.onClose.bind());
        this.socket.addEventListener('open', this.onOpen.bind());
        this.socket.addEventListener('message', this.onMessage.bind());
    }

    onError(event) {}

    onClose(event) {}

    onOpen(event) {}

    onMessage(event) {
        let msg = JSON.parse(event.data);
        this.subscriptions.map(subscription => {
            msg.name === subscription.name && subscription.callback(msg);
        });
    }

    send(name, body) {
        this.socket.send(JSON.stringify({name: name, body: body}));
    }

    receive(name, callback) {
        let subscription = {name: name, callback: callback};
        subscription.unsubscribe = () => {
            let index = this.subscriptions.indexOf(subscription);
            (index > -1) && this.subscriptions.splice(index, 1);
        };
        this.subscriptions.push(subscription);
        return subscription;
    }
}


export default Connection;