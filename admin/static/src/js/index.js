import React from 'react';
import {render} from 'react-dom';
import {Router, browserHistory} from 'react-router';
import {Provider} from 'react-redux';

import configureStore from './configureStore';
import configureRoutes from './configureRoutes';


const initialState = {
    user: null,
    isConnected: false,
    isAuthenticated: false
};
const store = configureStore(initialState);
const routes = configureRoutes();
const routerProps = {routes: routes, history: browserHistory};
const providerProps = {store: store};
const router = React.createElement(Router, routerProps);
const provider = React.createElement(Provider, providerProps, router);
const root = render(provider, document.getElementById('application'));


window.store = store;
window.root = root;