import React from 'react';


class StreamItem extends React.Component {
    render() {
        return (
            <div>
                <div>Item: {this.props.params.id}</div>
            </div>
        );
    }
}


export default StreamItem;