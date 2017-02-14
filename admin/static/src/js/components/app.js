import React, {Component, PropTypes} from 'react';
import {Match, Link} from 'react-router';
import {Waiting} from './waiting';
import {Login} from './login';
import DashboardContainer from '../containers/DashboardContainer';
import {StreamContainer} from '../containers/StreamContainer';


export default class App extends Component {
    static propTypes = {
        actions: PropTypes.object.isRequired,
        app: PropTypes.object.isRequired
    };

    componentWillReceiveProps(nextProps) {
        if (nextProps.app.isLogged && !nextProps.app.isConfigured) {
            this.props.actions.configure();
        }
    }

    render() {
        const {isConnected, isLogged, isConfigured} = this.props.app;

        if (!isConnected) {
            return <Waiting>Подключение к серверу</Waiting>;
        }
        if (!isLogged) {
            return <Login {...this.props}/>;
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
                    <Match pattern="/streams/:stream" component={StreamContainer}/>
                </div>
            </div>
        );
    }
}