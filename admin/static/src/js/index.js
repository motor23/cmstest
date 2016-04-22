import React from 'react';
import {run, routes} from './router';

let node = document.getElementById('application');
let router = run({routes: routes, node: node});

window.router = router;
window.React = React;