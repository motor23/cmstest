import React from 'react';
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


function run({routes, node, connection}) {
    assert(routes, 'Parameter `routes` is required!');
    assert(node, 'Parameter `node` is required!');
    let params = {
        routes: routes,
        history: browserHistory,
        createElement: (Component, props) =>
            <Component connection={connection} {...props}/>
    };
    return render(<Router {...params}/>, node);
}


export {run, routes};