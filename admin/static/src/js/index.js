import {render} from 'react-dom';
import configureStore from './configureStore';
import configureRouter from './configureRouter';
import configureConnection from './configureConnection';


const connection = configureConnection(window.config.ws);
const store = configureStore();
const router = configureRouter(store);


window.connection = connection;
window.store = store;


render(router, document.getElementById('application'));