import {createElement} from 'react';
import {Router, browserHistory} from 'react-router';
import {syncHistoryWithStore} from 'react-router-redux';
import {Provider} from 'react-redux';


import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import StreamList from './components/streams/list';
import StreamItem from './components/streams/item';


export default function configureRouter(store) {
    const history = syncHistoryWithStore(browserHistory, store);
    const routes = {
        path: '/',
        component: Application,
        indexRoute: {component: Dashboard},
        childRoutes: [
            {
                path: ':stream/:id',
                component: StreamItem
            },
            {
                path: ':stream',
                component: StreamList
            }
        ]
    };
    return createElement(Provider, {store}, createElement(Router, {routes, history}));
}