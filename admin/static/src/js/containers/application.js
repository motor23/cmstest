import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {loginWithToken} from '../actions';
import Login from '../components/login';
import Navigation from '../components/navigation';


class Application extends Component {
    static propTypes = {
        isAuthenticating: PropTypes.bool.isRequired,
        isAuthenticated: PropTypes.bool.isRequired,
        navigation: PropTypes.arrayOf(PropTypes.object).isRequired
    };

    componentWillMount() {
        const token = localStorage.getItem('token');
        token && this.props.dispatch(loginWithToken(token));
    }

    render() {
        const {isAuthenticating, isAuthenticated, error, navigation} = this.props;

        if (!isAuthenticated) {
            return (
                <Login
                    isAuthenticating={isAuthenticating}
                    isAuthenticated={isAuthenticated}
                    error={error}/>
            );
        }

        return (
            <div></div>
        );
    }
}


function mapStateToProps(state, props) {
    return {
        isAuthenticating: state.auth.isAuthenticating,
        isAuthenticated: state.auth.isAuthenticated,
        error: state.auth.error,
        user: state.auth.user,
        navigation: state.config.navigation
    };
}


export default connect(mapStateToProps)(Application);