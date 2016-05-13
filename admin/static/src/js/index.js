import React from 'react';
import {render} from 'react-dom';
import {Router, browserHistory} from 'react-router';
import {Provider} from 'react-redux';

import configureStore from './configureStore';
import configureRoutes from './configureRoutes';
import configureConnection from './configureConnection';
import {endpoints} from './actions';


const store = configureStore();
const connection = configureConnection(window.config.ws, store.dispatch, endpoints);

window.connection = connection;
window.store = store;

const routes = configureRoutes();
const router = React.createElement(Router, {routes: routes, history: browserHistory});
const provider = React.createElement(Provider, {store: store}, router);
const root = render(provider, document.getElementById('application'));