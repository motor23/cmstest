import React from 'react';


class Stream extends React.Component {
    render() {
        return (
            <div>
                {this.props.children}
            </div>
        );
    }
}


export default Stream;