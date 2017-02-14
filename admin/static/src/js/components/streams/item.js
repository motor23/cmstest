import React, {Component, PropTypes} from 'react';


export class StreamItem extends React.Component {
    render() {
        return (
            <div>
                <div>Item: {this.props.params.id}</div>
            </div>
        );
    }
}