import React from 'react';


class Provider extends React.Component {
    static propTypes = {
        store: React.PropTypes.object.isRequired,
        connection: React.PropTypes.object.isRequired,
        children: React.PropTypes.element.isRequired
    };

    static childContextType = {
        store: React.PropTypes.object.isRequired,
        connection: React.PropTypes.object.isRequired
    };

    getChildContext() {
        return {
            store: this.props.store,
            connection: this.props.connection
        };
    }

    componentWillMount() {
        
    }

    componentWillUnmount() {

    }

    render() {
        return React.Children.only(this.props.children);
    }
}


function provide(mapStateToProps) {
    return function compose(Component) {
        return class CompositeComponent extends React.Component {

        }
    }
}


export default Provider;