import React from 'react';


class AuthenticationRequired extends React.Component {
    render() {
        return (
            <div>{this.props.children}</div>
        );
    }
}


export default AuthenticationRequired;