import React, {Component, PropTypes} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {BrowserRouter, Switch, Route, Link} from 'react-router-dom';
import * as actions from './../actions';


import {Waiting} from './waiting';
import Menu from './Menu';
import LoginContainer from './Login';
import DashboardContainer from './Dashboard';
import StreamItemContainer from './StreamItem';
import StreamListContainer from './StreamList';


export class Connection extends Component {
    static propTypes = {
        status: PropTypes.oneOf(['CONNECTING', 'CONNECTED', 'DISCONNECTED'])
    };

    getConnectionStatusText(code) {
        return code === 'CONNECTING' ? 'Подключение к' :
               code === 'CONNECTED' ? 'Подключен к' :
               code === 'DISCONNECTED' ? 'Отключен от' : '';
    }

    render() {
        const {status} = this.props;
        const connectionClass = status.toLowerCase();
        const connectionStatus = this.getConnectionStatusText(status);
        return (
            <div className={'ikcms-connection ikcms-connection_status_' + connectionClass}>
                <span className="ikcms-connection__status">{connectionStatus}&nbsp;</span>
                <span className="ikcms-connection__url">{window.config.ws} (websocket)</span>
            </div>
        );
    }
}


export class App extends Component {
    static propTypes = {
        actions: PropTypes.object.isRequired,
        isConnected: PropTypes.bool.isRequired,
        isLogged: PropTypes.bool.isRequired,
        isConfigured: PropTypes.bool.isRequired
    };

    componentWillReceiveProps(nextProps) {
        if (nextProps.isLogged && !nextProps.isConfigured) {
            this.props.actions.configure();
        }
    }

    render() {
        const {isConnected, isLogged, isConfigured, menu, status, actions} = this.props;

        if (!isConnected) {
            return <Waiting>Подключение к серверу</Waiting>;
        }
        if (!isLogged) {
            return <LoginContainer actions={actions}/>;
        }
        if (!isConfigured) {
            return <Waiting>Загрузка конфигурации</Waiting>;
        }

        return (
            <BrowserRouter>
                <div className="ikcms">
                    <Connection status={status}/>
                    <Menu children={menu}/>
                    <div className="ikcms-view">
                        <div className="mdl-layout__content mdl-color-text--grey-600">
                            <Switch>
                                <Route exact path="/" component={DashboardContainer}/>
                                <Route exact path="/streams/:stream/:id" component={StreamItemContainer}/>
                                <Route exact path="/streams/:stream" component={StreamListContainer}/>
                            </Switch>
                        </div>
                    </div>
                </div>
            </BrowserRouter>
        );
    }
}


export function mapStateToProps(state) {
    return {
        status: state.app.status,
        isConnected: state.app.isConnected,
        isLogged: state.app.isLogged,
        isConfigured: state.app.isConfigured,
        menu: state.app.menu
    };
}


export function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(App);