import React from 'react';
import {connect} from 'react-redux';

import {loginWithToken} from '../actions/auth';
import Login from './login';
import Menu from './menu';
import Notifications from './notifications';


class Application extends React.Component {
    componentWillMount() {
        const token = localStorage.getItem('token');
        if (token) {
            this.props.dispatch(loginWithToken(token));
        }
    }

    render() {
        const {isLoggedIn, menu, children, user} = this.props;
        if (!isLoggedIn) { return <Login/>;}
        return (
            <div className="mdl-layout mdl-layout--fixed-header">
                <Notifications/>
                <div className="mdl-layout__header">
                    <div className="mdl-layout__header-row">
                        <Menu menu={menu}/>
                    </div>
                </div>
                <div className="mdl-layout__content mdl-color-text--grey-600">
                    {React.Children.only(children)}
                </div>
            </div>
        )
    }
}


function mapStateToProps(state, props) {
    return {
        isLoggedIn: state.user.isLoggedIn,
        menu: state.conf.menu,
        user: state.user
    };
}


export default connect(mapStateToProps)(Application);