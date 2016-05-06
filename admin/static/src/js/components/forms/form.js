import {Component, PropTypes, createElement} from 'react';


function elementFromJSON(registry, field, data, errors) {
    assert(registry.hasOwnProperty(field.name),
        'Cannot find component for widget `%s`!', field.widget);
    assert(data.hasOwnProperty(field.name),
        'Cannot find data for field`%s`!', field.name);
    let component = registry[field.name];
    let props = {
        field: field,
        value: data[field.name],
        error: errors[field.name]
    };
    return createElement(component, props);
}


class Row extends Component {
    static propTypes = {
        field: PropTypes.object.isRequired,
        data: PropTypes.object.isRequired,
        errors: PropTypes.object.isRequired
    };

    static contextTypes = {
        widgets: PropTypes.object.isRequired
    };

    render() {
        const {field, data, error} = this.props;
        return (
            <div className="row">
                {field.label && <label htmlFor={field.id}>{field.label}</label>}
                {error && <div className="error">{error}</div>}
                <FieldFromJSON field={field} data={data}/>
            </div>
        )
    }
}


class Form extends Component {
    static propTypes = {
        widgets: PropTypes.object.isRequired,
        fields: PropTypes.arrayOf(PropTypes.object).isRequired,
        data: PropTypes.object.isRequired,
        errors: PropTypes.object.isRequired,
        onChange: PropTypes.func.isRequired
    };

    static childContextTypes = {
        widgets: PropTypes.object.isRequired
    };

    getChildContext() {
        return {
            widgets: this.props.widgets
        }
    }

    getStateFromProps(props) {
    }

    constructor(props) {
        super(props);
        this.state = this.getStateFromProps(props);
    }

    render() {
        const {fields, data, errors} = this.props;
        return (
            <form className="form">
                {fields.map(field =>
                    <Row
                        field={field}
                        data={data[field.name]}
                        errors={errors[field.name]}
                    />
                )}
            </form>
        );
    }
}


export {Form, elementFromJSON};