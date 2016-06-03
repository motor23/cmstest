class Log {
    constructor() {
        this.logs = [];
        this.logsMaxCount = 1000;
        this.cursor = 0;
    }

    log(message) {
        const date = (new Date()).toISOString();
        const value = [date, message].join(' ');
        this.logs.push(value);
        if (this.logs.length > this.logsMaxCount) {
            this.logs.shift();
            this.cursor--;
        }
    }

    info() {

    }

    warning() {

    }

    error() {

    }

    persist() {
    }

    clear() {
    }
}


export default new Log();