import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {loginWithToken} from '../actions';
import Login from '../components/login';


class Application extends Component {
    static propTypes = {
        authenticated: PropTypes.bool.isRequired,
        navigation: PropTypes.arrayOf(PropTypes.object).isRequired,
        dashboard: PropTypes.arrayOf(PropTypes.object).isRequired
    };

    componentWillMount() {
        const token = localStorage.getItem('token');
        if (token) {
            this.props.dispatch(loginWithToken(token));
        }
    }

    render() {
        const {authenticated, navigation, dashboard} = this.props;

        return (
            <div className="mdl-layout mdl-layout--fixed-header">
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
        authenticated: state.user.isLoggedIn,
        navigation: state.config.menu.main,
        dashboard: state.config.menu.dashboard
    };
}


export default connect(mapStateToProps)(Application);