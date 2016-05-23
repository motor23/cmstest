import {createElement} from 'react';
import {Router, browserHistory} from 'react-router';
import {Provider} from 'react-redux';


import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import Stream from './components/streams/stream';
import StreamList from './components/streams/stream-list';
import StreamItem from './components/streams/stream-item';


export default function configureRouter(store) {
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
    return createElement(Provider, {store: store},
        createElement(Router, {routes: routes, history: browserHistory}));
}