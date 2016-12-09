import '../css/index.css';

import {createElement} from 'react';
import {render} from 'react-dom';
import {Provider, connect} from 'react-redux'
import configureStore from './util/store';
import configureConnection from './util/connection';
import {App} from './components';

const container = document.getElementById('application');
const connection = configureConnection(window.config.ws);
const store = configureStore(undefined, {logging: true, connection: connection});

connection.onerror = event => store.dispatch({type: 'APP_CONNECTION_CLOSED', payload: event});
connection.onopen = event => store.dispatch({type: 'APP_CONNECTION_OPENED', payload: event});

render(createElement(Provider, {store}, createElement(App)), container);
