import React, {Component, PropTypes} from 'react';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import Spinner from './common/spinner';


class Field extends Component {
    static propTypes = {
        onChange: PropTypes.func.isRequired,
        name: PropTypes.string.isRequired,
        widget: PropTypes.string.isRequired,
        errors: PropTypes.object.isRequired,
        values: PropTypes.any.isRequired,
        fields: PropTypes.array.isRequired
    };

    constructor() {
        super();
        this.onChange = this.onChange.bind(this);
    }

    onChange(event) {
        const {onChange, name} = this.props;
        const value = event.target.value;
        onChange(name, value);
    }

    render() {
        const {label, values} = this.props;
        return (
            <div>
                <label>{label}</label>
                <input type="input" value={values} onChange={this.onChange}/>
            </div>
        );
    }
}


class Form extends Component {
    static propTypes = {
        fields: PropTypes.array.isRequired,
        values: PropTypes.object.isRequired
    };

    constructor() {
        super();
        this.onUpdate = this.onUpdate.bind(this);
    }

    onUpdate(name, value) {
        const {values, onChange} = this.props;
        onChange({...values, [name]: value});
    }

    render() {
        const {fields, values} = this.props;
        return (
            <div>
                {fields.map(field =>
                    <Field
                        onChange={this.onUpdate}
                        name={field.name}
                        label={field.label}
                        widget={field.widget}
                        errors={{}}
                        values={values[field.name]}
                        fields={[]}
                     />
                )}
            </div>
        );
    }
}


export class StreamItem extends Component {
    static propTypes = {
        id: PropTypes.string.isRequired,
        stream: PropTypes.string.isRequired,
        fields: PropTypes.array.isRequired,
        values: PropTypes.object.isRequired
    };

    constructor() {
        super();
        this.onChange = this.onChange.bind(this);
    }

    onChange(values) {
        const {actions, id, stream} = this.props;
        actions.updateItem({id, stream, values});
    }

    componentWillMount() {
        const {actions, id, stream} = this.props;
        actions.fetchItem({id, stream});
    }

    componentWillReceiveProps(nextProps) {
        const {actions, id, stream} = this.props;
        if (nextProps.id !== id || nextProps.stream !== stream) {
            actions.fetchStreamItem({id: nextProps.id, stream: nextProps.stream});
        }
    }

    render() {
        const {values, fields} = this.props;
        return (
            <Form fields={fields} values={values} errors={{}} onChange={this.onChange}/>
        );
    }
}


export function mapStateToProps(state, ownProps) {
    return {
        id: ownProps.match.params.id,
        stream: ownProps.match.params.stream,
        fields: state.item.fields,
        values: state.item.values
    };
}


export function mapDispatchToProps(dispatch, ownProps) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(StreamItem);