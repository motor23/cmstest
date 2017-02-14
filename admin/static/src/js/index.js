import '../css/index.css';

import React from 'react';
import {render} from 'react-dom';
import {Provider} from 'react-redux';
import {BrowserRouter} from 'react-router';
import AppContainer from './containers/AppContainer';
import configureApi from './util/api';
import configureStore from './util/store';
import * as reducers from './reducers';

const node = document.getElementById('application');
const api = configureApi(window.config.ws);
const store = configureStore(undefined, {reducers, api});

api.onFailure = event => store.dispatch({type: 'CONNECTION_CLOSED', payload: event});
api.onSuccess = event => store.dispatch({type: 'CONNECTION_OPENED', payload: event});
api.connect();

window.api = api;
window.store = store;
window.React = React;
window.render = render;

render(
    <Provider store={store}>
        <BrowserRouter>
            <AppContainer/>
        </BrowserRouter>
    </Provider>
, node);