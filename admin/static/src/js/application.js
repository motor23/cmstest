import React, {createElement, Component, PropTypes, Children} from 'react';


import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import StreamList from './components/streams/list';
import StreamItem from './components/streams/item';


class Application extends Component {
    static propTypes = {
        connection: ConnectionPropType.isRequired,
        children: PropTypes.element.isRequired
    };

    static childContextTypes = {
        connection: ConnectionPropType.isRequired
    };

    state = {
        isLogged: false,
        isConnected: false,
        isStalled: false
    };

    getChildContext() {
        return {connection: this.props.connection};
    }

    componentWillMount() {

    }

    componentWillUnmount() {

    }

    render() {
        let {isLogged, isConnected} = this.state;
        if (!isConnected) {
            return
        }
        return Children.only(this.props.children);
    }
}

export default function configureRouter(store) {
    return (
        <Provider store={store}>
            <RouteConfigurator/>
        </Provider>
    );
}
