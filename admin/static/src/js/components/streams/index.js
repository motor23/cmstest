import React, {Component, PropTypes} from 'react';
import {Match, Link} from 'react-router';
import {StreamList} from './list';
import {StreamItem} from './item';




export class Stream extends Component {
    render() {
        return (
            <div>
                <Match exactly pattern="" component={(props) => <StreamList {...props} {...this.props}/>}/>
                <Match pattern=":id" component={(props) => <StreamItem {...props} {...this.props}/>}/>
            </div>
        );
    }
}