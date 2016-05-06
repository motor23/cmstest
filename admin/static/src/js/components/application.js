import React from 'react';
import {connect} from 'react-redux';


class Application extends React.Component {
    static propTypes = {
        user: React.PropTypes.object,
        isConnected: React.PropTypes.bool.isRequired,
        isAuthenticated: React.PropTypes.bool.isRequired
    };

    componentWillMount() {
    }

    componentWillUpdate(nextProps, nextState) {
    }

    render() {
        return React.Children.only(this.props.children);
    }
}


function mapStateToProps (state) {
    return {
        user: state.user,
        isConnected: state.isConnected,
        isAuthenticated: state.isAuthenticated
    };
}


export default connect(mapStateToProps)(Application);