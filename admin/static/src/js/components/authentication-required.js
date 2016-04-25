import React from 'react';


class AuthenticationRequired extends React.Component {
    static contextTypes = {
        router: React.PropTypes.object.isRequired
    };

    componentWillMount() {
        if (!window.loggedIn) {
            this.context.router.replace('/login');
        }
    }

    componentWillReceiveProps(nextProps) {
        if (!window.loggedIn) {
            this.context.router.replace('/login');
        }
    }
    
    render() {
        return (
            <div>{this.props.children}</div>
        );
    }
}


export default AuthenticationRequired;