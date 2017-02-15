import React, {Component, PropTypes} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {Match, Link} from 'react-router';
import * as actions from './../actions';
import {Waiting} from './waiting';

import LoginContainer from './Login';
import DashboardContainer from './Dashboard';
import StreamItemContainer from './StreamItem';
import StreamListContainer from './StreamList';


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
        const {isConnected, isLogged, isConfigured, actions} = this.props;

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
            <div className="mdl-layout mdl-layout--fixed-header">
                <div className="mdl-layout__header">
                    <div className="mdl-layout__header-row">
                        <div className="cms-nav">
                            <div className="cms-nav__item">
                                <Link to="/">Начало</Link>
                            </div>
                            <div className="cms-nav__item">
                                <Link to="streams/docs/">Документы</Link>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="mdl-layout__content mdl-color-text--grey-600">
                    <Match exactly pattern="/" component={DashboardContainer}/>
                    <Match excatly pattern="/streams/:stream" component={StreamListContainer}/>
                    <Match excatly pattern="/streams/:stream/:id" component={StreamItemContainer}/>
                </div>
            </div>
        );
    }
}


export function mapStateToProps(state) {
    return {
        isConnected: state.app.isConnected,
        isLogged: state.app.isLogged,
        isConfigured: state.app.isConfigured
    };
}


export function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(App);