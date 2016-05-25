import {createElement} from 'react';
import {Router, browserHistory} from 'react-router';
import {syncHistoryWithStore} from 'react-router-redux';
import {Provider} from 'react-redux';


import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import Stream from './components/streams/index';
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
                path: ':stream',
                component: Stream,
                indexRoute: {component: StreamList},
                childRoutes: [
                    {
                        path: ':id',
                        component: StreamItem
                    }
                ]
            }
        ]
    };
    return createElement(Provider, {store}, createElement(Router, {routes, history}));
}