import React, {Component, PropTypes, cloneElement} from 'react';
import {connect} from 'react-redux';

import Connecting from './connecting';
import Login from './login';


class App extends Component {
    static propTypes = {
        children: PropTypes.any,
        actions: PropTypes.object.isRequired,
        app: PropTypes.object.isRequired
    };

    componentWillMount() {
    }

    componentWillReceiveProps(nextProps, nextContext) {
    }

    render() {
        const {children, ...props} = this.props;
        if (!props.app.isConnected) {
            return <Connecting {...props}/>;
        }
        if (!props.app.isLogged) {
            return <Login {...props}/>;
        }
        if (!props.app.configuration) {
            return <Loading {...props}/>;
        }
        return cloneElement(children, props);
        /*
        return (

        )
        */
    }
}


export default App;