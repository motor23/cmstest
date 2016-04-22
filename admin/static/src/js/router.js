import {createElement} from 'react';
import {render} from 'react-dom';
import {Router, browserHistory} from 'react-router';

import assert from './util/assert';

import AuthenticationRequired from './components/authentication-required';
import Application from './components/application';
import Dashboard from './components/dashboard';
import Login from './components/login';
import Stream from './components/stream';
import StreamList from './components/stream-list';
import StreamItem from './components/stream-item';


let routes = {
    path: '/',
    component: Application,
    childRoutes: [
        {
            path: 'login',
            component: Login
        },
        {
            component: AuthenticationRequired,
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
        }
    ]
};


function run({routes, node}) {
    assert(routes, 'Parameter `routes` is required!');
    assert(node, 'Parameter `node` is required!');
    return render(
        createElement(Router, {routes: routes, history: browserHistory}),
        node
    );
}


export {run, routes};