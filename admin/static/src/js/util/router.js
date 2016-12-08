import React, {Component, PropTypes} from 'react';


export function flatten(nodes, parents=[]) {
    return [].concat.apply([], nodes.map(node => {
        if (Array.isArray(node.children)) {
            return flatten(node.children, parents.concat(node));
        }
        let path = parents.reduceRight((path, parent) =>
            parent.path + path, node.path);
        let onEnter = parents.reduceRight((hooks, parent) =>
            hooks.concat(parent.onEnter || []), node.onEnter || []).reverse();
        let onLeave = parents.reduceRight((hooks, parent) =>
            hooks.concat(parent.onLeave || []), node.onLeave || []).reverse();
        let children = node.children;
        return {path, onEnter, onLeave, children};
    }));
}


export function escape(pattern) {
    return pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}


export function compile(pattern) {
    let match;
    let lastIndex = 0;
    let matcher = /:([a-zA-Z_$][a-zA-Z0-9_$]*)|\*/g;
    let re = '^';
    let names = [];
    let tokens = [];
    while (match = matcher.exec(pattern)) {
        if(match.index !== lastIndex) {
            tokens.push(pattern.slice(lastIndex, match.index));
            re += escape(pattern.slice(lastIndex, match.index));
        }
        if (match[1]) {
            re += '([^/]+)';
            names.push(match[1]);
        } else if (match[0] === '*') {
            re += '(.*)';
            names.push('splat');
        }
        tokens.push(match[0]);
        lastIndex = matcher.lastIndex;
    }
    if (lastIndex !== pattern.length) {
        tokens.push(pattern.slice(lastIndex, pattern.length));
        re += escape(pattern.slice(lastIndex, pattern.length));
    }
    re += '$';
    return {pattern, re, tokens, names};
}


export function match(pattern, pathname) {
    let {re, names} = compile(pattern);
    let match = pathname.match(new RegExp(re, 'i'));
    if (match) {
        let values = match.slice(1).map(value => value && decodeURIComponent(value));
        return {names, values};
    }
    return null;
}