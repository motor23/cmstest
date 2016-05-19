import React from 'react';
import {render} from 'react-dom';
import {Router, browserHistory} from 'react-router';
import {Provider} from 'react-redux';

import configureStore from './configureStore';
import configureRoutes from './configureRoutes';
import configureConnection from './configureConnection';
import {endpoints} from './actions';


const connection = configureConnection(window.config.ws);
const store = configureStore();

window.connection = connection;
window.store = store;

const routes = configureRoutes();
const router = React.createElement(Router, {routes: routes, history: browserHistory});
const provider = React.createElement(Provider, {store: store}, router);
const root = render(provider, document.getElementById('application'));