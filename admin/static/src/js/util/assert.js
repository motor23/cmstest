export default function assert(condition, format) {
    if (format === undefined) {
        throw new Error('assert requires an error message argument');
    }
    if (!condition) {
        let args = Array.prototype.slice.call(arguments, 2);
        let index = 0;
        let message = format.replace(/%s/g, () => args[index++]);
        throw new Error(message);
    }
}