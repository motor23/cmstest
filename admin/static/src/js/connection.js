import assert from './util/assert';


class Connection {
    constructor(url) {
        assert(url, 'Argument `url` is required!');
        this.subscriptions = [];
        this.socket = new WebSocket(url);
        this.socket.onmessage = this.onmessage.bind(this);
    }

    close() {
        this.socket.close();
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

    onmessage(event) {
        let msg = JSON.parse(event.data);
        this.subscriptions.map(subscription => {
            msg.name === subscription.name && subscription.callback(msg);
        });
    }

}


export default Connection;