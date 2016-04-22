import React from 'react';


class Stream extends React.Component {
    render() {
        return (
            <div>
                <div>Stream: {this.props.params.stream}</div>
                {this.props.children}
            </div>
        );
    }
}


export default Stream;