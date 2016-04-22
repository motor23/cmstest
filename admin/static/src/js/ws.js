import assert from 'util/assert';


class WSDispatcher {
    constructor(url) {
        assert(url, 'Argument `url` is required!');
        this.url = url;
        this.socket = null;
        this.subscriptions = [];
    }

    connect() {
        this.socket = new WebSocket(this.url);
        this.socket.onopen = this.onOpen.bind(this);
        this.socket.onclose = this.onClose.bind(this);
        this.socket.onerror = this.onError.bind(this);
        this.socket.onmessage = this.onMessage.bind(this);
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    onOpen(event) {

    }

    onClose(event) {

    }

    onError(event) {

    }

    onMessage(event) {
        let message = JSON.parse(event.data);
        this.subscriptions.map(subscription => {
            if (message.name === subscription.name) {
                subscription.callback(message);
            }
        });
    }

    send(name, body) {
        let message = {name: name, body: body};
        this.socket.send(JSON.stringify(message));
    }

    subscribe(name, callback) {
        let subscription = {name: name, callback: callback};
        let unsubscribe = () => {
            let index = this.subscriptions.indexOf(subscription);
            if (index > -1) {
                this.subscriptions.splice(index, 1);
            }
        };
        this.subscriptions.push(subscription);
        return unsubscribe;
    }
}
