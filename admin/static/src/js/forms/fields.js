import {Component, PropTypes, createElement} from 'react';
import assert from 'assert';


class Hidden extends Component {
    static propTypes = {
        field: PropTypes.object.isRequired,
        value: PropTypes.string.isRequired,
        error: PropTypes.string.isRequired
    };

    render() {
        let {field, value} = this.props;
        return (
            <input
                id={field.id}
                name={field.name}
                value={value}
                type="hidden"
            />
        );
    }
}


class Text extends Component {
    render() {
        let {field, value} = this.props;
        return (
            <input
                id={field.id}
                name={field.name}
                value={value}
                type="text"
            />
        );
    }
}


class Textarea extends Component {
    render() {
        let {field, value} = this.props;
        return (
            <textarea
                name={name}
                value={value}
            />
        );
    }
}


class Password extends Component {
    render() {
        let {name} = this.props;
        let {value} = this.state;
        return (
            <input
                type="password"
                value={value}
            />
        );
    }
}


class Checkbox extends Component {
    render() {
        let {name} = this.props;
        let {value} = this.state;
        return (
            <input
                type="checkbox"
                name={name}
                value="checked"
                checked={(this.state.value + '') != ''}
            />
        );
    }
}


class FieldList extends Component {
    render() {
        let {name} = this.props;
    }
}


export {Hidden, Text, Textarea, Password, Checkbox, FieldList};
