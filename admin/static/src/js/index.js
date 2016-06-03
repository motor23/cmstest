import '../css/index.css';

import {render} from 'react-dom';
import configureStore from './configureStore';
import configureRouter from './configureRouter';
import configureConnection from './configureConnection';


const connection = configureConnection(window.config.ws);
const store = configureStore(undefined, {logging: true, connection: connection});
const router = configureRouter(store);


connection.onerror = event =>
    store.dispatch({type: 'CONNECTION_LOST', payload: event});


connection.onopen = event =>
    store.dispatch({type: 'CONNECTION_ESTABLISHED', payload: event});


window.connection = connection;
window.store = store;


render(router, document.getElementById('application'));