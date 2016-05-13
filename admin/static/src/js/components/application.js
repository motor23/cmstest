import React from 'react';
import {connect} from 'react-redux';

import {loginWithToken} from '../actions';
import Login from './login';


class Application extends React.Component {
    componentWillMount() {
        const token = localStorage.getItem('token');
        if (token) {
            this.props.dispatch(loginWithToken(token));
        }
    }

    render() {
        if (!this.props.isLoggedIn) {
            return <Login/>;
        }
        return React.Children.only(this.props.children);
    }
}


const mapStateToProps = state => ({
    isLoggedIn: state.user.isLoggedIn
});


export default connect(mapStateToProps)(Application);