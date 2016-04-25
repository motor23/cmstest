import React from 'react';
import Connection from './connection';
import {run, routes} from './router';


let node = document.getElementById('application');
let connection = new Connection(window.config.ws);
let router = run({routes: routes, node: node, connection: connection});


window.router = router;
window.React = React;