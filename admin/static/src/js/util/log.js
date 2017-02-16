import moment from 'moment';


class Logger {
    constructor(db) {
        this.db = db;
        this.logs = [];
        this.logsMaxCount = 10000;
        this.cursor = 0;
        this.pending = false;
        this.timer = setInterval(10000, this.persist.bind(this));
    }

    log(message) {
        const timestamp = moment().locale('en').format('YYYY-MMMM-DD HH:mm:ss: ');
        this.logs.push(timestamp + message);
        if (this.logs.length > this.logsMaxCount) {
            this.logs.shift();
            this.cursor--;
        }
    }

    trace() {
        const exc = new Error();
        this.log(exc.stack);
    }

    assert(condition, format) {
        if (!condition) {
            let args = Array.prototype.slice.call(arguments, 2);
            let index = 0;
            let message = format.replace(/%s/g, () => args[index++]);
            this.log('Assertion failed: ' + message);
            throw new Error(message);
        }
    }

    clear() {
        // TODO: Clear logs from IndexedDB
    }

    persist() {
        const entries = this.logs.slice(Math.max(this.cursor, 0), this.logs.length);
        if (entries.length) {
            // TODO: Persist logs to IndexedDB
        }
    }
}



export default new Logger();
